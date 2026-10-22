# Domain SEO API: inspect public website metadata

> Inspect metadata, sitemap observations and autocomplete suggestions; native mode does not measure traffic or rankings.

# Inspect website evidence before an SEO audit

Domain SEO Overview currently offers a public-evidence preview: website titles, meta descriptions, sitemap observations and autocomplete suggestions. This is useful for initial website triage, not for measuring a company's search performance.

## What the current mode cannot measure

Organic traffic, ranking positions, keyword search volumes, CPC and traffic value require a separately configured SEO data source. They remain null in the native preview. Autocomplete suggestions are neither ranking keywords nor search-volume measurements. A sitemap count is not Google's indexed-page count.

## Start with a bounded example

Open the Actor at https://apify.com/hirepulse/domain-seo-overview and use:

```json
{"domains":["example.com"],"country":"US","top_keywords":0,"competitors":0,"use_paid_upstream":false}
```

For REST, use the Apify API endpoint `POST /v2/acts/hirepulse~domain-seo-overview/run-sync-get-dataset-items`, pass your Apify token in the Authorization Bearer header and set `maxTotalChargeUsd=0.10&restartOnError=false`. These are instructions; this page does not run anything.

## Pricing and output

The native mode does not emit custom domain-lookup or domain-result charge events. The Actor start event and applicable Apify charges still apply, so this is not a promise of a free run. Review the live Pricing tab before starting. Keep `use_paid_upstream=false` for the preview.

Read `provider_mode`, `metrics_available`, `data_source` and `note` in the returned JSON. Public example Output tables show column definitions and can include fields that are null in this mode; they are not measured sample data. A dated, actual owner-run sample is shown on the Domain SEO tool page and in `samples/domain-seo.json`.

The separate HirePulse gateway at https://gethirepulse.xyz/mcp has its own tools and x402 prices. An Apify purchase does not provide prepaid gateway credit.

Source page: https://edtool79-collab.github.io/hirepulse-tools/guides/domain-seo-overview-python/
