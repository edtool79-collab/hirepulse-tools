# Build an n8n data API workflow with a real JSON input

> Build an n8n workflow that pulls competitor Google ads on a schedule, checks the JSON and sends only new ads to Slack.

Workflow automation tools like **n8n** allow engineering and growth teams to build resilient data pipelines without maintaining dedicated backend servers. Whether you are synchronizing leads into a CRM, monitoring competitors on a weekly schedule, or feeding fresh intelligence into an internal database, n8n provides a visual node canvas backed by self-hosted or cloud execution.

Connecting external data APIs into n8n is straightforward, but production workflows require proper architectural discipline: securing API credentials, validating responses, handling empty states, and preventing alert fatigue.

This guide walks through building an end-to-end competitor intelligence watcher in n8n using the [Google Ads Transparency Scraper](https://edtool79-collab.github.io/hirepulse-tools/google-ads-transparency-api/). We will configure an HTTP Request node, validate the structured JSON response, and route formatted alerts to Slack or Google Sheets.

## Architecture of the workflow

A reliable data automation in n8n follows a four-stage pipeline:

1. **Trigger:** A Manual Trigger for testing, transitioning to a Schedule Trigger (e.g., every Monday at 09:00 AM) in production.
2. **API Call:** An HTTP Request node calling Apify's synchronous dataset endpoint (`run-sync-get-dataset-items`) with a JSON payload.
3. **Validation & Filtering:** An IF or Switch node verifying that data was returned and isolating new ad creatives.
4. **Action:** Appending new rows to a Google Sheet or posting formatted alerts to a team Slack channel.

## Step 1: Configure the HTTP Request Node

In your n8n workflow canvas, add an **HTTP Request** node and configure the connection parameters:

- **Method:** `POST`
- **URL:** 
  ```text
  https://api.apify.com/v2/acts/hirepulse~google-ads-transparency-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN
  ```
- **Send Headers:** Enable headers and add:
  - `Content-Type`: `application/json`
- **Send Body:** Enable and select **JSON**. Paste the target request object:
  ```json
  {
    "domains": [
      "nike.com"
    ],
    "country": "US",
    "max_ads_per_domain": 40,
    "mode": "ads"
  }
  ```

### Managing API tokens securely in n8n
Never hardcode raw API tokens directly into the URL field in shared or version-controlled workflows. Instead:
- In n8n, create a new **Header Auth** credential named `Apify Auth`. Set the header name to `Authorization` and the value to `Bearer YOUR_APIFY_TOKEN`.
- Alternatively, use n8n's environment variables (`$env.APIFY_TOKEN`) to reference your secret securely at runtime.

## Step 2: Validate the raw JSON response

Execute the HTTP Request node manually. Because we are calling the synchronous dataset endpoint (`run-sync-get-dataset-items`), Apify runs the Actor and returns the resulting dataset items directly as a JSON array of items:

```json
[
  {
    "domain": "nike.com",
    "advertiser_name": "Nike, Inc.",
    "advertiser_verified": true,
    "format": "text",
    "first_shown": "2023-11-16T21:51:37Z",
    "last_shown": "2026-10-14T15:10:53Z",
    "days_running": 1062
  }
]
```

Inspect the returned items in n8n's output panel. Confirm that expected attributes—such as `domain`, `advertiser_name`, `format`, and `days_running`—are present before adding downstream consumers.

## Step 3: Implement branching and filtering

Not every execution will contain actionable creative changes. If you configure recurring competitor surveillance using the `"only_new_ads": true` setting:
- Runs where competitors launched new ads will return creative items with `format` and timestamps.
- Runs where no new ads appeared will return an empty array or an informational status message.

Add an **IF Node** after your HTTP step:
- **Condition:** String `{{ $json.format }}` is not empty.
- **True branch:** Connect to your Slack or database notification steps.
- **False branch:** Connect to a No-Operation (NoOp) node or log entry.

This simple condition ensures your team only receives alerts when actionable new creatives are detected, eliminating notification spam.

## Step 4: Formatting Slack and team alerts

Connect a **Slack Node** or **Webhook Node** to the True branch of your IF node. Format the message markdown to highlight key competitor intelligence:

```text
🚨 New Competitor Ad Detected: {{ $json.domain }}
• Advertiser: {{ $json.advertiser_name }} (Verified: {{ $json.advertiser_verified }})
• Format: {{ $json.format }}
• First Seen: {{ $json.first_shown }}
• Days Running: {{ $json.days_running }} days
```

Recipients can immediately see the ad format, advertiser identity, and lifespan without leaving Slack.

## Error handling and retry strategies

For enterprise reliability, configure n8n's node error handling settings:

- **Retry on Fail:** Enable with 2 retries and a 5-second interval to handle transient network hiccups.
- **Error Trigger:** Create a global Error Trigger workflow that catches unexpected HTTP 4xx/5xx responses and alerts an on-call engineer rather than failing silently.
- **Execution Logging:** n8n saves execution histories by default. When auditing historical runs, you can inspect the exact input payload submitted and compare it with the downstream records written to your database.

## Technical limitations and pricing

- **Scope:** The scraper extracts public Google Ads Transparency data (text, image, and video creatives, first/last seen dates, preview assets, and verification status). It does not expose private ad spend, conversion numbers, or CPC bidding metrics.
- **Pricing:** Billed at $0.005 per domain checked + $0.0015 per ad returned. The free Apify plan supports testing 1 domain with up to 5 ads.

## Next steps

- [Open Google Ads Transparency Scraper on the Apify Store](https://apify.com/hirepulse/google-ads-transparency-scraper)
- Review full input documentation on the [tool page](https://edtool79-collab.github.io/hirepulse-tools/google-ads-transparency-api/)
- Learn more about competitor creative analysis in [How to see every Google ad a competitor runs](https://edtool79-collab.github.io/hirepulse-tools/guides/competitor-google-ads/), or explore automated job tracking in [Google Jobs API with Python](https://edtool79-collab.github.io/hirepulse-tools/guides/google-jobs-json-python/)

Source page: https://edtool79-collab.github.io/hirepulse-tools/guides/n8n-data-api-workflow/
