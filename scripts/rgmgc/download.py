#!/usr/bin/env python3
"""Download RGMGC MAG genome FASTA files from NCBI Assembly."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lib.corpus_download import DownloadError, DownloadItem, add_common_arguments, main_wrapper, run_manifest_workflow


SLUG = "rgmgc"
DATASET = "RGMGC"
BIOPROJECT = "PRJNA657473"
EXPECTED_MAG_COUNT = 10_373
SIZE = "10,373 per-MAG NCBI Assembly genome FASTA files; total size not precomputed"
NOTE = (
    "Enumerates NCBI Assembly records for BioProject PRJNA657473 and downloads "
    "GenBank genome FASTA files only; skips raw reads, RGMGC gene catalogs, and "
    "Figshare protein/ORF bundles."
)
USER_AGENT = "awesome-mag/0.1 (+https://github.com/)"
ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"


def ncbi_common_params(args: argparse.Namespace) -> dict[str, str]:
    params = {"tool": "awesome-mag"}
    email = args.email or os.environ.get("NCBI_EMAIL", "")
    api_key = args.api_key or os.environ.get("NCBI_API_KEY", "")
    if email:
        params["email"] = email
    if api_key:
        params["api_key"] = api_key
    return params


def fetch_json(
    url: str,
    params: dict[str, str],
    *,
    retries: int,
    method: str = "GET",
) -> dict:
    encoded = urllib.parse.urlencode(params).encode("utf-8")
    if method == "GET":
        request_url = f"{url}?{encoded.decode('utf-8')}"
        data = None
    elif method == "POST":
        request_url = url
        data = encoded
    else:
        raise AssertionError(f"unsupported method: {method}")

    headers = {
        "Accept": "application/json, */*",
        "User-Agent": USER_AGENT,
    }
    if method == "POST":
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    attempts = max(1, retries + 1)
    for attempt in range(1, attempts + 1):
        request = urllib.request.Request(request_url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            if attempt < attempts and exc.code in {429, 500, 502, 503, 504}:
                time.sleep(min(30, 2 * attempt))
                continue
            raise DownloadError(f"NCBI request failed: {exc.code} {exc.reason}\n{body[:1000]}") from exc
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            if attempt < attempts:
                time.sleep(min(30, 2 * attempt))
                continue
            raise DownloadError(f"NCBI request failed: {exc}") from exc

    raise AssertionError("unreachable")


def fetch_assembly_uids(args: argparse.Namespace) -> list[str]:
    params = {
        **ncbi_common_params(args),
        "db": "assembly",
        "term": f"{BIOPROJECT}[BioProject]",
        "retmode": "json",
        "retmax": str(args.retmax),
    }
    payload = fetch_json(ESEARCH_URL, params, retries=args.retries)
    result = payload.get("esearchresult", {})
    count = int(result.get("count", "0"))
    uids = [str(uid) for uid in result.get("idlist", [])]
    if args.expected_count and count != args.expected_count:
        raise DownloadError(f"Unexpected RGMGC NCBI assembly count: {count} != {args.expected_count}")
    if len(uids) != count:
        raise DownloadError(
            f"NCBI ESearch returned {len(uids)} ids but reported count={count}; "
            "increase --retmax if this happens."
        )
    return uids


def chunks(values: list[str], size: int) -> list[list[str]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


def field(record: dict, *names: str) -> str:
    lower = {str(key).lower(): value for key, value in record.items()}
    for name in names:
        value = lower.get(name.lower())
        if value not in (None, ""):
            return str(value)
    return ""


def fetch_assembly_records(args: argparse.Namespace, uids: list[str]) -> list[dict]:
    if args.chunk_size <= 0:
        raise DownloadError("--chunk-size must be positive")
    records: list[dict] = []
    uid_chunks = chunks(uids, args.chunk_size)
    for index, uid_chunk in enumerate(uid_chunks, start=1):
        params = {
            **ncbi_common_params(args),
            "db": "assembly",
            "id": ",".join(uid_chunk),
            "retmode": "json",
        }
        payload = fetch_json(ESUMMARY_URL, params, retries=args.retries, method="POST")
        result = payload.get("result", {})
        returned_uids = [str(uid) for uid in result.get("uids", [])]
        if len(returned_uids) != len(uid_chunk):
            raise DownloadError(
                f"NCBI ESummary chunk {index}/{len(uid_chunks)} returned "
                f"{len(returned_uids)} records for {len(uid_chunk)} ids"
            )
        for uid in returned_uids:
            record = result.get(uid)
            if not isinstance(record, dict):
                raise DownloadError(f"NCBI ESummary response is missing uid {uid}")
            records.append(record)
        if args.log_every and (index == 1 or index == len(uid_chunks) or len(records) % args.log_every == 0):
            print(
                f"[ncbi] esummary chunks={index}/{len(uid_chunks)}; records={len(records)}",
                flush=True,
            )
        if index < len(uid_chunks) and args.sleep > 0:
            time.sleep(args.sleep)
    return records


def genome_url_from_ftp_path(ftp_path: str) -> str:
    ftp_path = ftp_path.rstrip("/")
    if not ftp_path:
        return ""
    basename = ftp_path.rsplit("/", 1)[-1]
    if ftp_path.startswith("ftp://"):
        base_url = "https://" + ftp_path[len("ftp://") :]
    else:
        base_url = ftp_path
    return f"{base_url}/{basename}_genomic.fna.gz"


def clean_cell(value: str) -> str:
    return " ".join(value.split())


def output_name(url: str, accession: str, seen: set[str]) -> str:
    leaf = Path(urllib.parse.urlparse(url).path).name
    if not leaf:
        leaf = f"{accession}_genomic.fna.gz"
    if leaf not in seen:
        seen.add(leaf)
        return leaf
    candidate = f"{accession}_{leaf}"
    if candidate in seen:
        raise DownloadError(f"Duplicate RGMGC output filename after accession disambiguation: {candidate}")
    seen.add(candidate)
    return candidate


def build_items(root: Path, records: list[dict]) -> tuple[list[DownloadItem], list[dict[str, str]]]:
    output_dir = root / "downloads" / SLUG / "assemblies"
    items: list[DownloadItem] = []
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    missing: list[str] = []

    for record in records:
        uid = field(record, "uid")
        accession = field(record, "assemblyaccession", "AssemblyAccession")
        assembly_name = field(record, "assemblyname", "AssemblyName")
        ftp_path = field(record, "ftppath_genbank", "FtpPath_GenBank") or field(
            record,
            "ftppath_refseq",
            "FtpPath_RefSeq",
        )
        if not accession or not ftp_path:
            missing.append(uid or accession or "<unknown>")
            continue
        url = genome_url_from_ftp_path(ftp_path)
        name = output_name(url, accession, seen)
        output = output_dir / name
        items.append(DownloadItem(url=url, output=output))
        rows.append(
            {
                "uid": uid,
                "accession": accession,
                "assembly_name": assembly_name,
                "biosample": field(record, "biosampleaccn", "BioSampleAccn"),
                "organism": clean_cell(field(record, "organism", "Organism")),
                "ftp_path": ftp_path,
                "url": url,
                "output": str(Path("assemblies") / name),
            }
        )

    if missing:
        preview = ", ".join(missing[:20])
        suffix = "" if len(missing) <= 20 else f", ... {len(missing) - 20} more"
        raise DownloadError(f"{len(missing)} RGMGC assembly records are missing accession or FTP path: {preview}{suffix}")
    return items, rows


def write_ncbi_manifest(root: Path, rows: list[dict[str, str]]) -> None:
    path = root / "downloads" / SLUG / "ncbi_assemblies_manifest.tsv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("uid", "accession", "assembly_name", "biosample", "organism", "ftp_path", "url", "output"),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    add_common_arguments(parser, jobs=8, connections=2)
    parser.add_argument(
        "--expected-count",
        type=int,
        default=EXPECTED_MAG_COUNT,
        help="Expected number of NCBI Assembly records. Defaults to 10,373.",
    )
    parser.add_argument(
        "--retmax",
        type=int,
        default=20_000,
        help="NCBI ESearch retmax. Must be greater than the expected assembly count.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=500,
        help="Number of assembly UIDs per NCBI ESummary request.",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.34,
        help="Seconds to sleep between NCBI ESummary requests. Keep nonzero unless using an API key.",
    )
    parser.add_argument(
        "--email",
        default="",
        help="Optional NCBI contact email. Can also be set with NCBI_EMAIL.",
    )
    parser.add_argument(
        "--api-key",
        default="",
        help="Optional NCBI API key. Can also be set with NCBI_API_KEY.",
    )
    parser.add_argument(
        "--log-every",
        type=int,
        default=2_000,
        help="Print NCBI enumeration progress every N records; set 0 to disable.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).expanduser().resolve()

    uids = fetch_assembly_uids(args)
    print(f"[ncbi] esearch BioProject={BIOPROJECT}; assembly_records={len(uids)}", flush=True)
    records = fetch_assembly_records(args, uids)
    if args.expected_count and len(records) != args.expected_count:
        raise DownloadError(f"Unexpected RGMGC assembly record count: {len(records)} != {args.expected_count}")

    items, rows = build_items(root, records)
    if args.expected_count and len(items) != args.expected_count:
        raise DownloadError(f"Unexpected RGMGC genome FASTA URL count: {len(items)} != {args.expected_count}")
    write_ncbi_manifest(root, rows)

    return run_manifest_workflow(
        root=root,
        slug=SLUG,
        dataset=DATASET,
        size=SIZE,
        items=items,
        downloader=args.downloader,
        jobs=args.jobs,
        connections=args.connections,
        retries=args.retries,
        verify=args.verify_md5,
        note=NOTE,
        manifest_only=args.manifest_only,
    )


if __name__ == "__main__":
    raise SystemExit(main_wrapper(main))
