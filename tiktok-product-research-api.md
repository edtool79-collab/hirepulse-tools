# TikTok Product Research & Video Growth Radar

Research the TikTok attention behind a product before spending more time on it.
Get linked videos, creator-account breadth, an explainable research score and
saved history. Same-video measurements separate actual added views from large
lifetime counts. This follows a bounded product-video sample, not all TikTok.

- Store: https://apify.com/hirepulse/viral-product-radar
- Page: https://edtool79-collab.github.io/hirepulse-tools/tiktok-product-research-api/
- Apify MCP: https://mcp.apify.com?tools=hirepulse/viral-product-radar
- Price: $0.02 per delivered report; Clockworks collection is separate and capped ($0.04 total by default).

## First run

1. Start with one product, such as `mini projector`.
2. Keep Live videos via Clockworks. Review the total collection cap and check
   **I allow the separately capped Clockworks collection charge**. It is off by default.
3. Start the Actor; open REPORT for the readable report or OUTPUT for source evidence.
4. Reuse the same `state_id` after at least six hours to compare the same videos.
   First collection is a baseline, not a growth alert.

One product report with ten collected videos is about $0.05 at the checked source
price ($0.02 report + $0.03 collection). The default $0.04 source cap permits at
most $0.06 in report plus source events for ONE product. Multiple product reports
cost $0.02 EACH; the collection cap is shared across the entire run. Upstream
failures can still incur source charges; an empty result has no report event.
Review current provider pricing. No monthly subscription or startup fee is configured.

```json
{
  "keywords": [
    "mini projector"
  ],
  "analysis_mode": "product_videos",
  "upstream_source": "clockworks",
  "allow_paid_upstream": true,
  "upstream_max_charge_usd": 0.04,
  "max_items": 10,
  "state_id": "my-product-research",
  "deliver_all_reports": true
}
```

The JSON example explicitly opts into collection. An API request without consent
does not silently start a paid provider. With no usable export it returns
`configuration_required` and setup instructions before collection.

## Use an existing export

Select Existing video export (`upstream_source=public`) and supply `video_snapshot`:
its original `observed_at`, a source label and up to100 records. There is no
collection-provider call for imports. Do not change the observation timestamp to
make old counters appear fresh. Direct anonymous collection is not supported in
the cloud product-video workflow.

## Evidence for people and agents

- Matching video URLs, public counters and original observation times.
- Creator-account breadth, concentration and same-video growth where comparable.
- Baseline/watch/candidate classification, blockers and next research actions.
- JSON results and an HTML report; stable watchlist history for later comparisons.

The score is a research heuristic, not a probability of virality or a prediction
of sales, conversion, profit or TikTok Shop demand. Public creator accounts are
not verified independent businesses. No Shop sales or ad-spend feed is included.

## API and billing limits

Use the Apify API or its MCP server with this Actor; the independent HirePulse
gateway catalog is separate. Keep API tokens in Authorization headers or SDK
configuration, never in published URLs. `maxTotalChargeUsd` on the parent limits
report events; `upstream_max_charge_usd` separately caps Clockworks collection.
Inspect an existing run after a timeout before launching another paid run.
