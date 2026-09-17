#!/usr/bin/env bash
set -euo pipefail

REGION="${REGION:-us-east4}"
SERVICE_NAME="${SERVICE_NAME:-investing-os-post-open}"
TIME_ZONE="${TIME_ZONE:-America/New_York}"
COLLECTOR_JOB="${COLLECTOR_JOB:-investing-os-bar-collector}"
FINALIZER_JOB="${FINALIZER_JOB:-investing-os-bar-finalizer}"
SCHEDULER_SA_NAME="${SCHEDULER_SA_NAME:-investing-os-scheduler}"
PROJECT_ID="${PROJECT_ID:-$(gcloud config get-value project 2>/dev/null)}"

if [[ -z "${PROJECT_ID}" || "${PROJECT_ID}" == "(unset)" ]]; then
  echo "PROJECT_ID is not set and gcloud has no active project." >&2
  exit 1
fi

SERVICE_URL="$(gcloud run services describe "${SERVICE_NAME}" \
  --project="${PROJECT_ID}" \
  --region="${REGION}" \
  --format='value(status.url)')"

if [[ -z "${SERVICE_URL}" ]]; then
  echo "Could not resolve Cloud Run URL for ${SERVICE_NAME}." >&2
  exit 1
fi

SCHEDULER_EMAIL="${SCHEDULER_SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
COLLECT_URL="${SERVICE_URL}/collect"

# Ensure the existing scheduler service account can invoke Cloud Run.
gcloud run services add-iam-policy-binding "${SERVICE_NAME}" \
  --project="${PROJECT_ID}" \
  --region="${REGION}" \
  --member="serviceAccount:${SCHEDULER_EMAIL}" \
  --role="roles/run.invoker" >/dev/null

upsert_job() {
  local job_name="$1"
  local schedule="$2"

  if gcloud scheduler jobs describe "${job_name}" \
      --project="${PROJECT_ID}" \
      --location="${REGION}" >/dev/null 2>&1; then
    gcloud scheduler jobs update http "${job_name}" \
      --project="${PROJECT_ID}" \
      --location="${REGION}" \
      --schedule="${schedule}" \
      --time-zone="${TIME_ZONE}" \
      --uri="${COLLECT_URL}" \
      --http-method=POST \
      --message-body='{}' \
      --update-headers="Content-Type=application/json" \
      --oidc-service-account-email="${SCHEDULER_EMAIL}" \
      --oidc-token-audience="${SERVICE_URL}"
  else
    gcloud scheduler jobs create http "${job_name}" \
      --project="${PROJECT_ID}" \
      --location="${REGION}" \
      --schedule="${schedule}" \
      --time-zone="${TIME_ZONE}" \
      --uri="${COLLECT_URL}" \
      --http-method=POST \
      --message-body='{}' \
      --headers="Content-Type=application/json" \
      --oidc-service-account-email="${SCHEDULER_EMAIL}" \
      --oidc-token-audience="${SERVICE_URL}"
  fi
}

# Every 10 minutes. Calls before 9:31 ET are harmlessly skipped by /collect.
upsert_job "${COLLECTOR_JOB}" "*/10 9-15 * * 1-5"

# Final pass shortly after the close to capture the last RTH minutes through 15:59.
upsert_job "${FINALIZER_JOB}" "5 16 * * 1-5"

echo
echo "Collector jobs configured successfully."
echo "  ${COLLECTOR_JOB}: */10 9-15 * * 1-5 (${TIME_ZONE}) -> ${COLLECT_URL}"
echo "  ${FINALIZER_JOB}: 5 16 * * 1-5 (${TIME_ZONE}) -> ${COLLECT_URL}"
echo
echo "Optional immediate test:"
echo "  gcloud scheduler jobs run ${COLLECTOR_JOB} --project=${PROJECT_ID} --location=${REGION}"
