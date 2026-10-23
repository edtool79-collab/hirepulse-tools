# Website tech stack API: detect CMS, frameworks and pixels in Python

> Detect what any website runs in bulk with Python: CMS, frameworks, hosting, analytics and ad pixels with evidence and confidence levels, per-domain pricing.

When you qualify accounts, audit competitors, or monitor a portfolio of sites, you need to know what each website actually runs: which CMS, which frontend framework, which analytics and ad pixels, and who hosts it. Enterprise tools like BuiltWith charge recurring subscriptions for this, and a headless-browser crawler costs real compute per page.

The [Website Tech Stack Detector](https://edtool79-collab.github.io/hirepulse-tools/website-tech-stack-api/) takes plain-HTTP inspection instead: paste a list of domains and get what each one runs, with the evidence that proved every detection plus a confidence level, so a wrong row is auditable. Unreachable domains are never charged.

## What the detector returns

The Actor's input is a required list of domains (up to 100 per run):

```json
{
  "domains": [
    "linear.app"
  ],
  "track_diff": false,
  "use_paid_upstream": false
}
```

Every analyzed domain produces a structured record with observed evidence fields, for example:

```json
{
  "domain": "linear.app",
  "status": "ok",
  "final_url": "https://linear.app/",
  "title": "Linear — The system for product development",
  "has_meta_pixel": false,
  "has_google_ads_tag": false,
  "has_ga4": false,
  "has_gtm": false,
  "has_linkedin_insight": false
}
```

Beyond the boolean pixel flags shown above, detection covers CMS, frontend frameworks, ecommerce platforms, hosting, analytics, payments and support widgets, plus DNS email-provider signals. Every detection returns the evidence that proved it and a confidence level.

Two optional flags worth knowing:

- **`track_diff`** — run the same watchlist repeatedly and record technology changes between runs; set `"only_changes": true` to return only domains whose technologies changed since the last run, plus first runs.
- **`use_paid_upstream`** — owner-side opt-in for external paid data providers; it stays disabled by default, so the default run leans on public and platform-native evidence only.

## Quick start with cURL

```bash
curl --fail-with-body -X POST "https://api.apify.com/v2/acts/hirepulse~website-tech-stack-detector/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "domains": ["stripe.com", "linear.app"],
  "track_diff": false
}'
```

## Production Python pipeline

A bulk enrichment script mapping a CRM export of domains to tech-stack rows:

```python
import os
import json
import csv
from apify_client import ApifyClient

client = ApifyClient(os.environ.get("APIFY_TOKEN", "YOUR_APIFY_TOKEN"))

domains = ["stripe.com", "linear.app", "notion.so"]

run_input = {
    "domains": domains,
    "track_diff": False,          # set True for repeated watchlist runs
    "use_paid_upstream": False,   # keep public evidence only
}

run = client.actor("hirepulse/website-tech-stack-detector").call(run_input=run_input)

if not run or run.get("status") != "SUCCEEDED":
    raise RuntimeError("Actor execution failed; check run logs.")

records = list(client.dataset(run["defaultDatasetId"]).iterate_items())

with open("tech_stacks.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["domain", "status", "final_url"])
    # Real records carry more fields; extend fieldnames to the ones you need.
    writer.writeheader()
    for rec in records:
        writer.writerow({k: rec.get(k, "") for k in writer.fieldnames})

ok = sum(1 for r in records if r.get("status") == "ok")
blocked = sum(1 for r in records if r.get("status") != "ok")
print(f"Analyzed: {len(records)} | ok: {ok} | not ok (never charged): {blocked}")
```

## Architectural considerations

### Evidence-backed rows beat score-only rows

Each detection ships with the proof that triggered it, so when a downstream stakeholder asks "why did you say this site runs GTM?", the answer is in the record itself. This matters when feeding results into scoring models: evidence rows let you build confidence-weighted features instead of trusting a bare boolean.

### Batch sizing and charging granularity

One run accepts up to 100 domains. Domains whose home page never answers, are blocked, or are invalid are not charged, and each chargeable response is a documented event per domain. The run summary (in the `OUTPUT` key-value record) reports counts of checked, charged and unreachable domains, plus related HirePulse tools that add data for the same input, so you can chain enrichment deliberately.

### Monitoring beats one-shot enrichment

With `track_diff: true`, repeated runs on the same watchlist become a change feed: new pixels appear, hosting shifts, a CMS migration lands. Driving this from a scheduled job gives you a technographic change stream for competitor monitoring or portfolio watch, at event pricing only when a page actually answered.

### Consent and dynamic loading hide tools

Detection is based on visible page and DNS evidence. Consent banners, client-side lazy loading and strict blockers can hide a technology, and a detected pixel does not prove active advertising or spend. Treat nulls and low-confidence rows as unknowns rather than negatives.

## Technical limitations and pricing

- **Availability & Source Boundaries:** The default mode uses public or platform-native sources with external paid data providers disabled. It does not execute heavy headless-browser rendering for SPA post-render injections, does not measure ad spend or traffic, and reports unsupported or unavailable fields honestly.
- **Pricing:** $0.005 per domain checked + $0.001 per detected tech (before Apify plan discounts). Domains with no stack cost $0; unreachable, blocked and invalid domains are never charged. The live Pricing tab is authoritative — set a maximum total charge before starting a run.

## Next steps

- [Open Website Tech Stack Detector on the Apify Store](https://apify.com/hirepulse/website-tech-stack-detector)
- Explore parameters on the [tool documentation page](https://edtool79-collab.github.io/hirepulse-tools/website-tech-stack-api/)
- Related guide: [Domain SEO API: inspect public website metadata](https://edtool79-collab.github.io/hirepulse-tools/guides/domain-seo-overview-python/)

Source page: https://edtool79-collab.github.io/hirepulse-tools/guides/website-tech-stack-python/
