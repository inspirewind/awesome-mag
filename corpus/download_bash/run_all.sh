#!/usr/bin/env bash
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
LOG_DIR="${ROOT_DIR}/corpus/logs"

usage() {
  cat <<'USAGE'
Usage:
  bash corpus/download_bash/run_all.sh [-j N] [part_dir ...]

Examples:
  bash corpus/download_bash/run_all.sh
  bash corpus/download_bash/run_all.sh -j 2 part1_recommended_direct
  bash corpus/download_bash/run_all.sh -j 6 part1_recommended_direct part3_viral_direct
  bash corpus/download_bash/run_all.sh -j 2 part4_hard_datasets

By default this runs all scripts in:
  part1_recommended_direct
  part2_large_or_caveated_direct
  part3_viral_direct
USAGE
}

max_jobs="${MAX_JOBS:-3}"
parts=()

while (($# > 0)); do
  case "$1" in
    -j|--jobs)
      if (($# < 2)); then
        echo "Missing value after $1" >&2
        exit 2
      fi
      max_jobs="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      parts+=("$1")
      shift
      ;;
  esac
done

if ! [[ "${max_jobs}" =~ ^[0-9]+$ ]] || ((max_jobs < 1)); then
  echo "Job count must be a positive integer: ${max_jobs}" >&2
  exit 2
fi

if ((${#parts[@]} == 0)); then
  parts=(
    "part1_recommended_direct"
    "part2_large_or_caveated_direct"
    "part3_viral_direct"
  )
fi

mkdir -p "${LOG_DIR}"

scripts=()
for part in "${parts[@]}"; do
  part_dir="${SCRIPT_DIR}/${part}"
  if [[ ! -d "${part_dir}" ]]; then
    echo "Part directory does not exist: ${part}" >&2
    exit 2
  fi

  shopt -s nullglob
  for script in "${part_dir}"/*.sh; do
    scripts+=("${script}")
  done
  shopt -u nullglob
done

if ((${#scripts[@]} == 0)); then
  echo "No scripts found."
  exit 0
fi

running_jobs() {
  jobs -rp | wc -l | tr -d ' '
}

wait_for_slot() {
  while (("$(running_jobs)" >= max_jobs)); do
    if ! wait -n; then
      failures=$((failures + 1))
    fi
  done
}

failures=0

echo "Starting ${#scripts[@]} scripts with max parallel jobs: ${max_jobs}"
echo "Logs: corpus/logs/"

for script in "${scripts[@]}"; do
  wait_for_slot

  slug="$(awk -F: '/^# slug:/ { value=$2; sub(/^[ \t]+/, "", value); print value; exit }' "${script}")"
  if [[ -z "${slug}" ]]; then
    slug="$(basename "${script}" .sh)"
  fi

  log="${LOG_DIR}/${slug}.log"
  rel_script="${script#${ROOT_DIR}/}"
  rel_log="${log#${ROOT_DIR}/}"

  echo "START ${rel_script} -> ${rel_log}"
  (
    printf 'script=%s\n' "${rel_script}"
    printf 'started_at=%s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
    bash "${script}"
  ) > "${log}" 2>&1 &
done

while (("$(running_jobs)" > 0)); do
  if ! wait -n; then
    failures=$((failures + 1))
  fi
done

echo "All launched jobs finished. Failures: ${failures}"
echo "Run status summary with: python3 corpus/build_status.py"

if ((failures > 0)); then
  exit 1
fi
