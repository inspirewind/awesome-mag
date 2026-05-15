#!/usr/bin/env python3
"""Build genome-level clustering inputs from corpus downloads.

This script turns the normalized ``downloads/<slug>/`` layout into inputs for:

- RabbitTClust: one bacterial/archaeal MAG FASTA path per line.
- vclust: one merged viral genome FASTA, one viral genome per sequence record.

It is intentionally conservative. Ambiguous multi-FASTA MAG sources are reported
in ``problems.tsv`` instead of being silently treated as sequence-level genomes.
"""

from __future__ import annotations

import argparse
import bz2
import csv
import gzip
import hashlib
import io
import lzma
import re
import shutil
import sys
import tarfile
import time
import zipfile
import zlib
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import BinaryIO, Iterator


CORPUS_DIR = Path(__file__).resolve().parent
ROOT_DIR = CORPUS_DIR.parent
DEFAULT_DOWNLOADS_DIR = ROOT_DIR / "downloads"
DEFAULT_OUT_DIR = CORPUS_DIR / "cluster_inputs"

VIRAL_SLUGS = {"gut-phage-database", "mgv", "uhgv", "metavr"}
FASTA_SUFFIXES = (
    ".fa",
    ".fasta",
    ".fna",
    ".fas",
    ".ffn",
    ".fa.gz",
    ".fasta.gz",
    ".fna.gz",
    ".fas.gz",
    ".ffn.gz",
    ".fa.bz2",
    ".fasta.bz2",
    ".fna.bz2",
    ".fas.bz2",
    ".ffn.bz2",
    ".fa.xz",
    ".fasta.xz",
    ".fna.xz",
    ".fas.xz",
    ".ffn.xz",
)
PROTEIN_SUFFIXES = (
    ".faa",
    ".faa.gz",
    ".aa",
    ".aa.gz",
    ".pep",
    ".pep.gz",
    ".faa.bz2",
    ".aa.bz2",
    ".pep.bz2",
    ".faa.xz",
    ".aa.xz",
    ".pep.xz",
)
ARCHIVE_SUFFIXES = (
    ".tar",
    ".tar.gz",
    ".tgz",
    ".tar.bz2",
    ".tbz2",
    ".tar.xz",
    ".txz",
    ".zip",
)
UNSUPPORTED_ARCHIVE_SUFFIXES = (".tar.zst", ".tzst", ".zst")
IGNORED_NAMES = {
    ".download-complete",
    ".ds_store",
    "_manifest.aria2",
    "manifest.tsv",
}


class ProgressLogger:
    def __init__(self, *, quiet: bool = False) -> None:
        self.quiet = quiet
        self.started_at = time.monotonic()

    def log(self, message: str) -> None:
        if self.quiet:
            return
        elapsed = time.monotonic() - self.started_at
        print(f"[{elapsed:8.1f}s] {message}", file=sys.stderr, flush=True)


@dataclass(frozen=True)
class DatasetMeta:
    slug: str
    dataset: str
    part: str
    script: str = ""

    @property
    def scope(self) -> str:
        if self.part == "part3_viral_direct" or self.slug in VIRAL_SLUGS:
            return "viral"
        return "mag"


@dataclass(frozen=True)
class SourceFasta:
    slug: str
    dataset: str
    part: str
    scope: str
    path: Path
    archive_path: Path | None = None
    archive_type: str = ""
    member_name: str = ""
    sibling_fastas: int = 1

    @property
    def label(self) -> str:
        if self.member_name:
            return f"{self.archive_path}!{self.member_name}"
        return str(self.path)

    @property
    def name_hint(self) -> str:
        name = self.member_name or self.path.name
        for suffix in (".gz", ".fasta", ".fna", ".fa", ".fas", ".ffn"):
            if name.lower().endswith(suffix):
                name = name[: -len(suffix)]
        return Path(name).name


@dataclass
class FastaSummary:
    records: int = 0
    bases: int = 0
    sampled_records: int = 0
    sampled_bases: int = 0
    headers: list[str] = field(default_factory=list)
    truncated: bool = False

    @property
    def first_header(self) -> str:
        return self.headers[0] if self.headers else ""


@dataclass
class Layout:
    mode: str
    confidence: str
    note: str


@dataclass
class Problem:
    severity: str
    slug: str
    source: str
    code: str
    message: str


@dataclass
class MagRow:
    slug: str
    dataset: str
    scope: str
    genome_id: str
    path: Path
    source: str
    mode: str
    seq_count: int | str = ""
    bp: int | str = ""


def parse_metadata(path: Path) -> dict[str, str]:
    metadata: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return metadata
    for line in lines:
        line = line.strip()
        if not line.startswith("#"):
            continue
        payload = line[1:].strip()
        if ":" not in payload:
            continue
        key, value = payload.split(":", 1)
        metadata[key.strip().lower()] = value.strip()
    return metadata


def discover_dataset_meta(root: Path) -> dict[str, DatasetMeta]:
    rows: dict[str, DatasetMeta] = {}
    for script in sorted((root / "corpus" / "download_bash").glob("*/*.sh")):
        if script.parent.name.startswith("_"):
            continue
        metadata = parse_metadata(script)
        slug = metadata.get("slug") or script.stem
        rows[slug] = DatasetMeta(
            slug=slug,
            dataset=metadata.get("dataset", slug),
            part=metadata.get("part", script.parent.name),
            script=str(script.relative_to(root)),
        )
    return rows


def has_suffix(name: str, suffixes: tuple[str, ...]) -> bool:
    lowered = name.lower()
    return any(lowered.endswith(suffix) for suffix in suffixes)


def is_split_archive_piece(path: Path) -> bool:
    return re.search(r"\.tar\.gz\.\d+$", path.name.lower()) is not None


def is_probably_fasta_name(name: str) -> bool:
    lowered = name.lower()
    if has_suffix(lowered, PROTEIN_SUFFIXES):
        return False
    return has_suffix(lowered, FASTA_SUFFIXES)


