# Company contacts finder API: public emails and socials in Python

> Extract public corporate emails, inquiry forms, phone numbers and verified social profiles per domain with Python. Only public evidence — no private inbox guessing.

CRM enrichment and outbound workflows need contact channels that actually exist: the support email a company publishes, its press inbox, the official X/Twitter or LinkedIn profile — not guessed email patterns. Enterprise contact APIs charge per-credit subscriptions for data you can often find on the company's own site.

The [Company Contacts Finder](https://edtool79-collab.github.io/hirepulse-tools/company-contacts-api/) extracts exactly what the company publishes publicly: corporate emails, inquiry/contact form URLs, phone numbers, official social profiles, and DNS/MX email-provider evidence.

## What the finder returns

Input is a list of domains with optional DNS enrichment:

```json
{
  "domains": ["linear.app"],
  "include_dns": true,
  "use_paid_upstream": false
}
```

Each analyzed domain produces a structured record, for example:

```json
{
  "domain": "linear.app",
  "status": "ok",
  "linkedin": null,
  "twitter": "https://x.com/linear"
}
```

Records carry the publicly observed contact fields — emails, phones, inquiry forms, social profiles — plus MX/DNS evidence when `include_dns` is enabled, telling you whether the company runs Google Workspace, Microsoft 365 or its own mail stack.

## Quick start with cURL

```bash
curl --fail-with-body -X POST "https://api.apify.com/v2/acts/hirepulse~company-contact-details-finder/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "domains": ["stripe.com", "linear.app"],
  "include_dns": true
}'
```

## Production Python pipeline

Enriching a CRM export and splitting the output by channel reliability:

```python
import os
import json
from apify_client import ApifyClient

client = ApifyClient(os.environ.get("APIFY_TOKEN", "YOUR_APIFY_TOKEN"))

domains = ["stripe.com", "linear.app", "notion.so"]

run_input = {
    "domains": domains,
    "include_dns": True,        # add MX / mail-provider evidence
    "use_paid_upstream": False, # public evidence only
}

run = client.actor("hirepulse/company-contact-details-finder").call(run_input=run_input)

if not run or run.get("status") != "SUCCEEDED":
    raise RuntimeError("Actor execution failed; check run logs.")

records = list(client.dataset(run["defaultDatasetId"]).iterate_items())

ok = [r for r in records if r.get("status") == "ok"]
for r in ok:
    channels = {k: v for k, v in r.items() if k in ("linkedin", "twitter") and v}
    mail_provider = r.get("mail_provider") or "unknown"
    print(f"{r['domain']}: {channels or 'no socials found'} | mail: {mail_provider}")

with open("contacts.json", "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)
```

### Privacy boundaries are a feature

Only publicly accessible website and DNS evidence is extracted — no private employee inboxes, no gated data. That keeps the workflow inside acceptable-use lines for CRM enrichment and makes the output defensible: every contact traces to a page the company chose to publish. A personal-email enrichment product would be `not_for` this tool.

### MX evidence before cold email

`include_dns` returns the mail provider and SPF/DMARC context. A domain on Microsoft 365 with a `reject` DMARC policy behaves differently for deliverability than one on a small provider with no policy — route domains through a verification- and deliverability-aware sequence instead of blasting all of them identically.

### Charging follows success

Billing is per domain checked plus per public contact found; domains that publish nothing or are unreachable are not charged, and the run summary reports counts of checked, charged and unreachable domains. Batch up to 100 domains per run and read the summary to reconcile against your list.

## Technical limitations and pricing

- **Availability & Source Boundaries:** Extracts only publicly accessible evidence from company websites and DNS. Does not verify that an individual mailbox exists or accepts email; DNS/MX records are infrastructure evidence, not mailbox confirmation. Missing or blocked pages are reported without inventing details.
- **Pricing:** $0.005 per domain checked + $0.001 per public contact found. Domains with no contacts cost $0. Live Pricing tab is authoritative.

## Next steps

- [Open Company Contacts Finder on the Apify Store](https://apify.com/hirepulse/company-contact-details-finder)
- Explore parameters on the [tool documentation page](https://edtool79-collab.github.io/hirepulse-tools/company-contacts-api/)
- Related guide: [Hiring signals for sales: find companies that are growing](https://edtool79-collab.github.io/hirepulse-tools/guides/hiring-signals-for-sales/)

Source page: https://edtool79-collab.github.io/hirepulse-tools/guides/company-contacts-python/
