# Generate an llms.txt draft from a Shopify product feed

Verified 2026-10-28. For store owners and ecommerce agencies that want a reviewable text index from an accessible Shopify or WooCommerce product feed.

[Open Actor](https://apify.com/hirepulse/shopify-to-llms-generator?utm_source=hirepulse_docs&utm_medium=owned&utm_campaign=apify_quickstart_20261028&utm_content=shopify-to-llms-generator)

## Input

```json
{
  "store_url": "https://www.untuckit.com",
  "max_products": 5
}
```

## Run in Python

Download [runner](https://edtool79-collab.github.io/hirepulse-tools/examples/apify-bounded-run.py) and [input](https://edtool79-collab.github.io/hirepulse-tools/examples/shopify-to-llms-generator.json).

```bash
pip install requests
# Set APIFY_TOKEN in your environment; never paste it into this website.
python apify-bounded-run.py hirepulse/shopify-to-llms-generator shopify-to-llms-generator.json 0.03
```

## Captured owner output

Captured 2026-10-28T09:51:36.755Z, Build UIbZf3heOD2LfAJJa. Selected fields, not customer results or current measurements.

```json
{
  "store_url": "https://www.untuckit.com",
  "platform": "Shopify",
  "crawl_status": "SUCCESS_SHOPIFY",
  "products_indexed": 5,
  "deployed": false,
  "ucp_conformant": false,
  "llms_txt_excerpt": "# Untuckit\n> Draft based on a sampled public catalog; review before publishing.\n\n## Sources\n- [Store](https://www.untuckit.com)\n\n## Sampled Products\n- [Full-Zip CPO Jacket](https://www.untuckit.com/products/raphael-boiled-wool): Currency unknown 158.00 (In Stock) — Like many timeless looks, this sharp jacket is inspired by a heritage military style: the wool jackets once worn by U.S. Navy Chief Petty Officers on patrol. The warm, supersoft wool blend offers just enough stretch to let you move comfortably all da\n- [Full-Zip CPO Jacket](https://www.untuckit.com/products/corwin): Currency unknown 158.00 (In Stock) — Like many timeless looks, this sharp jacket is inspired by a heritage military style: the wool jackets once worn by U.S. Navy Chief Petty Officers on patrol. The warm, supersoft wool blend offers just enough stretch to let you move comfortably all da\n- [Knit Overshirt - FINAL SALE](https://www.untuckit.com/products/garavelle-knit-overshirt-sky-captain): Currency unknown 45.00 (Out of Stock) — When it’s brisk but not freezing, our Knit Overshirts make easy, warm layers that look good over any tee or Henley. Yet, they're light enough to layer under a jacket. Featuring soft 100% cotton that's knit for an easy feel, throw on one for your next\n- [Performance Short-Sleeve Vandelay Shirt - FINAL SALE](https://www.untuckit.com/products/vandelay): Currency unknown 45.00 (Out of"
}
```

## Cost and limits

$0.02 per delivered report containing at least one product, charged per report rather than per product. No billable dataset report for blocked or empty feeds. Applicable platform storage access charges may apply.

Protected or empty feeds can return diagnostics without a catalog report. The sample is capped at five products, not a full inventory. The Actor does not publish files, add checkout support or verify policies. An llms.txt file does not guarantee citations, AI visibility or sales.

Download LLMS_TXT_DRAFT from the run key-value store or read llms_txt in the report. Check product URLs and wording, then decide whether to publish the file yourself. The Actor never deploys to your website.