def is_supported_archive(path: Path) -> bool:
    return has_suffix(path.name, ARCHIVE_SUFFIXES)


def is_unsupported_archive(path: Path) -> bool:
    return has_suffix(path.name, UNSUPPORTED_ARCHIVE_SUFFIXES)


def is_compressed_file(path: Path | str) -> bool:
    lowered = str(path).lower()
    return lowered.endswith((".gz", ".bz2", ".xz"))


def should_ignore_file(path: Path) -> bool:
    name = path.name.lower()
    if name in IGNORED_NAMES:
        return True
    if name.startswith("."):
        return True
    if name.endswith((".aria2", ".part", ".tmp", ".md5", ".sha256", ".crc")):
        return True
    if is_split_archive_piece(path):
        return True
    return False


def relpath(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def display_path(path: Path, root: Path) -> str:
    return relpath(path, root)


def human_bytes(value: int | None) -> str:
    if value is None:
        return "unknown size"
    units = ("B", "KiB", "MiB", "GiB", "TiB", "PiB")
    amount = float(value)
    for unit in units:
        if amount < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(amount)} {unit}"
            return f"{amount:.1f} {unit}"
        amount /= 1024
    return f"{value} B"


def output_path(path: Path, *, relative_to: Path | None) -> str:
    resolved = path.resolve()
    if relative_to is None:
        return str(resolved)
    try:
        return str(resolved.relative_to(relative_to.resolve()))
    except ValueError:
        return str(resolved)


def sanitize_id(value: str, fallback: str = "genome") -> str:
    value = value.strip().lstrip(">")
    if not value:
        value = fallback
    value = re.sub(r"\s+", "_", value)
    value = re.sub(r"[^A-Za-z0-9._|:+-]+", "_", value)
    value = value.strip("._-")
    if not value:
        value = fallback
    return value[:160]


def stable_fasta_name(genome_id: str, suffix: str = ".fna") -> str:
    clean = sanitize_id(genome_id)
    digest = hashlib.sha1(genome_id.encode("utf-8", errors="replace")).hexdigest()[:12]
    return f"{clean[:90]}__{digest}{suffix}"


def strip_fasta_suffix(name: str) -> str:
    lowered = name.lower()
    for suffix in (
        ".fasta.bz2",
        ".fna.bz2",
        ".fas.bz2",
        ".ffn.bz2",
        ".fa.bz2",
        ".fasta.xz",
        ".fna.xz",
        ".fas.xz",
        ".ffn.xz",
        ".fa.xz",
        ".fasta.gz",
        ".fna.gz",
        ".fas.gz",
        ".ffn.gz",
        ".fa.gz",
        ".fasta",
        ".fna",
        ".fas",
        ".ffn",
        ".fa",
        ".bz2",
        ".xz",
        ".gz",
    ):
        if lowered.endswith(suffix):
            return name[: -len(suffix)]
    return name


@contextmanager
def source_reader(source: SourceFasta) -> Iterator[BinaryIO]:
    @contextmanager
    def wrap_compression(raw: BinaryIO, name: str) -> Iterator[BinaryIO]:
        lowered = name.lower()
        if lowered.endswith(".gz"):
            with gzip.GzipFile(fileobj=raw) as wrapped:
                yield wrapped
        elif lowered.endswith(".bz2"):
            with bz2.BZ2File(raw) as wrapped:
                yield wrapped
        elif lowered.endswith(".xz"):
            with lzma.LZMAFile(raw) as wrapped:
                yield wrapped
        else:
            yield raw

    if source.archive_path is None:
        handle = source.path.open("rb")
        try:
            with wrap_compression(handle, source.path.name) as wrapped:
                yield wrapped
        finally:
            handle.close()
        return

    if source.archive_type == "zip":
        with zipfile.ZipFile(source.archive_path) as archive:
            with archive.open(source.member_name) as member_handle:
                with wrap_compression(member_handle, source.member_name) as wrapped:
                    yield wrapped
        return

    if source.archive_type == "tar":
        with tarfile.open(source.archive_path, mode="r:*") as archive:
            member = archive.getmember(source.member_name)
            extracted = archive.extractfile(member)
            if extracted is None:
                raise OSError(f"Could not read tar member: {source.member_name}")
            with extracted:
                with wrap_compression(extracted, source.member_name) as wrapped:
                    yield wrapped
        return

    raise OSError(f"Unsupported archive type for {source.label}: {source.archive_type}")


def iter_fasta_headers_and_lengths(handle: BinaryIO) -> Iterator[tuple[str, int]]:
    header = ""
    length = 0
    for raw_line in handle:
        line = raw_line.decode("utf-8", errors="replace").strip()
        if not line:
            continue
        if line.startswith(">"):
            if header:
                yield header, length
            header = line[1:].strip()
            length = 0
        elif header:
            length += len(re.sub(r"\s+", "", line))
    if header:
        yield header, length


def summarize_fasta(source: SourceFasta, *, sample_records: int, full: bool = False) -> FastaSummary:
    summary = FastaSummary()
    limit = 0 if full else sample_records
    with source_reader(source) as handle:
        for header, length in iter_fasta_headers_and_lengths(handle):
            summary.records += 1
            summary.bases += length
            if limit <= 0 or summary.sampled_records < limit:
                summary.sampled_records += 1
                summary.sampled_bases += length
                if len(summary.headers) < sample_records:
                    summary.headers.append(header)
            elif not full:
                summary.truncated = True
                break
    return summary


def token_from_header(header: str) -> str:
    return header.strip().lstrip(">").split(None, 1)[0]


