# Website SEO checks in Python: metadata and sitemaps

Verified 2026-10-28. For SEO consultants and agencies preparing an initial website review. Collect page metadata and sitemap observations in structured JSON.

[Open Actor](https://apify.com/hirepulse/domain-seo-overview?utm_source=hirepulse_docs&utm_medium=owned&utm_campaign=apify_quickstart_20261028&utm_content=domain-seo-overview)

## Input

```json
{
  "domains": [
    "linear.app"
  ],
  "top_keywords": 0,
  "competitors": 0,
  "use_paid_upstream": false
}
```

## Run in Python

Download [runner](https://edtool79-collab.github.io/hirepulse-tools/examples/apify-bounded-run.py) and [input](https://edtool79-collab.github.io/hirepulse-tools/examples/domain-seo-overview.json).

```bash
pip install requests
# Set APIFY_TOKEN in your environment; never paste it into this website.
python apify-bounded-run.py hirepulse/domain-seo-overview domain-seo-overview.json 0.03
```

## Captured owner output

Captured 2026-11-03T21:13:51.694Z, Build L3gaycRDgsSc84gMz (v1.5.1). Selected fields, not customer results or current measurements.

```json
{
  "record_type": "domain_overview",
  "domain": "linear.app",
  "final_url": "https://linear.app/",
  "http_status": 200,
  "page_title": "Linear — The system for product development",
  "canonical_url": null,
  "h1": "Linear is a purpose-built tool for planning and building products",
  "checked_at": "2026-11-03T21:13:51.694100+00:00",
  "sitemap_present": true,
  "sitemap_urls_found": 985,
  "popularity_tier": "top_50k",
  "popularity_source": "Chrome UX Report (Google), 2026-09",
  "provider_mode": "native",
  "metrics_available": false,
  "seo_readiness": {
    "score": 90,
    "tier": "good"
  },
  "findings": [
    {
      "code": "missing_canonical",
      "severity": "low",
      "message": "No canonical link tag was found on the homepage.",
      "recommendation": "Add <link rel=\"canonical\" href=\"...\"> to the <head> to prevent duplicate content across URL variants.",
      "evidence": "canonical link tag missing"
    }
  ]
}
```

## Cost and limits

Public mode emits no domain-lookup or domain-result events. The listed Actor start event is $0.00005 per GB, minimum one event; applicable Apify platform charges can apply. A spending cap is a limit, not a quoted price.

Native mode does not measure visits, Google rankings, search volume or CPC. Those fields remain null. The Chrome popularity bucket is not a visit count. A sitemap count is not a Google index count.

Use the result to prioritize a manual review. For measured SEO metrics, use a separately configured data provider; this example keeps paid sources disabled.
