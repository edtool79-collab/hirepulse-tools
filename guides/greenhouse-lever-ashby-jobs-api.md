# Track company jobs in Python: Greenhouse, Lever and Ashby

Verified 2026-10-28. For recruiting teams and account researchers who need jobs from specific companies. Get apply links and a company summary from supported public ATS boards.

[Open Actor](https://apify.com/hirepulse/ats-job-pulse?utm_source=hirepulse_docs&utm_medium=owned&utm_campaign=apify_quickstart_20261028&utm_content=ats-job-pulse)

## Input

```json
{
  "companies": [
    "linear.app"
  ],
  "output_mode": "jobs_and_summary",
  "max_jobs_per_company": 3,
  "track_diff": false
}
```

## Run in Python

Download [runner](https://edtool79-collab.github.io/hirepulse-tools/examples/apify-bounded-run.py) and [input](https://edtool79-collab.github.io/hirepulse-tools/examples/ats-job-pulse.json).

```bash
pip install requests
# Set APIFY_TOKEN in your environment; never paste it into this website.
python apify-bounded-run.py hirepulse/ats-job-pulse ats-job-pulse.json 0.06
```

## Captured owner output

Captured 2026-10-28T09:52:47.507Z, Build rZjr8CeDoss1izo48. Selected fields, not customer results or current measurements.

```json
{
  "record_type": "company_summary",
  "company_domain": "linear.app",
  "ats_type": "ashby",
  "total_active_jobs": 32,
  "remote_jobs": 32,
  "is_first_run": null,
  "new_jobs": null,
  "closed_jobs": null,
  "matching_jobs": 32
}
```

## Cost and limits

Standard company-processed event: $0.05 for each successfully processed company, plus the listed Actor start event; plan discounts may apply. No company event for a company that is not found or fails. The sample uses a $0.06 maximum event charge.

Workday and other unsupported or protected boards may return no data. Missing data does not mean a company is not hiring. An open job is not proof of buying intent or budget. Filters and output caps do not reduce the per-company charge.

For change tracking, use track_diff=true and a unique, stable state_id for your watchlist. Set only_changes=true for later comparisons. The first run is a baseline, not a hiring spike. Schedule future runs in your own Apify account only after reviewing their recurring cost.
