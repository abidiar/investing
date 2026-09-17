#!/usr/bin/env bash
set -euo pipefail

: "${PROJECT_ID:?Set PROJECT_ID before running, for example: export PROJECT_ID=my-project-id}"

REGION="${REGION:-us-east4}"
SERVICE_NAME="${SERVICE_NAME:-investing-os-post-open}"
JOB_NAME="${JOB_NAME:-investing-os-post-open-1016}"
SPREADSHEET_ID="${SPREADSHEET_ID:-14lTnD-on91I4F5E5FAQ8-39zTRv2GzBjyd1b4_uCzjc}"
SECRET_NAME="${SECRET_NAME:-tradier-api-token}"
RUNTIME_SA_NAME="${RUNTIME_SA_NAME:-investing-os-runtime}"
SCHEDULER_SA_NAME="${SCHEDULER_SA_NAME:-investing-os-scheduler}"

RUNTIME_EMAIL="${RUNTIME_SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
SCHEDULER_EMAIL="${SCHEDULER_SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud config set project "${PROJECT_ID}"

echo "Enabling required APIs..."
gcloud services enable \
  run.googleapis.com \
  cloudscheduler.googleapis.com \
  secretmanager.googleapis.com \
  sheets.googleapis.com \
  drive.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com

if ! gcloud iam service-accounts describe "${RUNTIME_EMAIL}" >/dev/null 2>&1; then
  gcloud iam service-accounts create "${RUNTIME_SA_NAME}" \
    --display-name="Investing OS Cloud Run runtime"
fi

if ! gcloud iam service-accounts describe "${SCHEDULER_EMAIL}" >/dev/null 2>&1; then
  gcloud iam service-accounts create "${SCHEDULER_SA_NAME}" \
    --display-name="Investing OS Cloud Scheduler invoker"
fi

echo
echo "Enter the Tradier token. Input is hidden and is sent directly to Secret Manager."
read -r -s -p "Tradier API token: " TRADIER_TOKEN
echo

if gcloud secrets describe "${SECRET_NAME}" >/dev/null 2>&1; then
  printf '%s' "${TRADIER_TOKEN}" | gcloud secrets versions add "${SECRET_NAME}" --data-file=-
else
  printf '%s' "${TRADIER_TOKEN}" | gcloud secrets create "${SECRET_NAME}" \
    --replication-policy="automatic" --data-file=-
fi
unset TRADIER_TOKEN

SECRET_VERSION="$(gcloud secrets versions list "${SECRET_NAME}" \
  --filter='state=ENABLED' --sort-by='~createTime' --limit=1 \
  --format='value(name.basename())')"

gcloud secrets add-iam-policy-binding "${SECRET_NAME}" \
  --member="serviceAccount:${RUNTIME_EMAIL}" \
  --role="roles/secretmanager.secretAccessor" >/dev/null

echo "Deploying private Cloud Run service..."
gcloud run deploy "${SERVICE_NAME}" \
  --source . \
  --region="${REGION}" \
  --service-account="${RUNTIME_EMAIL}" \
  --no-allow-unauthenticated \
  --cpu=1 \
  --memory=512Mi \
  --min-instances=0 \
  --max-instances=1 \
  --concurrency=1 \
  --timeout=120 \
  --set-env-vars="SPREADSHEET_ID=${SPREADSHEET_ID},CONFIRMATION_SHEET=Post-Open Confirmation,TRADIER_BASE_URL=https://api.tradier.com/v1,DATA_SOURCE=Tradier Consolidated,TIMEZONE=America/New_York" \
  --set-secrets="TRADIER_API_TOKEN=${SECRET_NAME}:${SECRET_VERSION}"

SERVICE_URL="$(gcloud run services describe "${SERVICE_NAME}" \
  --region="${REGION}" --format='value(status.url)')"

gcloud run services add-iam-policy-binding "${SERVICE_NAME}" \
  --region="${REGION}" \
  --member="serviceAccount:${SCHEDULER_EMAIL}" \
  --role="roles/run.invoker" >/dev/null

if gcloud scheduler jobs describe "${JOB_NAME}" --location="${REGION}" >/dev/null 2>&1; then
  gcloud scheduler jobs update http "${JOB_NAME}" \
    --location="${REGION}" \
    --schedule="16 10 * * 1-5" \
    --time-zone="America/New_York" \
    --uri="${SERVICE_URL}/confirm" \
    --http-method=POST \
    --message-body='{}' \
    --update-headers="Content-Type=application/json" \
    --oidc-service-account-email="${SCHEDULER_EMAIL}" \
    --oidc-token-audience="${SERVICE_URL}"
else
  gcloud scheduler jobs create http "${JOB_NAME}" \
    --location="${REGION}" \
    --schedule="16 10 * * 1-5" \
    --time-zone="America/New_York" \
    --uri="${SERVICE_URL}/confirm" \
    --http-method=POST \
    --message-body='{}' \
    --headers="Content-Type=application/json" \
    --oidc-service-account-email="${SCHEDULER_EMAIL}" \
    --oidc-token-audience="${SERVICE_URL}"
fi

cat <<EOF

Deployment finished.

Cloud Run URL:
  ${SERVICE_URL}

IMPORTANT — share the Google Sheet as Editor with:
  ${RUNTIME_EMAIL}

Spreadsheet:
  https://docs.google.com/spreadsheets/d/${SPREADSHEET_ID}/edit

After sharing, run a manual Scheduler test:
  gcloud scheduler jobs run ${JOB_NAME} --location=${REGION}

Then inspect logs:
  gcloud run services logs read ${SERVICE_NAME} --region=${REGION} --limit=50

The scheduled run is 10:16 AM America/New_York, Monday-Friday.
The handler checks Tradier's market clock and skips closed-market days.
EOF
