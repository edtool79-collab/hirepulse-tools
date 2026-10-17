# Fix YouTube Transcript IP Blocks & RAG Extraction

> Download YouTube transcripts in bulk with timestamps and bypass IP blocks. Extract clean chunks for LangChain, LlamaIndex, Chroma and RAG.

Video is one of the densest repositories of domain expertise on the web—from conference keynotes and engineering tech talks to product teardowns and tutorial videos. However, ingesting video content into modern AI pipelines and Retrieval-Augmented Generation (RAG) knowledge bases is notoriously cumbersome.

Running speech-to-text models like Whisper locally requires GPU compute, takes significant processing time, and speech-to-text cloud APIs typically cost $0.006+ per audio minute. For a 60-minute technical talk, that adds both latency and ongoing expense. Furthermore, raw audio transcription often loses the alignment between the spoken text and the precise video timeline.

The [YouTube Transcript Scraper](https://edtool79-collab.github.io/hirepulse-tools/youtube-transcript-api/) extracts public captions and transcripts directly from YouTube's video backend in seconds. It accepts video URLs or IDs in bulk, works on standard long-form videos as well as YouTube Shorts, and returns timestamped lines in clean JSON or plain text.

## Fixing youtube-transcript-api IpBlocked and 429 errors in Python

If you have used open-source libraries like `youtube-transcript-api` in production (e.g. deployed on AWS EC2, Heroku, or DigitalOcean), you have almost certainly encountered the infamous `IpBlocked` or HTTP 429 rate-limit exception (documented extensively in GitHub Issue #272). YouTube aggressively flags and blocks standard cloud datacenter IP subnets.

Developers frequently try to solve this with manual residential proxy rotation or spinning up headless Chromium clusters, which adds severe latency, failure points, and infrastructure overhead. The [YouTube Transcript Scraper](https://edtool79-collab.github.io/hirepulse-tools/youtube-transcript-api/) solves this by managing residential sessions and rotating request routing behind the scenes, allowing you to extract timestamped captions for large batches of videos without maintaining your own proxy infrastructure.

## Why timestamps matter for AI and RAG

In a production RAG system, an LLM should never answer a user query without citing verifiable sources. When an answer is derived from a 45-minute conference lecture, pointing the user to the video URL alone is not enough—they need the exact second where the speaker made the claim.

By preserving timestamps for every transcript segment:
- Your chunking pipeline can attach `start_seconds` and `duration` metadata to every embedded vector chunk.
- When an LLM generates a response, it can generate direct deep-link citations formatted as `https://youtube.com/watch?v=VIDEO_ID&t=142s`.
- Users can click the citation and immediately jump to the exact timestamp in the video player to verify the model's claim.

## Quick start with cURL

You can query transcripts via Apify's synchronous API endpoint:

```bash
curl --fail-with-body -X POST "https://api.apify.com/v2/acts/hirepulse~youtube-transcript-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "videos": [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  ]
}'
```

You can pass standard watch URLs, short links (`youtu.be/...`), Shorts URLs, or plain 11-character video IDs.

## Building a Python chunking pipeline for vector search

Below is a Python script that pulls transcripts in bulk, organizes them into timestamp-aware text chunks suitable for embedding models (such as OpenAI, Cohere, or sentence-transformers), and formats deep links for citations:

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

# Target YouTube video URLs or IDs
target_videos = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
]

run_input = {
    "videos": target_videos
}

# Run the YouTube Transcript Scraper Actor
run = client.actor("hirepulse/youtube-transcript-scraper").call(run_input=run_input)

if not run or run.get("status") != "SUCCEEDED":
    raise RuntimeError(f"Actor failed with status: {run.get('status')}")

# Iterate through dataset items
records = list(client.dataset(run["defaultDatasetId"]).iterate_items())
print(f"Extracted transcripts for {len(records)} video(s).\n")

# Process transcript lines into timestamp-anchored RAG chunks
rag_documents = []

for record in records:
    video_id = record.get("video_id", "unknown")
    video_url = record.get("video_url", f"https://www.youtube.com/watch?v={video_id}")
    transcript_segments = record.get("transcript", [])

    # If transcript is a list of lines with timestamps
    current_chunk = []
    chunk_start_time = 0
    words_in_chunk = 0

    for seg in transcript_segments:
        text = seg.get("text", "").strip()
        start = seg.get("start", 0)

        if not current_chunk:
            chunk_start_time = int(start)

        current_chunk.append(text)
        words_in_chunk += len(text.split())

        # When chunk reaches ~150 words, create a RAG document chunk
        if words_in_chunk >= 150:
            chunk_text = " ".join(current_chunk)
            citation_url = f"https://www.youtube.com/watch?v={video_id}&t={chunk_start_time}s"

            rag_documents.append({
                "video_id": video_id,
                "video_url": video_url,
                "start_seconds": chunk_start_time,
                "citation_url": citation_url,
                "content": chunk_text
            })

            current_chunk = []
            words_in_chunk = 0

    # Capture remaining text in last chunk
    if current_chunk:
        chunk_text = " ".join(current_chunk)
        rag_documents.append({
            "video_id": video_id,
            "video_url": video_url,
            "start_seconds": chunk_start_time,
            "citation_url": f"https://www.youtube.com/watch?v={video_id}&t={chunk_start_time}s",
            "content": chunk_text
        })

print(f"Generated {len(rag_documents)} timestamped document chunks ready for embedding.")
for doc in rag_documents[:3]:
    print(f"\n[Timestamp: {doc['start_seconds']}s | Citation: {doc['citation_url']}]")
    print(f"Text: {doc['content'][:140]}...")

# Save prepared RAG chunks
Path("youtube_rag_chunks.json").write_text(
    json.dumps(rag_documents, indent=2, ensure_ascii=False),
    encoding="utf-8"
)
```

## Architectural considerations for video ingestion

### 1. Ingestion speed and cost
Fetching existing caption tracks over HTTP takes less than 2 seconds per video, whereas downloading an audio stream and running an external transcription API consumes minutes of wall-clock time and ongoing cloud API costs. Using the transcript scraper as the first line of ingestion provides a high-throughput, low-cost pipeline.

### 2. Handling auto-generated vs. uploaded captions
YouTube transcripts include both creator-provided subtitle tracks and YouTube's automated speech recognition (ASR) captions. For technical videos with specialized jargon (like acronyms or code libraries), review whether critical domain terminology requires supplementary normalization or prompt context.

### 3. Preserving chunk boundaries
Avoid naive character slicing (e.g., splitting text blindly every 500 characters), which can slice words in half and disconnect sentences from their starting timestamps. Chunk based on natural transcript sentence breaks or fixed word windows, anchoring each chunk to the timestamp of its first line.

## Limitations and pricing

- **Availability:** The scraper retrieves transcripts and captions that exist on the requested YouTube video or Short. If a creator has explicitly disabled all captions and no automated transcript is available, the video will not have transcript text.
- **Pricing:** $0.003 per delivered transcript. Videos without captions, unavailable videos and failed fetches are not charged.

## Next steps

- [Open YouTube Transcript Scraper on the Apify Store](https://apify.com/hirepulse/youtube-transcript-scraper)
- View full parameters on the [tool page](https://edtool79-collab.github.io/hirepulse-tools/youtube-transcript-api/)
- Connect live video data to intelligent agents in [Give your AI agent live data with MCP](https://edtool79-collab.github.io/hirepulse-tools/guides/ai-agent-live-data-mcp/), or build an automated pipeline in [Build an n8n data API workflow](https://edtool79-collab.github.io/hirepulse-tools/guides/n8n-data-api-workflow/)

Source page: https://edtool79-collab.github.io/hirepulse-tools/guides/bulk-youtube-transcripts-rag/
