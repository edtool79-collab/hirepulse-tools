# Company Contact Details API: Public Emails & Social Profiles

> Find publicly listed business contact information from company websites. Export corporate emails, phone numbers, contact forms, and social links.

## What you get

- Find publicly listed corporate emails, phone numbers, and inquiry forms
- Extract official company social profiles (LinkedIn, GitHub, X/Twitter)
- Inspect DNS and MX email infrastructure
- Zero-scraping privacy: only publicly accessible business contact information

## Company Contacts Finder (`hirepulse/company-contact-details-finder`)

**Use it when:** You need publicly accessible corporate emails, inquiry forms, phone numbers, or social media links from company domains.

**Not for:** Private personal cell numbers or unverified leaked email lists.

- MCP: `https://mcp.apify.com?tools=hirepulse/company-contact-details-finder`
- Apify Store: https://apify.com/hirepulse/company-contact-details-finder
- Page: https://edtool79-collab.github.io/hirepulse-tools/company-contacts-api/
- Price: $0.005 per domain checked + $0.001 per public contact found.

### Input

| Field | Type | Required / default | Notes |
| --- | --- | --- | --- |
| `domains` | array of strings | required | Company domains to search for public contacts. |

Example input:

```json
{
  "domains": [
    "stripe.com",
    "vercel.com"
  ]
}
```

### Output example

Selected fields of one record from a real test run:

```json
{
  "domain": "stripe.com",
  "contacts": [
    {
      "type": "email",
      "value": "support@stripe.com",
      "label": "Support"
    },
    {
      "type": "email",
      "value": "press@stripe.com",
      "label": "Press"
    },
    {
      "type": "social",
      "value": "https://twitter.com/stripe",
      "label": "X / Twitter"
    }
  ]
}
```

## Connect

- Remote MCP server: `https://mcp.apify.com?tools=hirepulse/<tool-id>`; several tools are comma-separated.
- Authentication: OAuth in the browser, or the header `Authorization: Bearer <APIFY_TOKEN>`.
- Local (stdio): `npx -y @apify/actors-mcp-server --tools hirepulse/<tool-id>`, with `APIFY_TOKEN` in `env`.
- REST: `POST https://api.apify.com/v2/acts/hirepulse~<tool-id>/run-sync-get-dataset-items?maxTotalChargeUsd=0.10&restartOnError=false` with the input as the JSON body and `Authorization: Bearer <APIFY_TOKEN>` in the header. Start with one query or domain.
- Billing depends on the tool and delivered events; see its price and free-plan limits. Actor-start charges also apply. Inspect an existing run after a timeout before retrying a paid request.

Source page: https://edtool79-collab.github.io/hirepulse-tools/company-contacts-api/