def parse_slug_value_options(values: list[str], *, option_name: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise RuntimeError(f"{option_name} expects slug=value, got: {value}")
        slug, payload = value.split("=", 1)
        slug = slug.strip()
        payload = payload.strip()
        if not slug or not payload:
            raise RuntimeError(f"{option_name} expects non-empty slug and value, got: {value}")
        parsed[slug] = payload
    return parsed


def compile_mag_id_regexes(values: list[str]) -> dict[str, re.Pattern[str]]:
    raw = parse_slug_value_options(values, option_name="--mag-id-regex")
    compiled: dict[str, re.Pattern[str]] = {}
    for slug, pattern in raw.items():
        try:
            compiled[slug] = re.compile(pattern)
        except re.error as exc:
            raise RuntimeError(f"Invalid --mag-id-regex for {slug}: {exc}") from exc
    return compiled


def parse_layout_overrides(values: list[str]) -> dict[str, str]:
    raw = parse_slug_value_options(values, option_name="--layout-override")
    allowed = {"file_per_genome", "record_per_genome", "split_by_mag_id"}
    for slug, mode in raw.items():
        if mode not in allowed:
            raise RuntimeError(
                f"Invalid --layout-override for {slug}: {mode}. "
                f"Allowed values: {', '.join(sorted(allowed))}"
            )
    return raw


def regex_group_value(match: re.Match[str]) -> str | None:
    if "mag" in match.groupdict():
        value = match.group("mag")
        return value.strip() if value else None
    if match.lastindex:
        value = match.group(1)
        return value.strip() if value else None
    return None


def infer_mag_id(
    header: str,
    *,
    filename_hint: str = "",
    custom_regex: re.Pattern[str] | None = None,
) -> str | None:
    text = header.strip().lstrip(">")

    if custom_regex is not None:
        match = custom_regex.search(text)
        if match:
            value = regex_group_value(match)
            if value:
                return value

    key_match = re.search(
        r"(?:^|[\s|;,])(?:genome|genome_id|mag|mag_id|bin|bin_id|sample_bin)=([^|;,\s]+)",
        text,
        flags=re.IGNORECASE,
    )
    if key_match:
        return key_match.group(1)

    token = token_from_header(text)
    if not token:
        return None

    pipe_fields = [field for field in token.split("|") if field]
    if len(pipe_fields) > 1:
        for field in pipe_fields:
            if re.search(r"(?:MAG|bin|genome)", field, flags=re.IGNORECASE):
                return field

    contig_patterns = (
        r"^(.+?)(?:[._-]{1,3}(?:contig|ctg|scaffold|scaf|tig|unitig|seq|sequence)[._-]?\d.*)$",
        r"^(.+?)(?:[._-]{1,3}NODE[._-]?\d.*)$",
        r"^(.+?)(?:[._-]{1,3}k\d+_\d+.*)$",
        r"^(.+?)(?:[._-]{1,3}(?:length|cov)_[0-9].*)$",
    )
    for pattern in contig_patterns:
        match = re.match(pattern, token, flags=re.IGNORECASE)
        if match and match.group(1):
            candidate = match.group(1).strip("._-")
            if candidate and not re.match(r"^(?:NODE|contig|scaffold|ctg)\d*$", candidate, re.IGNORECASE):
                return candidate

    if filename_hint and re.match(r"^(?:NODE|contig|scaffold|ctg)[._-]?\d+", token, re.IGNORECASE):
        return filename_hint

    return None


def classify_layout_with_options(
    source: SourceFasta,
    summary: FastaSummary,
    *,
    dataset_regular_fastas: int,
    custom_regex: re.Pattern[str] | None,
    layout_override: str,
) -> Layout:
    if layout_override:
        return Layout(
            mode=layout_override,
            confidence="override",
            note="layout selected by user override",
        )

    if source.scope == "viral":
        return Layout(
            mode="record_per_genome",
            confidence="high",
            note="viral catalogue; each FASTA record is treated as one viral genome",
        )

    if source.archive_path is not None and source.sibling_fastas > 1:
        return Layout(
            mode="file_per_genome",
            confidence="high",
            note="multi-file archive; each FASTA member is treated as one MAG",
        )

    if source.archive_path is None and dataset_regular_fastas > 1:
        return Layout(
            mode="file_per_genome",
            confidence="high",
            note="multiple FASTA files in the dataset directory; each file is treated as one MAG",
        )

    if summary.records <= 1:
        return Layout(
            mode="file_per_genome",
            confidence="high",
            note="single-record FASTA",
        )

    inferred = [
        infer_mag_id(header, filename_hint=source.name_hint, custom_regex=custom_regex)
        for header in summary.headers
    ]
    known = [value for value in inferred if value]
    if known and len(known) == len(inferred):
        unique_known = set(known)
        if len(unique_known) == 1:
            return Layout(
                mode="file_per_genome",
                confidence="medium",
                note="multi-record FASTA headers share one inferred MAG id",
            )
        if len(unique_known) < len(known):
            return Layout(
                mode="split_by_mag_id",
                confidence="medium",
                note="multi-FASTA records have reusable inferred MAG ids",
            )
        if custom_regex is not None:
            return Layout(
                mode="split_by_mag_id",
                confidence="override",
                note="custom MAG-id regex matched each sampled record",
            )
        return Layout(
            mode="unknown_multi_fasta",
            confidence="low",
            note="each sampled record has a distinct inferred id, but MAG-level grouping is unproven",
        )

    return Layout(
        mode="unknown_multi_fasta",
        confidence="low",
        note="multi-record MAG FASTA lacks a reliable MAG id pattern in sampled headers",
    )


def deterministic_layout_without_content(
    source: SourceFasta,
    *,
    dataset_regular_fastas: int,
    layout_override: str,
) -> Layout | None:
    if layout_override:
        return Layout(
            mode=layout_override,
            confidence="override",
            note="layout selected by user override; content sampling skipped",
        )
    if source.scope == "viral":
        return None
    if source.archive_path is not None and source.sibling_fastas > 1:
        return Layout(
            mode="file_per_genome",
            confidence="high",
            note="multi-file archive; each FASTA member is treated as one MAG; content sampling skipped",
        )
    if source.archive_path is None and dataset_regular_fastas > 1:
        return Layout(
            mode="file_per_genome",
            confidence="high",
            note="multiple FASTA files in the dataset directory; each file is treated as one MAG; content sampling skipped",
        )
    return None


def discover_archive_fastas(
    *,
    dataset: DatasetMeta,
    archive_path: Path,
    root: Path,
    problems: list[Problem],
    logger: ProgressLogger,
    log_every: int,
) -> list[SourceFasta]:
    if is_unsupported_archive(archive_path):
        problems.append(
            Problem(
                "error",
                dataset.slug,
                display_path(archive_path, root),
                "unsupported-archive",
                "Unsupported archive compression; extract it before building cluster inputs.",
            )
        )
        return []

    archive_rel = display_path(archive_path, root)
    archive_size = human_bytes(archive_path.stat().st_size if archive_path.exists() else None)
    logger.log(f"{dataset.slug}: scanning archive members: {archive_rel} ({archive_size})")

    def record_archive_error(exc: BaseException, *, total_members: int, fasta_members: int) -> None:
        message = (
            f"{type(exc).__name__}: {exc}; scanned_entries={total_members}; "
            f"fasta_members_seen={fasta_members}. The archive is likely incomplete or corrupt; "
            "partial members from this archive were not added to clustering inputs."
        )
        logger.log(f"{dataset.slug}: archive scan failed for {archive_path.name}: {message}")
        problems.append(
            Problem(
                "error",
                dataset.slug,
                display_path(archive_path, root),
                "archive-read-failed",
                message,
            )
        )

    try:
        if archive_path.name.lower().endswith(".zip"):
            total_members = 0
            members: list[str] = []
            with zipfile.ZipFile(archive_path) as archive:
                for info in archive.infolist():
                    total_members += 1
                    if log_every > 0 and total_members % log_every == 0:
                        logger.log(
                            f"{dataset.slug}: {archive_path.name}: scanned {total_members} zip entries; "
                            f"FASTA members={len(members)}"
                        )
                    if not info.is_dir() and is_probably_fasta_name(Path(info.filename).name):
                        members.append(info.filename)
            logger.log(
                f"{dataset.slug}: {archive_path.name}: found {len(members)} FASTA member(s) "
                f"across {total_members} zip entries"
            )
            return [
                SourceFasta(
                    slug=dataset.slug,
                    dataset=dataset.dataset,
                    part=dataset.part,
                    scope=dataset.scope,
                    path=archive_path,
                    archive_path=archive_path,
                    archive_type="zip",
                    member_name=name,
                    sibling_fastas=len(members),
                )
                for name in members
            ]

        total_members = 0
        members: list[str] = []
        try:
            with tarfile.open(archive_path, mode="r|*") as archive:
                for member in archive:
                    total_members += 1
                    if log_every > 0 and total_members % log_every == 0:
                        logger.log(
                            f"{dataset.slug}: {archive_path.name}: scanned {total_members} tar entries; "
                            f"FASTA members={len(members)}"
                        )
                    if member.isfile() and is_probably_fasta_name(Path(member.name).name):
                        members.append(member.name)
        except (
            EOFError,
            OSError,
            gzip.BadGzipFile,
            lzma.LZMAError,
            tarfile.TarError,
            zlib.error,
        ) as exc:
            record_archive_error(exc, total_members=total_members, fasta_members=len(members))
            return []

        if members:
            logger.log(
                f"{dataset.slug}: {archive_path.name}: found {len(members)} FASTA member(s) "
                f"across {total_members} tar entries"
            )
            return [
                SourceFasta(
                    slug=dataset.slug,
                    dataset=dataset.dataset,
                    part=dataset.part,
                    scope=dataset.scope,
                    path=archive_path,
                    archive_path=archive_path,
                    archive_type="tar",
                    member_name=name,
                    sibling_fastas=len(members),
                )
                for name in members
            ]
        if total_members > 0:
            logger.log(
                f"{dataset.slug}: {archive_path.name}: found 0 FASTA members "
                f"across {total_members} tar entries"
            )
            return []
    except (
        EOFError,
        OSError,
        gzip.BadGzipFile,
        lzma.LZMAError,
        tarfile.TarError,
        zipfile.BadZipFile,
        zlib.error,
    ) as exc:
        record_archive_error(exc, total_members=0, fasta_members=0)
        return []

    problems.append(
        Problem(
            "warning",
            dataset.slug,
            display_path(archive_path, root),
            "archive-unrecognized",
            "File has an archive-looking suffix but was not readable as tar or zip.",
        )
    )
    return []

def discover_sources(
    *,
    root: Path,
    downloads_dir: Path,
    dataset_filter: set[str] | None,
    logger: ProgressLogger,
    log_every: int,
) -> tuple[list[SourceFasta], list[Problem], dict[str, DatasetMeta]]:
    metadata = discover_dataset_meta(root)
    problems: list[Problem] = []
    sources: list[SourceFasta] = []

    if not downloads_dir.exists():
        problems.append(
            Problem(
                "error",
                "",
                display_path(downloads_dir, root),
                "downloads-missing",
                "Downloads directory does not exist.",
            )
        )
        return sources, problems, metadata

    dataset_dirs = sorted(path for path in downloads_dir.iterdir() if path.is_dir())
    if dataset_filter:
        dataset_dirs = [path for path in dataset_dirs if path.name in dataset_filter]
    logger.log(f"discovering sources under {display_path(downloads_dir, root)}; datasets={len(dataset_dirs)}")

    for dataset_index, dataset_dir in enumerate(dataset_dirs, start=1):
        slug = dataset_dir.name
        dataset = metadata.get(slug, DatasetMeta(slug=slug, dataset=slug, part="unknown"))
        regular_fastas: list[Path] = []
        archive_paths: list[Path] = []
        logger.log(f"[{dataset_index}/{len(dataset_dirs)}] {slug}: walking files")

        walked = 0
        for path in sorted(dataset_dir.rglob("*")):
            walked += 1
            if not path.is_file() or should_ignore_file(path):
                if log_every > 0 and walked % log_every == 0:
                    logger.log(
                        f"{slug}: walked {walked} paths; FASTA files={len(regular_fastas)}; "
                        f"archives={len(archive_paths)}"
                    )
                continue
            if is_supported_archive(path) or is_unsupported_archive(path):
                archive_paths.append(path)
            elif is_probably_fasta_name(path.name):
                regular_fastas.append(path)
            if log_every > 0 and walked % log_every == 0:
                logger.log(
                    f"{slug}: walked {walked} paths; FASTA files={len(regular_fastas)}; "
                    f"archives={len(archive_paths)}"
                )

        logger.log(
            f"{slug}: file walk done; paths={walked}; FASTA files={len(regular_fastas)}; "
            f"archives={len(archive_paths)}"
        )

        for path in regular_fastas:
            sources.append(
                SourceFasta(
                    slug=dataset.slug,
                    dataset=dataset.dataset,
                    part=dataset.part,
                    scope=dataset.scope,
                    path=path,
                    sibling_fastas=len(regular_fastas),
                )
            )

        for path in archive_paths:
            problem_count_before = len(problems)
            members = discover_archive_fastas(
                dataset=dataset,
                archive_path=path,
                root=root,
                problems=problems,
                logger=logger,
                log_every=log_every,
            )
            had_new_error = any(problem.severity == "error" for problem in problems[problem_count_before:])
            if not members and not had_new_error:
                problems.append(
                    Problem(
                        "warning",
                        dataset.slug,
                        display_path(path, root),
                        "archive-without-fasta",
                        "No nucleotide FASTA members were found in this archive.",
                    )
                )
            sources.extend(members)
            logger.log(f"{slug}: total discovered FASTA sources={len(sources)}")

        if not regular_fastas and not archive_paths:
            problems.append(
                Problem(
                    "warning",
                    dataset.slug,
                    display_path(dataset_dir, root),
                    "no-fasta-source",
                    "No FASTA or supported archive files were found under this dataset directory.",
                )
            )

        logger.log(f"{slug}: discovery complete")

    return sources, problems, metadata


def inspect_sources(
    *,
    sources: list[SourceFasta],
    sample_records: int,
    full: bool,
    custom_regexes: dict[str, re.Pattern[str]],
    layout_overrides: dict[str, str],
    logger: ProgressLogger,
    log_every: int,
    sample_file_per_genome: bool,
) -> tuple[list[dict[str, str]], list[Problem], dict[str, Layout]]:
    problems: list[Problem] = []
    rows: list[dict[str, str]] = []
    layouts: dict[str, Layout] = {}
    regular_counts: dict[str, int] = {}
    for source in sources:
        if source.archive_path is None:
            regular_counts[source.slug] = regular_counts.get(source.slug, 0) + 1

    logger.log(f"inspecting FASTA layouts; sources={len(sources)}; full_count={full}")

    for source_index, source in enumerate(sources, start=1):
        if log_every > 0 and (source_index == 1 or source_index % log_every == 0 or source_index == len(sources)):
            logger.log(
                f"inspect progress: {source_index}/{len(sources)} sources; "
                f"current={source.slug}:{Path(source.member_name or source.path.name).name}"
            )
        key = source.label
        layout = deterministic_layout_without_content(
            source,
            dataset_regular_fastas=regular_counts.get(source.slug, 0),
            layout_override=layout_overrides.get(source.slug, ""),
        )
        summary = FastaSummary()
        sampled = False
        if layout is None or sample_file_per_genome or full:
            try:
                summary = summarize_fasta(source, sample_records=sample_records, full=full)
                sampled = True
            except (OSError, gzip.BadGzipFile, lzma.LZMAError, EOFError) as exc:
                problems.append(Problem("error", source.slug, source.label, "fasta-read-failed", str(exc)))
                continue

            if summary.records == 0:
                problems.append(Problem("error", source.slug, source.label, "empty-fasta", "No FASTA records found."))
                continue

            layout = classify_layout_with_options(
                source,
                summary,
                dataset_regular_fastas=regular_counts.get(source.slug, 0),
                custom_regex=custom_regexes.get(source.slug),
                layout_override=layout_overrides.get(source.slug, ""),
            )
        layouts[key] = layout
        if layout.mode == "unknown_multi_fasta":
            problems.append(
                Problem(
                    "error",
                    source.slug,
                    source.label,
                    "ambiguous-mag-multifasta",
                    layout.note,
                )
            )
        if source.scope == "viral" and summary.records > 0:
            note = "viral record-per-genome"
        else:
            note = layout.note
        rows.append(
            {
                "slug": source.slug,
                "dataset": source.dataset,
                "part": source.part,
                "scope": source.scope,
                "source": source.label,
                "archive_member": source.member_name,
                "layout": layout.mode,
                "confidence": layout.confidence,
                "records_observed": str(summary.records) if sampled else "",
                "bases_observed": str(summary.bases) if sampled else "",
                "sampled_records": str(summary.sampled_records) if sampled else "0",
                "truncated": "yes" if summary.truncated else "no",
                "first_header": summary.first_header[:240],
                "note": note,
            }
        )
    return rows, problems, layouts


def ensure_clean_dir(path: Path, *, force: bool) -> None:
    if path.exists():
        if not force:
            raise RuntimeError(f"Output directory already exists; rerun with --force: {path}")
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_source_to_plain_fasta(source: SourceFasta, output: Path) -> tuple[int, int]:
    output.parent.mkdir(parents=True, exist_ok=True)
    records = 0
    bases = 0
    saw_header = False
    with source_reader(source) as handle, output.open("wb") as out:
        for raw_line in handle:
            line = raw_line.rstrip(b"\r\n")
            if not line:
                continue
            if line.startswith(b">"):
                records += 1
                saw_header = True
                out.write(line + b"\n")
            elif saw_header:
                bases += len(re.sub(rb"\s+", b"", line))
                out.write(line + b"\n")
    return records, bases


def write_split_by_record(
    source: SourceFasta,
    out_dir: Path,
    *,
    id_prefix: str,
) -> list[MagRow]:
    rows: list[MagRow] = []
    out_dir.mkdir(parents=True, exist_ok=True)
    current: io.BufferedWriter | None = None
    current_bp = 0
    current_records = 0
    current_id = ""
    current_path: Path | None = None
    seen: set[str] = set()

    def close_current() -> None:
        nonlocal current, current_bp, current_records, current_id, current_path
        if current is None or current_path is None:
            return
        current.close()
        rows.append(
            MagRow(
                slug=source.slug,
                dataset=source.dataset,
                scope=source.scope,
                genome_id=current_id,
                path=current_path,
                source=source.label,
                mode="record_per_genome",
                seq_count=current_records,
                bp=current_bp,
            )
        )
        current = None
        current_bp = 0
        current_records = 0
        current_id = ""
        current_path = None

    with source_reader(source) as handle:
        for raw_line in handle:
            line = raw_line.rstrip(b"\r\n")
            if not line:
                continue
            if line.startswith(b">"):
                close_current()
                header = line[1:].decode("utf-8", errors="replace").strip()
                base_id = token_from_header(header) or header
                genome_id = f"{id_prefix}{base_id}" if id_prefix else base_id
                if genome_id in seen:
                    genome_id = f"{genome_id}|{hashlib.sha1(header.encode()).hexdigest()[:10]}"
                seen.add(genome_id)
                current_id = genome_id
                current_path = out_dir / stable_fasta_name(genome_id)
                current = current_path.open("wb")
                current.write(b">" + header.encode("utf-8", errors="replace") + b"\n")
                current_records = 1
                current_bp = 0
                continue
            if current is None:
                continue
            current_bp += len(re.sub(rb"\s+", b"", line))
            current.write(line + b"\n")
    close_current()
    return rows


def write_split_by_mag_id(
    source: SourceFasta,
    out_dir: Path,
    *,
    custom_regex: re.Pattern[str] | None,
) -> tuple[list[MagRow], list[Problem]]:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows_by_id: dict[str, MagRow] = {}
    problems: list[Problem] = []
    current: io.BufferedWriter | None = None
    current_id = ""
    current_path: Path | None = None

    def close_current() -> None:
        nonlocal current
        if current is not None:
            current.close()
            current = None

    with source_reader(source) as handle:
        for raw_line in handle:
            line = raw_line.rstrip(b"\r\n")
            if not line:
                continue
            if line.startswith(b">"):
                close_current()
                header = line[1:].decode("utf-8", errors="replace").strip()
                mag_id = infer_mag_id(
                    header,
                    filename_hint=source.name_hint,
                    custom_regex=custom_regex,
                )
                if not mag_id:
                    problems.append(
                        Problem(
                            "error",
                            source.slug,
                            source.label,
                            "header-without-mag-id",
                            f"Could not infer MAG id from header: {header[:240]}",
                        )
                    )
                    current_id = ""
                    current_path = None
                    continue
                current_id = mag_id
                row = rows_by_id.get(mag_id)
                if row is None:
                    current_path = out_dir / stable_fasta_name(mag_id)
                    row = MagRow(
                        slug=source.slug,
                        dataset=source.dataset,
                        scope=source.scope,
                        genome_id=mag_id,
                        path=current_path,
                        source=source.label,
                        mode="split_by_mag_id",
                        seq_count=0,
                        bp=0,
                    )
                    rows_by_id[mag_id] = row
                    current = current_path.open("wb")
                else:
                    current_path = row.path
                    current = current_path.open("ab")
                current.write(b">" + header.encode("utf-8", errors="replace") + b"\n")
                row.seq_count = int(row.seq_count) + 1
                continue
            if current is None or not current_id:
                continue
            row = rows_by_id[current_id]
            row.bp = int(row.bp) + len(re.sub(rb"\s+", b"", line))
            current.write(line + b"\n")
    close_current()
    return list(rows_by_id.values()), problems


def process_mag_source(
    source: SourceFasta,
    layout: Layout,
    *,
    materialized_dir: Path,
    copy_compressed: bool,
    custom_regex: re.Pattern[str] | None,
) -> tuple[list[MagRow], list[Problem]]:
    out_dir = materialized_dir / source.slug
    if layout.mode == "file_per_genome":
        if source.archive_path is None and not (copy_compressed and is_compressed_file(source.path.name)):
            genome_id = strip_fasta_suffix(source.path.name)
            return [
                MagRow(
                    slug=source.slug,
                    dataset=source.dataset,
                    scope=source.scope,
                    genome_id=genome_id,
                    path=source.path,
                    source=source.label,
                    mode="file_per_genome",
                )
            ], []

        genome_id = strip_fasta_suffix(Path(source.member_name).name if source.member_name else source.path.name)
        output = out_dir / stable_fasta_name(genome_id)
        seq_count, bp = copy_source_to_plain_fasta(source, output)
        return [
            MagRow(
                slug=source.slug,
                dataset=source.dataset,
                scope=source.scope,
                genome_id=genome_id,
                path=output,
                source=source.label,
                mode="file_per_genome",
                seq_count=seq_count,
                bp=bp,
            )
        ], []

    if layout.mode == "record_per_genome":
        return write_split_by_record(source, out_dir, id_prefix=""), []

    if layout.mode == "split_by_mag_id":
        return write_split_by_mag_id(source, out_dir, custom_regex=custom_regex)

    return [], [
        Problem(
            "error",
            source.slug,
            source.label,
            "unmaterialized-layout",
            f"Cannot materialize layout: {layout.mode}",
        )
    ]


def append_viral_source(
    source: SourceFasta,
    *,
    out_fasta: io.BufferedWriter,
    seen_ids: set[str],
    viral_fasta_path: Path,
) -> tuple[list[MagRow], list[Problem]]:
    rows: list[MagRow] = []
    problems: list[Problem] = []
    current_id = ""
    current_bp = 0
    current_records = 0

    def close_current() -> None:
        nonlocal current_id, current_bp, current_records
        if not current_id:
            return
        rows.append(
            MagRow(
                slug=source.slug,
                dataset=source.dataset,
                scope=source.scope,
                genome_id=current_id,
                path=viral_fasta_path,
                source=source.label,
                mode="viral_record_per_genome",
                seq_count=current_records,
                bp=current_bp,
            )
        )
        current_id = ""
        current_bp = 0
        current_records = 0

    with source_reader(source) as handle:
        for raw_line in handle:
            line = raw_line.rstrip(b"\r\n")
            if not line:
                continue
            if line.startswith(b">"):
                close_current()
                header = line[1:].decode("utf-8", errors="replace").strip()
                token = sanitize_id(token_from_header(header) or header, fallback="viral_genome")
                viral_id = f"{source.slug}|{token}"
                if viral_id in seen_ids:
                    viral_id = f"{viral_id}|{hashlib.sha1(header.encode()).hexdigest()[:10]}"
                seen_ids.add(viral_id)
                current_id = viral_id
                current_records = 1
                current_bp = 0
                out_fasta.write(f">{viral_id} source={source.slug}\n".encode("utf-8"))
                continue
            if not current_id:
                problems.append(
                    Problem(
                        "warning",
                        source.slug,
                        source.label,
                        "viral-sequence-before-header",
                        "Ignored sequence text before the first FASTA header.",
                    )
                )
                continue
            current_bp += len(re.sub(rb"\s+", b"", line))
            out_fasta.write(line + b"\n")
    close_current()
    return rows, problems


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_problems(path: Path, problems: list[Problem]) -> None:
    rows = [
        {
            "severity": problem.severity,
            "slug": problem.slug,
            "source": problem.source,
            "code": problem.code,
            "message": problem.message,
        }
        for problem in problems
    ]
    write_tsv(path, rows, ["severity", "slug", "source", "code", "message"])


def write_mag_rows(path: Path, rows: list[MagRow], *, root: Path) -> None:
    write_tsv(
        path,
        [
            {
                "slug": row.slug,
                "dataset": row.dataset,
                "scope": row.scope,
                "genome_id": row.genome_id,
                "path": str(row.path) if not row.path.is_absolute() else display_path(row.path, root),
                "source": row.source,
                "mode": row.mode,
                "seq_count": str(row.seq_count),
                "bp": str(row.bp),
            }
            for row in rows
        ],
        ["slug", "dataset", "scope", "genome_id", "path", "source", "mode", "seq_count", "bp"],
    )


def write_filelist(path: Path, rows: list[MagRow], *, relative_to: Path | None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(output_path(row.path, relative_to=relative_to) + "\n")


def command_inspect(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    downloads_dir = Path(args.downloads_dir).resolve()
    out_dir = Path(args.out_dir).resolve()
    dataset_filter = set(args.datasets.split(",")) if args.datasets else None
    custom_regexes = compile_mag_id_regexes(args.mag_id_regex)
    layout_overrides = parse_layout_overrides(args.layout_override)
    logger = ProgressLogger(quiet=args.quiet)
    sources, discover_problems, _ = discover_sources(
        root=root,
        downloads_dir=downloads_dir,
        dataset_filter=dataset_filter,
        logger=logger,
        log_every=args.log_every,
    )
    rows, inspect_problems, _ = inspect_sources(
        sources=sources,
        sample_records=args.sample_records,
        full=args.full_count,
        custom_regexes=custom_regexes,
        layout_overrides=layout_overrides,
        logger=logger,
        log_every=args.log_every,
        sample_file_per_genome=args.sample_file_per_genome,
    )
    problems = discover_problems + inspect_problems

    write_tsv(
        out_dir / "inspect.tsv",
        rows,
        [
            "slug",
            "dataset",
            "part",
            "scope",
            "source",
            "archive_member",
            "layout",
            "confidence",
            "records_observed",
            "bases_observed",
            "sampled_records",
            "truncated",
            "first_header",
            "note",
        ],
    )
    write_problems(out_dir / "problems.tsv", problems)
    print(f"Sources inspected: {len(rows)}")
    print(f"Problems: {len(problems)}")
    print(f"Inspect table: {display_path(out_dir / 'inspect.tsv', root)}")
    print(f"Problems table: {display_path(out_dir / 'problems.tsv', root)}")
    if args.fail_on_problems and any(problem.severity == "error" for problem in problems):
        return 1
    return 0


def command_build(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    downloads_dir = Path(args.downloads_dir).resolve()
    out_dir = Path(args.out_dir).resolve()
    dataset_filter = set(args.datasets.split(",")) if args.datasets else None
    relative_to = Path(args.relative_to).resolve() if args.relative_to else None
    custom_regexes = compile_mag_id_regexes(args.mag_id_regex)
    layout_overrides = parse_layout_overrides(args.layout_override)
    logger = ProgressLogger(quiet=args.quiet)
    ensure_clean_dir(out_dir, force=args.force)

    sources, discover_problems, _ = discover_sources(
        root=root,
        downloads_dir=downloads_dir,
        dataset_filter=dataset_filter,
        logger=logger,
        log_every=args.log_every,
    )
    inspect_rows, inspect_problems, layouts = inspect_sources(
        sources=sources,
        sample_records=args.sample_records,
        full=args.full_count,
        custom_regexes=custom_regexes,
        layout_overrides=layout_overrides,
        logger=logger,
        log_every=args.log_every,
        sample_file_per_genome=args.sample_file_per_genome,
    )
    all_problems = discover_problems + inspect_problems

    write_tsv(
        out_dir / "inspect.tsv",
        inspect_rows,
        [
            "slug",
            "dataset",
            "part",
            "scope",
            "source",
            "archive_member",
            "layout",
            "confidence",
            "records_observed",
            "bases_observed",
            "sampled_records",
            "truncated",
            "first_header",
            "note",
        ],
    )

    materialized_dir = out_dir / "materialized"
    rabbit_dir = out_dir / "rabbittclust"
    vclust_dir = out_dir / "vclust"
    rabbit_dir.mkdir(parents=True, exist_ok=True)
    vclust_dir.mkdir(parents=True, exist_ok=True)

    mag_rows: list[MagRow] = []
    viral_rows: list[MagRow] = []

    for source in sources:
        layout = layouts.get(source.label)
        if layout is None:
            continue
        if source.scope == "viral":
            continue
        if args.log_every > 0 and (len(mag_rows) == 0 or len(mag_rows) % args.log_every == 0):
            logger.log(f"materializing MAG source: {source.slug}:{Path(source.member_name or source.path.name).name}")
        rows, problems = process_mag_source(
            source,
            layout,
            materialized_dir=materialized_dir,
            copy_compressed=True,
            custom_regex=custom_regexes.get(source.slug),
        )
        mag_rows.extend(rows)
        all_problems.extend(problems)

    viral_sources = [source for source in sources if source.scope == "viral" and source.label in layouts]
    viral_fasta = vclust_dir / "viral_genomes.fna"
    seen_viral_ids: set[str] = set()
    with viral_fasta.open("wb") as handle:
        for source in viral_sources:
            logger.log(f"appending viral source: {source.slug}:{Path(source.member_name or source.path.name).name}")
            rows, problems = append_viral_source(
                source,
                out_fasta=handle,
                seen_ids=seen_viral_ids,
                viral_fasta_path=viral_fasta,
            )
            viral_rows.extend(rows)
            all_problems.extend(problems)

    if not viral_rows:
        viral_fasta.unlink(missing_ok=True)

    by_slug: dict[str, list[MagRow]] = {}
    for row in mag_rows:
        by_slug.setdefault(row.slug, []).append(row)
    for slug, rows in sorted(by_slug.items()):
        write_filelist(rabbit_dir / f"{slug}.list", rows, relative_to=relative_to)

    write_filelist(
        rabbit_dir / "all_bacterial_archaeal_mags.list",
        sorted(mag_rows, key=lambda row: (row.slug, row.genome_id)),
        relative_to=relative_to,
    )
    write_mag_rows(out_dir / "mags.tsv", sorted(mag_rows, key=lambda row: (row.slug, row.genome_id)), root=root)
    write_mag_rows(out_dir / "viral_genomes.tsv", viral_rows, root=root)
    write_problems(out_dir / "problems.tsv", all_problems)

    print(f"Bacterial/archaeal MAGs: {len(mag_rows)}")
    print(f"Viral genomes: {len(viral_rows)}")
    print(f"RabbitTClust list: {display_path(rabbit_dir / 'all_bacterial_archaeal_mags.list', root)}")
    if viral_rows:
        print(f"vclust FASTA: {display_path(viral_fasta, root)}")
    print(f"Problems table: {display_path(out_dir / 'problems.tsv', root)}")

    if args.fail_on_problems and any(problem.severity == "error" for problem in all_problems):
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build RabbitTClust and vclust genome-level inputs from downloads/<slug>/."
    )
    parser.add_argument("--root", default=str(ROOT_DIR), help="Repository root.")
    parser.add_argument(
        "--downloads-dir",
        default=str(DEFAULT_DOWNLOADS_DIR),
        help="Directory containing downloads/<slug> dataset directories.",
    )
    parser.add_argument(
        "--out-dir",
        default=str(DEFAULT_OUT_DIR),
        help="Output directory for inspect tables, filelists, and materialized FASTA files.",
    )
    parser.add_argument(
        "--datasets",
        default="",
        help="Comma-separated slug allowlist. Defaults to all dataset directories under downloads.",
    )
    parser.add_argument(
        "--sample-records",
        type=int,
        default=2000,
        help="Number of FASTA headers to sample per source during layout inference.",
    )
    parser.add_argument(
        "--sample-file-per-genome",
        action="store_true",
        help=(
            "Also read FASTA content for sources whose layout is already deterministically "
            "file_per_genome. By default these are not sampled, which keeps inspect usable "
            "for very large tar archives and per-MAG file trees."
        ),
    )
    parser.add_argument(
        "--full-count",
        action="store_true",
        help="Scan entire FASTA sources during inspection instead of stopping after the sample.",
    )
    parser.add_argument(
        "--log-every",
        type=int,
        default=1000,
        help="Print progress every N walked paths, archive members, or inspected sources. Use 0 to disable interval logs.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress logs; summary output is still printed.",
    )
    parser.add_argument(
        "--fail-on-problems",
        action="store_true",
        help="Return nonzero when any error-level problem is reported.",
    )
    parser.add_argument(
        "--mag-id-regex",
        action="append",
        default=[],
        metavar="SLUG=REGEX",
        help=(
            "Custom MAG id extraction regex for ambiguous multi-FASTA datasets. "
            "Use a named group (?P<mag>...) or the first capture group. Repeatable."
        ),
    )
    parser.add_argument(
        "--layout-override",
        action="append",
        default=[],
        metavar="SLUG=MODE",
        help=(
            "Override layout inference for a dataset. MODE is file_per_genome, "
            "record_per_genome, or split_by_mag_id. Repeatable."
        ),
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    inspect_parser = subparsers.add_parser("inspect", help="Inspect downloaded datasets without materializing inputs.")
    inspect_parser.set_defaults(func=command_inspect)

    build_parser_ = subparsers.add_parser("build", help="Materialize inputs and write clustering filelists.")
    build_parser_.add_argument(
        "--force",
        action="store_true",
        help="Replace the output directory if it already exists.",
    )
    build_parser_.add_argument(
        "--relative-to",
        default="",
        help="Write filelist paths relative to this directory. Defaults to absolute paths.",
    )
    build_parser_.set_defaults(func=command_build)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
