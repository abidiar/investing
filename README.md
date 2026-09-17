# Investing OS — Tradier → Cloud Run → Google Sheets

This is the **Phase 1 connection service** for the active control plane:

- Spreadsheet: `Investing OS Intelligence Engine v1.0`
- Spreadsheet ID: `14lTnD-on91I4F5E5FAQ8-39zTRv2GzBjyd1b4_uCzjc`
- Target tab: `Post-Open Confirmation`
- Schedule: 10:16 AM Eastern, Monday–Friday
- Data source: Tradier production consolidated market data

## What this version does

1. Keeps the Cloud Run service private.
2. Receives an authenticated POST from Cloud Scheduler.
3. Checks Tradier's market clock.
4. Reads the existing preregistered premarket setup.
5. Stops without inventing a setup when `Premarket setup valid?` is not `Yes`.
6. Retrieves Tradier batch quotes and one-minute Time & Sales bars.
7. Calculates and writes current price, cumulative session VWAP, open, session high/low, 5-minute and 15-minute opening ranges, relative strength, latest-minute new-low status, and consolidated volume.
8. Leaves the evidence matrix governed separately. It does **not** falsely pass evidence gates.

It does not place orders and contains no Tradier trading endpoint.

## Deploy from Google Cloud Shell

1. Upload and unzip this package:

```bash
unzip investing-os-tradier-cloud-run.zip
cd investing-os-tradier-cloud-run
chmod +x deploy.sh
```

2. Set the Google Cloud project ID:

```bash
export PROJECT_ID="YOUR_GOOGLE_CLOUD_PROJECT_ID"
export REGION="us-east4"
```

3. Deploy:

```bash
./deploy.sh
```

The script prompts for the Tradier token without displaying it and stores it directly in Secret Manager.

4. Share the Google Sheet as **Editor** with the runtime service-account email printed by the script. Do not make the Sheet public.

5. Test:

```bash
gcloud scheduler jobs run investing-os-post-open-1016 --location=us-east4
gcloud run services logs read investing-os-post-open --region=us-east4 --limit=50
```

## Security model

- `investing-os-runtime@PROJECT_ID.iam.gserviceaccount.com`: accesses the one Tradier secret and the specifically shared Sheet.
- `investing-os-scheduler@PROJECT_ID.iam.gserviceaccount.com`: has only Cloud Run Invoker on the private service.
- Scheduler authenticates with OIDC.
- The service does not allow unauthenticated access.
- Cloud Run is capped at one instance and zero minimum instances.

## Scheduler behavior

Cron: `16 10 * * 1-5`

Time zone: `America/New_York`

The job can fire on a weekday holiday, but the app checks Tradier's market clock and exits when the market is closed.

## Sandbox testing

Use `https://sandbox.tradier.com/v1` and the sandbox token for delayed-data testing. Return to production before relying on the 10:16 snapshot.

## Next version

Phase 2 should add the automatic evidence matrix, two completed five-minute VWAP holds, sector breadth, constituent participation, trap checks, five-minute ATR, anti-chasing calculations, and an append-only post-open log. Those rules should be added only after this connection version's raw values are verified against the broker feed.
