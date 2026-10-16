# Find companies hiring now: a hiring-signals workflow for sales

> Find companies that are hiring right now and rank them for outreach: open jobs, Google ads, SEO trend and an intent score per domain.

Modern B2B outbound sales has shifted away from static contact databases and cold email blasting. High-performing revenue teams and autonomous AI SDRs rely on trigger events: measurable changes in a target account's behavior that indicate active growth, organizational change, and budget allocation.

Among these triggers, hiring velocity is one of the strongest signals of buying intent. When a company aggressively expands its headcount, it simultaneously purchases software licenses, hardware, onboarding tools, compliance services, and office infrastructure.

The challenge is aggregating hiring data alongside complementary buying signals. Looking up job boards, checking whether the company is actively running paid ads, and checking organic search traffic across 200 prospective accounts usually requires four different tools and extensive manual data wrangling.

The [Company Intent Radar](https://edtool79-collab.github.io/hirepulse-tools/company-intent-signals-api/) combines these critical growth metrics into a single API call per company domain. It audits hiring across six modern ATS platforms, checks active Google Ads campaigns, inspects organic search trends, and resolves MX email infrastructure, summarizing the account with an actionable 0–100 intent score.

## Multi-dimensional intent signals per company

When you pass a list of domains (such as `stripe.com` and `notion.so`), the API checks four primary growth indicators:

1. **Hiring velocity:** Total open job requisitions and new jobs opened within the last 30 days, audited across Greenhouse, Lever, Ashby, Workable, Recruitee, and SmartRecruiters.
2. **Paid ad investment:** Whether the company is actively running Google Ads right now, and the total volume of active ad creatives.
3. **Organic search momentum:** Estimated monthly organic search traffic and search trajectory.
4. **Email infrastructure:** The primary mail provider resolved from DNS MX records (e.g., Google Workspace, Microsoft 365).
5. **Composite Intent Score:** A normalized 0–100 score reflecting total growth momentum, accompanied by a concise, machine-readable summary suitable for LLMs and automated prompt injection.

## Quick start with cURL

You can query company intent signals synchronously using Apify's API endpoint:

```bash
curl --fail-with-body -X POST "https://api.apify.com/v2/acts/hirepulse~company-intent-radar/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "domains": [
    "stripe.com",
    "notion.so"
  ],
  "country": "US"
}'
```

The endpoint processes the submitted domains, synthesizes the multi-signal audit, and returns structured records directly in the JSON response.

## Inspecting a real intent record: Stripe

Here is an example record from a verified test run inspecting `stripe.com`:

```json
{
  "domain": "stripe.com",
  "intent_score": 85,
  "open_jobs": 727,
  "ads_running_now": true,
  "email_provider": "Google Workspace"
}
```

This single payload instantly qualifies the account:
- With 727 open roles, Stripe is in an aggressive hiring phase across multiple engineering and go-to-market teams.
- An active Google Ads footprint demonstrates ongoing paid acquisition investment.
- An intent score of 85 places the account in the highest tier of commercial activity.
- The `Google Workspace` MX signature identifies their core communication tech stack.

## Building a Python lead qualification pipeline

Below is a Python script that enriches an account list, segments companies by intent score, and prepares high-priority accounts for targeted outreach:

```bash
pip install apify-client
```

```python
import os
import json
from pathlib import Path
from apify_client import ApifyClient

# Initialize the Apify client
client = ApifyClient(os.environ.get("APIFY_TOKEN", "YOUR_APIFY_TOKEN"))

# Target prospect domains to score
prospect_domains = [
    "stripe.com",
    "notion.so"
]

run_input = {
    "domains": prospect_domains,
    "country": "US"
}

# Run the Company Intent Radar Actor
run = client.actor("hirepulse/company-intent-radar").call(run_input=run_input)

if not run or run.get("status") != "SUCCEEDED":
    raise RuntimeError(f"Actor failed with status: {run.get('status')}")

# Iterate through dataset items
records = list(client.dataset(run["defaultDatasetId"]).iterate_items())
print(f"Audited intent signals for {len(records)} account(s).\n")

# Process and segment accounts
qualified_pipeline = []

for item in records:
    domain = item.get("domain", "Unknown")
    score = item.get("intent_score", 0)
    jobs = item.get("open_jobs", 0)
    ads_active = item.get("ads_running_now", False)
    email_stack = item.get("email_provider", "Unknown")

    # Segment accounts based on intent tier
    if score >= 70:
        tier = "Tier 1: High Intent (Immediate Outreach)"
    elif score >= 40:
        tier = "Tier 2: Moderate Intent (Nurture)"
    else:
        tier = "Tier 3: Low Intent (Monitor)"

    qualified_pipeline.append({
        "domain": domain,
        "tier": tier,
        "intent_score": score,
        "open_jobs": jobs,
        "running_ads": ads_active,
        "email_stack": email_stack
    })

    print(f"[{domain}] Intent Score: {score}/100 -> {tier}")
    print(f"  Open Jobs: {jobs:,} | Running Google Ads: {ads_active} | Email: {email_stack}\n")

# Save segmented pipeline
Path("qualified_accounts.json").write_text(
    json.dumps(qualified_pipeline, indent=2, ensure_ascii=False),
    encoding="utf-8"
)
```

## How to use intent signals in AI SDR workflows

When feeding intent data into AI agents (such as Claude, GPT-4, or Clay AI formulas), avoid vague instructions like "write an email about this company." Ground the prompt in the exact observed evidence:

```text
Target Account: stripe.com
Observed Data: 727 open roles across engineering and sales; active Google Ads campaigns; Google Workspace infrastructure.

Task: Draft a concise 3-sentence outreach note for our security automation platform. Reference their current hiring scale and tech stack directly. Do not invent company claims or flatter the prospect. Focus on streamlining security compliance during rapid headcount expansion.
```

By constraining the model to observed hiring volume and infrastructure data, the generated outreach is relevant, professional, and free of AI hallucinations.

## Limitations and pricing

- **Scope:** The API audits modern ATS boards (Greenhouse, Lever, Ashby, Workable, Recruitee, SmartRecruiters), Google Ads activity, organic search traffic, and MX records. It does not track private internal headcount reductions, private venture financing rounds, or internal procurement ticketing systems.
- **Pricing:** Billed at $0.03 per company report, charged only when a complete report is generated. On the free Apify tier, you can test hiring and email signals for up to 5 companies.

## Next steps

- [Open Company Intent Radar on the Apify Store](https://apify.com/hirepulse/company-intent-radar)
- Review full input documentation on the [tool page](https://edtool79-collab.github.io/hirepulse-tools/company-intent-signals-api/)
- Deep-dive into individual competitor ad creatives with [How to see every Google ad a competitor runs](https://edtool79-collab.github.io/hirepulse-tools/guides/competitor-google-ads/), or inspect individual ATS job postings in [Greenhouse, Lever and Ashby jobs API](https://edtool79-collab.github.io/hirepulse-tools/guides/greenhouse-lever-ashby-jobs-api/)

Source page: https://edtool79-collab.github.io/hirepulse-tools/guides/hiring-signals-for-sales/
