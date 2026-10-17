# Scrape Greenhouse, Lever & Ashby Jobs Without API Keys

> Extract every open job from Greenhouse, Lever, Ashby, and Workable boards without employer API keys. Complete Python scraping guide.

If you track tech hiring, recruit talent, or sell B2B software, monitoring open roles at specific target accounts is essential. When a company posts ten new data engineering roles or starts hiring its first account executives in EMEA, it signals technical investment, team expansion, and potential software budget.

The challenge is building an automated collection pipeline. Every company hosts their career portal on a different applicant tracking system (ATS)—one uses Greenhouse, another Lever, a third Ashby or Workable. Career page URLs are constantly changing, and legacy scrapers break whenever an employer modifies their frontend site template.

The [ATS Job Scraper](https://edtool79-collab.github.io/hirepulse-tools/ats-jobs-api/) simplifies this by resolving company domains directly to their underlying ATS boards. You pass plain domains—like `stripe.com` or `notion.so`—and the tool automatically locates the active board and extracts every open role into standardized JSON records.

## Supported ATS platforms and extracted fields

The scraper automatically detects and extracts job postings from six major modern ATS providers:
- **Greenhouse**
- **Lever**
- **Ashby**
- **Workable**
- **Recruitee**
- **SmartRecruiters**

*(Note: Legacy enterprise suites like Workday or bespoke in-house career portals are not supported.)*

For every open posting discovered, the tool extracts standardized attributes:
- **Role information:** Job `title`, hiring `department` or team classification, and primary `location`.
- **Work arrangement:** Explicit `is_remote` boolean flag indicating whether the position offers remote flexibility.
- **Timeline:** The `posting_date` timestamp.
- **Direct application:** The canonical `apply_url` leading directly to the ATS candidate submission form.
- **Compensation:** The published `salary` range, where disclosed by the employer.

The tool also features an incremental tracking capability (`only_new_jobs: true`), enabling you to run scheduled daily or weekly jobs that return only new openings posted since the previous execution.

## Quick start with cURL

You can execute a multi-company lookup via Apify's synchronous dataset endpoint:

```bash
curl --fail-with-body -X POST "https://api.apify.com/v2/acts/hirepulse~ats-job-pulse/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "companies": [
    "stripe.com",
    "notion.so"
  ]
}'
```

This request queries the career boards for both `stripe.com` and `notion.so`, resolving their ATS endpoints and returning all active listings.

## Building a Python hiring intelligence monitor

Using `apify-client`, you can pull open jobs across a portfolio of target accounts, categorize hiring velocity by department, and flag key hiring expansions:

```bash
pip install apify-client
```

```python
import os
import json
from collections import Counter
from pathlib import Path
from apify_client import ApifyClient

# Initialize client
client = ApifyClient(os.environ.get("APIFY_TOKEN", "YOUR_APIFY_TOKEN"))

# Target company domains to monitor
target_accounts = [
    "stripe.com",
    "notion.so"
]

run_input = {
    "companies": target_accounts
}

# Run the ATS Job Scraper Actor
run = client.actor("hirepulse/ats-job-pulse").call(run_input=run_input)

if not run or run.get("status") != "SUCCEEDED":
    raise RuntimeError(f"Actor run failed with status: {run.get('status')}")

# Iterate through dataset items
all_jobs = list(client.dataset(run["defaultDatasetId"]).iterate_items())
print(f"Collected {len(all_jobs)} open roles across {len(target_accounts)} companies.\n")

# Aggregate hiring by company and department
company_breakdown = {}

for job in all_jobs:
    company = job.get("company", "Unknown")
    dept = job.get("department", "General")
    title = job.get("title", "")
    is_remote = job.get("is_remote", False)
    apply_url = job.get("apply_url", "")

    if company not in company_breakdown:
        company_breakdown[company] = {
            "total_jobs": 0,
            "remote_jobs": 0,
            "departments": Counter(),
            "sample_roles": []
        }

    company_breakdown[company]["total_jobs"] += 1
    if is_remote:
        company_breakdown[company]["remote_jobs"] += 1
    company_breakdown[company]["departments"][dept] += 1

    if len(company_breakdown[company]["sample_roles"]) < 3:
        company_breakdown[company]["sample_roles"].append({
            "title": title,
            "dept": dept,
            "apply_url": apply_url
        })

# Display summary report
for company, data in company_breakdown.items():
    print(f"=== {company.upper()} ({data['total_jobs']} Open Roles, {data['remote_jobs']} Remote) ===")
    print("Top Departments:")
    for dept, count in data["departments"].most_common(4):
        print(f"  - {dept}: {count} openings")
    print("Sample Roles:")
    for role in data["sample_roles"]:
        print(f"  * {role['title']} ({role['dept']})")
    print()

# Save detailed report
Path("ats_job_report.json").write_text(
    json.dumps(company_breakdown, indent=2, ensure_ascii=False),
    encoding="utf-8"
)
```

## Best practices for account-based hiring tracking

### 1. Distinguishing job queries from company board audits
When your research question is "Which companies are hiring machine learning engineers in Berlin?", use a query-based tool like the [Google Jobs Scraper](https://edtool79-collab.github.io/hirepulse-tools/google-jobs-api/). When your question is "What exactly is Stripe building right now across all engineering teams?", query the company's ATS board directly with the ATS Job Scraper.

### 2. Monitoring department hiring velocity
Total job counts provide a snapshot, but department distribution indicates strategic intent. A company with 20 new engineering roles is investing in product development; a company with 15 sales development representative (SDR) roles is scaling its outbound revenue engine.

### 3. Understanding ATS update timestamps
Some ATS providers update the `posting_date` timestamp whenever a job description is touched or refreshed by a recruiter, rather than only when the requisition was originally opened. When configuring new-job alerts, evaluate incremental changes between successive snapshots (`only_new_jobs: true`) rather than relying purely on absolute dates.

## Technical limitations and pricing

- **ATS coverage:** Supports Greenhouse, Lever, Ashby, Workable, Recruitee, and SmartRecruiters. It does not support Workday or proprietary internal career portals.
- **Salary disclosure:** Extracted whenever published on the public board; postings where compensation is not stated will omit salary values.
- **Pricing:** $0.05 per company whose job board was found and processed, however many jobs it has. Companies that are not found, and failed ones, are not charged.

## Next steps

- [Open ATS Job Scraper on the Apify Store](https://apify.com/hirepulse/ats-job-pulse)
- Review full documentation and schemas on the [tool page](https://edtool79-collab.github.io/hirepulse-tools/ats-jobs-api/)
- Combine ATS hiring with Google Ads and SEO momentum in [Hiring signals for sales](https://edtool79-collab.github.io/hirepulse-tools/guides/hiring-signals-for-sales/), or discover roles by title and location in [Google Jobs API](https://edtool79-collab.github.io/hirepulse-tools/guides/google-jobs-json-python/)

Source page: https://edtool79-collab.github.io/hirepulse-tools/guides/greenhouse-lever-ashby-jobs-api/
