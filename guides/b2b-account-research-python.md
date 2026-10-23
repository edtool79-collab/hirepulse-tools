# B2B account research in Python: hiring, tech and email signals per domain

> Turn company domains into account dossiers with Python: live open-job counts, named technologies from postings, mail provider and public contacts for $0.005 per profile.

Account research from a domain usually means stitching five tools together: one for hiring signals, one for the tech stack, one for contacts, one for email infrastructure, and glue code to keep the statuses straight. Enterprise intent platforms (ZoomInfo, Clay waterfalls) price the same stitches at subscriptions or per-credit rates that dwarf the cost of calling the public evidence directly.

The [B2B Account Research Agent](https://edtool79-collab.github.io/hirepulse-tools/b2b-account-research-api/) does the stitching: one domain in, one JSON dossier out — hiring data from the company's ATS, website technologies, how the company sells, its mail setup from public DNS, and publicly published contacts, each section with its own status.

## Inside one dossier

Input is just a list of domains:

```json
{ "domains": ["linear.app", "vercel.com"] }
```

A real output row (for linear.app, shortened):

```json
{
  "domain": "linear.app",
  "status": "ok",
  "company_name": "Linear",
  "tech_stack": ["Cloudflare", "Next.js", "React"],
  "mail_provider": "Google Workspace",
  "email_senders": ["Google Workflow", "Amazon SES", "HubSpot"],
  "dmarc_policy": "reject",
  "ats": {
    "detected": true, "platform": "ashby", "match": "linked",
    "evidence_url": "https://linear.app/careers",
    "active_jobs_count": 34, "remote_jobs_count": 34,
    "departments": [{"name": "GTM", "count": 19}, {"name": "Product", "count": 13}],
    "posted_last_7_days": 7, "posted_last_30_days": 10,
    "sample_titles": ["Product Support Specialist, APAC", "Field Marketing Manager"]
  }
}
```

The dossier also covers technologies named in job postings (each with a short quote), GTM/product/engineering hiring flags, leadership roles, pricing-page and free-trial presence, security certifications claimed on the trust page, and the languages the site localizes for.

## Quick start with cURL

```bash
curl --fail-with-body -X POST "https://api.apify.com/v2/acts/hirepulse~b2b-account-research-agent/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "domains": ["linear.app", "vercel.com"]
}'
```

## Production Python: score and rank an account list

```python
import os
import json
from apify_client import ApifyClient

client = ApifyClient(os.environ.get("APIFY_TOKEN", "YOUR_APIFY_TOKEN"))

# Your CRM export of target domains
domains = ["linear.app", "vercel.com", "notion.so", "stripe.com"]

run = client.actor("hirepulse/b2b-account-research-agent").call(
    run_input={"domains": domains}
)

if not run or run.get("status") != "SUCCEEDED":
    raise RuntimeError("Actor execution failed; check run logs.")

profiles = list(client.dataset(run["defaultDatasetId"]).iterate_items())

def intent_score(p: dict) -> int:
    """Explainable heuristic: recent hiring + GTM roles + selling signals."""
    ats = p.get("ats") or {}
    score = 0
    score += min(ats.get("posted_last_30_days", 0), 20)      # hiring recency
    score += min(ats.get("active_jobs_count", 0) // 2, 15)   # hiring scale
    depts = {d["name"].upper() for d in ats.get("departments", [])}
    score += 10 if "GTM" in depts or "SALES" in depts else 0
    pages = p.get("sales_signals") or {}
    score += 5 if pages.get("pricing_page") else 0
    score += 5 if pages.get("free_trial") else 0
    return score

ranked = sorted(
    (p for p in profiles if p.get("status") == "ok"),
    key=intent_score, reverse=True,
)
for p in ranked:
    print(f"{intent_score(p):3d}  {p['domain']:20s}  jobs={p.get('ats',{}).get('active_jobs_count')}  mail={p.get('mail_provider')}")

with open("ranked_accounts.json", "w", encoding="utf-8") as f:
    json.dump(ranked, f, ensure_ascii=False, indent=2)
```

### Unknown is not zero

Every section carries its own status. A blocked website never renders as "no data": a missing hiring count means the count is unknown, and the record says so. Build your downstream scoring on tri-state logic (present / absent / unknown) — collapsing unknown to zero silently biases rankings toward whoever publishes more.

### Built for agent loops and CRM plumbing

The output is agent-ready by design: one compact JSON row per company with section statuses, made for LangGraph/CrewAI/Claude-tool loops, n8n/Make/Clay workflows, or direct CRM field writes. It is explicitly not for personal-email discovery, mailbox verification, or revenue/headcount estimation.

### Cost model favors broad triage

At $0.005 per useful profile — blocked, parked and DNS-only results are not charged — running a full mid-market list is an order of magnitude cheaper than per-credit waterfall tools. Use this as the first enrichment pass, then reserve your expensive signal vendors for the accounts the dossier already ranks high.

## Technical limitations and pricing

- **Availability & Source Boundaries:** Hiring data comes from detected ATS boards (Greenhouse, Lever, Ashby, Workable, Recruitee, SmartRecruiters) with live open-job counts; technologies from public page and posting evidence; email setup from public DNS; contacts only from the company's own published pages. No browser, no login, no paid data providers. Not for personal email discovery, mailbox verification, revenue or headcount.
- **Pricing:** $0.005 per useful profile; blocked, parked and DNS-only results are not charged. No third-party data-provider key required.

## Next steps

- [Open B2B Account Research Agent on the Apify Store](https://apify.com/hirepulse/b2b-account-research-agent)
- Explore parameters on the [tool documentation page](https://edtool79-collab.github.io/hirepulse-tools/b2b-account-research-api/)
- Related guide: [Company contacts finder API: public emails and socials in Python](https://edtool79-collab.github.io/hirepulse-tools/guides/company-contacts-python/)

Source page: https://edtool79-collab.github.io/hirepulse-tools/guides/b2b-account-research-python/
