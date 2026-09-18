#!/usr/bin/env bash
set -euo pipefail
: "${PROJECT_ID:?Set PROJECT_ID, e.g. PROJECT_ID=deendirectory-93c7e}"
REGION="${REGION:-us-east4}"
SERVICE_NAME="${SERVICE_NAME:-investing-os-post-open}"

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

if [[ "$(git branch --show-current)" != "research/tori-v1-2-replication" ]]; then
  echo "ERROR: switch to research/tori-v1-2-replication first." >&2
  exit 2
fi

python3 -m venv .venv-tori-replication
source .venv-tori-replication/bin/activate
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt pandas numpy

mkdir -p research/results
if ! grep -qxF 'research/data/tori_checksum/' .git/info/exclude 2>/dev/null; then
  echo 'research/data/tori_checksum/' >> .git/info/exclude
fi
if ! grep -qxF '.venv-tori-replication/' .git/info/exclude 2>/dev/null; then
  echo '.venv-tori-replication/' >> .git/info/exclude
fi

python research/run_tori_checksum_gcp.py \
  --project "$PROJECT_ID" \
  --region "$REGION" \
  --service "$SERVICE_NAME" \
  --push-results
