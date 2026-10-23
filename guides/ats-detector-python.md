# ATS detector API: find any company's job board in Python

> Detect which ATS a company runs (Greenhouse, Lever, Ashby) from its domain and get the official careers board URL with Python. Free Actor, no employer keys.

Before you can scrape a company's jobs you need two facts: which applicant tracking system powers its careers site, and the real URL of the public board. Manual detection means viewing the page source, hunting for `boards.greenhouse.io` or `/api/ashby/` references, and repeating per company.

The [ATS Detector](https://edtool79-collab.github.io/hirepulse-tools/ats-detector-api/) automates that: pass a domain, get the detected ATS vendor (Greenhouse, Lever, Ashby, Workable, Recruitee, SmartRecruiters), the official public board URL, and the available job count — one metadata record per domain.

## Detection architecture

The Actor inspects public website evidence and known ATS URL patterns from a plain-HTTP pass — no headless browser, no employer API keys. A typical record:

```json
{
  "domain": "linear.app",
  "status": "found",
  "ats": "ashby",
  "board_slug": "linear",
  "board_url": "https://jobs.ashbyhq.com/linear",
  "open_jobs": 27,
  "note": null,
  "checked_at": "2026-10-20T21:22:00.000Z"
}
```

`note` is non-null when detection is partial (for example a custom-hosted portal without a standard vendor), so downstream code can branch on uncertainty instead of treating every row the same.

## Quick start with cURL

```bash
curl --fail-with-body -X POST "https://api.apify.com/v2/acts/hirepulse~ats-detector/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "domains": ["linear.app", "datadoghq.com"]
}'
```

## Production Python pipeline

A two-stage pipeline typical in lead qualification: detect boards in bulk, then hand found boards to a jobs scraper:

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ.get("APIFY_TOKEN", "YOUR_APIFY_TOKEN"))

domains = ["linear.app", "datadoghq.com", "retail-company.example"]

run = client.actor("hirepulse/ats-detector").call(run_input={"domains": domains})
records = list(client.dataset(run["defaultDatasetId"]).iterate_items())

found = [r for r in records if r.get("status") == "found"]
missing = [r for r in records if r.get("status") != "found"]

for r in found:
    print(f"{r['domain']}: {r['ats']} board at {r['board_url']} ({r['open_jobs']} jobs)")

# Stage 2: feed detected boards into the ATS Job Scraper for listings.
if found:
    scrape_input = {"domains": [r["domain"] for r in found]}
    jobs_run = client.actor("hirepulse/ats-job-pulse").call(run_input=scrape_input)
    jobs = list(client.dataset(jobs_run["defaultDatasetId"]).iterate_items())
    print(f"Pulled {len(jobs)} job records from detected boards.")

print(f"Undetected (not charged): {[r['domain'] for r in missing]}")
```

Undetected boards cost $0, so cold lists with many non-ATS companies are cheap to triage through this tool first rather than running a heavier scraper blindly.

### Detection, not parsing

The detector identifies the vendor and board URL and counts available jobs. It does not parse individual postings — chain into the [ATS Job Scraper](https://edtool79-collab.github.io/hirepulse-tools/ats-jobs-api/) for titles, salaries and apply links. Keeping the two stages separate lets you price-optimise: a $0.005 metadata check before committing to a $0.05 full-board pull.

### Custom career portals

Some companies host hiring on their own domain instead of a standard ATS. Those return a `note` describing what was observed rather than a clean vendor match. Treat `note != null` rows as candidates for manual review, not as garbage.

### Sizing and concurrency

Input is a list of company domains (up to 100 per run). Detection is lightweight plain-HTTP, so throughput is high and timeouts are rare; batch a full CRM export in one call rather than looping per-domain, which multiplies Actor-start events.

## Technical limitations and pricing

- **Availability & Source Boundaries:** Detects Greenhouse, Lever, Ashby, Workable, Recruitee and SmartRecruiters, plus custom career portals. Returns board metadata and available job count, not individual listings. Workday, Taleo and SAP SuccessFactors are not standard detections.
- **Pricing:** The Actor itself has no fee configured; normal Apify platform usage charges can apply. Undetected boards cost $0. The live Pricing tab is authoritative — set a maximum total charge before starting a run.

## Next steps

- [Open ATS Detector on the Apify Store](https://apify.com/hirepulse/ats-detector)
- Explore parameters on the [tool documentation page](https://edtool79-collab.github.io/hirepulse-tools/ats-detector-api/)
- Related guide: [Greenhouse, Lever and Ashby jobs API without employer keys](https://edtool79-collab.github.io/hirepulse-tools/guides/greenhouse-lever-ashby-jobs-api/)

Source page: https://edtool79-collab.github.io/hirepulse-tools/guides/ats-detector-python/
