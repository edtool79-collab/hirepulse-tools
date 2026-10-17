# YouTube transcripts in bulk, with timestamps (API)

> Get transcripts of YouTube videos and Shorts in bulk, with timestamps, as JSON or plain text.

## What you get

- Bulk video URLs or IDs
- Timestamps per line
- Plain text or JSON output

## YouTube Transcript Scraper (`hirepulse/youtube-transcript-scraper`)

**Use it when:** You need transcripts of YouTube videos in bulk, with timestamps.

- MCP: `https://mcp.apify.com?tools=hirepulse/youtube-transcript-scraper`
- Apify Store: https://apify.com/hirepulse/youtube-transcript-scraper
- Page: https://edtool79-collab.github.io/hirepulse-tools/youtube-transcript-api/
- Price: $0.003 per delivered transcript. Videos without captions, unavailable videos and failed fetches are not charged.. Free Apify plan: the first 3 videos of each run.

### Input

| Field | Type | Required / default | Notes |
| --- | --- | --- | --- |
| `videos` | array of strings | required | Video URLs or IDs. |
| `language` | string | optional | Transcript language. |
| `include_timestamps` | boolean | default false |  |

Input of the test run below:

```json
{
  "videos": [
    "https://youtu.be/jNQXAC9IVRw"
  ],
  "include_timestamps": true
}
```

### Output example

One record from a real test run on 2026-10-15 (long text and lists shortened):

```json
{
  "video_id": "jNQXAC9IVRw",
  "url": "https://www.youtube.com/watch?v=jNQXAC9IVRw",
  "status": "ok",
  "title": "Me at the zoo",
  "channel": "jawed",
  "duration_seconds": 19,
  "language": "en",
  "is_auto_generated": false,
  "transcript": "All right, so here we are, in front of the elephants the cool thing about these guys is that they have really... really really long trunks and that's cool (baaaaaaaaaaahhh!!) and that's pretty much all there is to say",
  "word_count": 39,
  "note": null,
  "segments": [
    {
      "start": 1.2,
      "duration": 2.16,
      "text": "All right, so here we are, in front of the elephants"
    },
    {
      "start": 5.32,
      "duration": 2.66,
      "text": "the cool thing about these guys is that they have really..."
    },
    {
      "start": 7.97,
      "duration": 4.64,
      "text": "really really long trunks"
    }
  ]
}
```

## Connect

- Remote MCP server: `https://mcp.apify.com?tools=hirepulse/<tool-id>`; several tools are comma-separated.
- Authentication: OAuth in the browser, or the header `Authorization: Bearer <APIFY_TOKEN>`.
- Local (stdio): `npx -y @apify/actors-mcp-server --tools hirepulse/<tool-id>`, with `APIFY_TOKEN` in `env`.
- REST: `POST https://api.apify.com/v2/acts/hirepulse~<tool-id>/run-sync-get-dataset-items?token=<APIFY_TOKEN>` with the input as the JSON body.
- Every result is billed (pay per use, no subscription). Start with one query or domain, then scale up.

Source page: https://edtool79-collab.github.io/hirepulse-tools/youtube-transcript-api/
