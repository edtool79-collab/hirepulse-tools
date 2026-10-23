#!/usr/bin/env python3
"""
HERMES AUTONOMOUS GROWTH RUNNER (Model-Agnostic Engine)
------------------------------------------------------
Autonomously generates, verifies, and deploys high-impact developer guides
for https://edtool79-collab.github.io/hirepulse-tools/

Supports ANY language model via:
1. Standard OpenAI-compatible API (OpenAI, OpenRouter, DeepSeek, Groq, Ollama, vLLM)
   Configured via: LLM_API_KEY / OPENAI_API_KEY, LLM_BASE_URL / OPENAI_BASE_URL, LLM_MODEL / OPENAI_MODEL
2. Google Gemini REST API
   Configured via: GEMINI_API_KEY, GEMINI_MODEL

Usage:
  python hermes_runner.py --once
  python hermes_runner.py --topic "custom topic" --tool "ats-jobs-api"
  python hermes_runner.py --cron-loop 6
  python hermes_runner.py --status
  python hermes_runner.py --dry-run
"""

import os
import sys
import json
import time
import shutil
import argparse
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# Windows console encoding safeguard
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Configuration Paths
ASTRO_DIR = Path(r"C:\Users\sales\agy-inbox\astro-site")
SITE_REPO_DIR = Path(r"c:\Users\sales\Downloads\גדכגד\site-repo")
GUIDES_DATA_PATH = ASTRO_DIR / "src" / "data" / "guides.json"
GUIDES_CONTENT_DIR = ASTRO_DIR / "src" / "content" / "guides"
LLMS_TXT_PATH = ASTRO_DIR / "public" / "llms.txt"
STATE_FILE = ASTRO_DIR / "hermes_state.json"

# High-Intent Curated Topic Ideas Pool
PREVETTED_TOPIC_QUEUE = [
    {
        "slug": "scrape-greenhouse-jobs-python-no-key",
        "tool": "ats-jobs-api",
        "category": "Hiring",
        "title": "Scrape Greenhouse Jobs with Python Without Employer API Keys",
        "description": "Extract structured job listings, compensation ranges, and tech stacks directly from Greenhouse boards using Python and clean JSON.",
        "related": ["greenhouse-lever-ashby-jobs-api", "google-jobs-json-python"]
    },
    {
        "slug": "track-competitor-google-ads-n8n",
        "tool": "google-ads-transparency-api",
        "category": "Automation",
        "title": "Automate Competitor Google Ad Alerts in n8n with Real-Time Slack Notifications",
        "description": "Build an automated n8n workflow that monitors competitor Google Ads Transparency updates and alerts your marketing team in Slack.",
        "related": ["competitor-google-ads", "n8n-data-api-workflow"]
    },
    {
        "slug": "youtube-transcript-rag-chromadb",
        "tool": "youtube-transcript-api",
        "category": "Transcripts",
        "title": "Chunk YouTube Transcripts for LangChain and ChromaDB RAG Pipelines",
        "description": "Download bulk YouTube transcripts with timestamps, segment into semantic chunks, and build a local vector search index using ChromaDB.",
        "related": ["bulk-youtube-transcripts-rag", "ai-agent-live-data-mcp"]
    },
    {
        "slug": "b2b-lead-enrichment-clay-alternative",
        "tool": "b2b-account-research-api",
        "category": "Company research",
        "title": "Self-Hosted Clay Alternative: B2B Lead Enrichment for $0.05 per Account",
        "description": "Replace expensive B2B data waterfalls with an automated pipeline combining hiring signals, detected tech stack, and ad activity.",
        "related": ["hiring-signals-for-sales", "n8n-data-api-workflow"]
    },
    {
        "slug": "cursor-ide-live-mcp-data-setup",
        "tool": "ai-visibility-radar",
        "category": "AI agents",
        "title": "Connect Cursor IDE to Live Web & Company Intelligence via Apify MCP",
        "description": "Configure Cursor with Model Context Protocol to query live website tech stacks, hiring intent, and robots.txt audits directly inside your IDE.",
        "related": ["ai-agent-live-data-mcp", "keyword-search-volume-api"]
    },
    {
        "slug": "audit-website-crawler-readiness-perplexity",
        "tool": "ai-visibility-radar",
        "category": "AI visibility",
        "title": "How to Audit Website Crawler Access for Perplexity, ChatGPT and ClaudeBot",
        "description": "Inspect robots directives, llms.txt endpoints, and JSON-LD markup to ensure your site is discoverable by agentic search engines.",
        "related": ["ai-agent-live-data-mcp", "domain-seo-overview-python"]
    },
    {
        "slug": "ecommerce-dropshipping-price-monitor-python",
        "tool": "aliexpress-search-api",
        "category": "Commerce",
        "title": "Build an Automated AliExpress Price & Sold-Count Tracker in Python",
        "description": "Track e-commerce product price variations, discount changes, and sales velocity over time with lightweight plain-HTTP requests.",
        "related": ["aliexpress-search-python", "keyword-search-volume-api"]
    },
    {
        "slug": "detect-applicant-tracking-systems-python",
        "tool": "ats-detector-api",
        "category": "Hiring",
        "title": "Detect ATS Job Board Providers from Company Domains with Python",
        "description": "Identify whether a prospect uses Greenhouse, Lever, Ashby, or Workable to enrich recruiting pipelines and target HR tech sales.",
        "related": ["greenhouse-lever-ashby-jobs-api", "hiring-signals-for-sales"]
    }
]

SYSTEM_PROMPT = """You are Hermes, the Autonomous Lead Technical Growth Engineer for HirePulse (https://edtool79-collab.github.io/hirepulse-tools/).
Generate an authoritative, production-grade technical MDX guide for the requested topic.

Strict Requirements:
1. Output MUST be a valid JSON object with exactly two keys:
   - "metadata": {"slug": str, "tool": str, "category": str, "title": str, "description": str, "related": [str, str]}
   - "mdx_content": str
2. MDX must start with frontmatter (title and description), followed by:
   import { href } from '../../lib/site';
3. Use <a href={href('tool-slug/')}>Tool Name</a> for tool references.
4. Internal links must use trailing slashes.
5. Headings must be level 2 (##) to support the sidebar TOC.
6. Provide a verified cURL request and a complete, production-ready Python script using apify-client.
7. Include explicit, honest technical limitations matching HirePulse catalog standards.
8. Do NOT wrap JSON in markdown backticks if possible, return raw parseable JSON string."""

def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"published_slugs": [], "history": []}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

class ModelClient:
    """Model-agnostic LLM caller supporting OpenAI-compatible and Gemini APIs."""
    def __init__(self, model=None, api_key=None, api_base=None):
        self.api_key = api_key or os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        self.api_base = api_base or os.environ.get("LLM_BASE_URL") or os.environ.get("OPENAI_BASE_URL")
        self.model = model or os.environ.get("LLM_MODEL") or os.environ.get("OPENAI_MODEL") or os.environ.get("GEMINI_MODEL")

        # Auto-detect mode
        if not self.api_base and os.environ.get("GEMINI_API_KEY") and not os.environ.get("OPENAI_API_KEY"):
            self.mode = "gemini"
            if not self.model:
                self.model = "gemini-2.0-flash"
        else:
            self.mode = "openai_compatible"
            if not self.api_base:
                self.api_base = "https://api.openai.com/v1"
            if not self.model:
                self.model = "gpt-4o-mini"

    def generate(self, user_prompt: str) -> str:
        if not self.api_key:
            raise ValueError(
                "No API Key found! Set LLM_API_KEY, OPENAI_API_KEY, or GEMINI_API_KEY in your environment, "
                "or pass --api-key <key> on the command line."
            )

        if self.mode == "gemini":
            return self._call_gemini(user_prompt)
        return self._call_openai_compatible(user_prompt)

    def _call_openai_compatible(self, user_prompt: str) -> str:
        endpoint = f"{self.api_base.rstrip('/')}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        if "openrouter.ai" in endpoint:
            headers["HTTP-Referer"] = "https://edtool79-collab.github.io/hirepulse-tools/"
            headers["X-Title"] = "Hermes Growth Agent"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Task: {user_prompt}"}
            ],
            "temperature": 0.2
        }

        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8")
            raise RuntimeError(f"OpenAI-Compatible API HTTP Error {e.code}: {err_msg}")

    def _call_gemini(self, user_prompt: str) -> str:
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": f"{SYSTEM_PROMPT}\n\nTask: {user_prompt}"}]}
            ],
            "generationConfig": {
                "temperature": 0.2,
                "responseMimeType": "application/json"
            }
        }
        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8")
            raise RuntimeError(f"Gemini API HTTP Error {e.code}: {err_msg}")

def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
    return res.returncode, res.stdout, res.stderr

def build_and_verify():
    print(f"[*] Running verification build in {ASTRO_DIR}...")
    code, out, err = run_cmd("cmd /c npm run build", cwd=ASTRO_DIR)
    if code != 0:
        print("[!] Build failed!")
        print(err or out)
        return False
    print("[+] Verification build succeeded!")
    return True

def sync_and_publish(slug, title):
    print(f"[*] Syncing build artifacts to {SITE_REPO_DIR}...")
    dist_dir = ASTRO_DIR / "dist"
    if not dist_dir.exists():
        raise FileNotFoundError(f"Dist dir {dist_dir} does not exist.")

    # Copy dist to static repo excluding .git
    run_cmd(f'robocopy "{dist_dir}" "{SITE_REPO_DIR}" /E /XD .git /R:1 /W:1')

    print("[*] Staging git changes in distribution repo...")
    run_cmd("git add .", cwd=SITE_REPO_DIR)
    commit_msg = f"feat(guide): publish {slug} - {title} [hermes-autonomous]"
    run_cmd(f'git commit -m "{commit_msg}"', cwd=SITE_REPO_DIR)
    
    print("[*] Pushing to origin main...")
    code, out, err = run_cmd("git push origin main", cwd=SITE_REPO_DIR)
    if code != 0:
        print(f"[!] Warning: Git push exited with code {code}: {err or out}")
    else:
        print("[+] Git push successful!")

    # IndexNow Ping
    ping_indexnow(slug)

def ping_indexnow(slug):
    canonical_url = f"https://edtool79-collab.github.io/hirepulse-tools/guides/{slug}/"
    print(f"[*] Pinging IndexNow for {canonical_url}...")
    payload = {
        "host": "edtool79-collab.github.io",
        "key": "4b8c9d2e1a3f5076b9e8d7c6b5a41234",
        "keyLocation": "https://edtool79-collab.github.io/hirepulse-tools/4b8c9d2e1a3f5076b9e8d7c6b5a41234.txt",
        "urlList": [canonical_url]
    }
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            print(f"[+] IndexNow ping response: {res.status}")
    except Exception as e:
        print(f"[-] IndexNow ping non-fatal notice: {e}")

def execute_generation_cycle(topic_spec=None, client=None, dry_run=False):
    if client is None:
        client = ModelClient()

    state = load_state()
    published = set(state.get("published_slugs", []))

    if not topic_spec:
        for candidate in PREVETTED_TOPIC_QUEUE:
            if candidate["slug"] not in published:
                topic_spec = candidate
                break

    if not topic_spec:
        print("[*] All pre-vetted topics have been published! Provide a custom topic with --topic.")
        return False

    slug = topic_spec["slug"]
    print(f"\n=======================================================")
    print(f"[*] Starting Hermes Growth Cycle: {slug}")
    print(f"[*] Tool: {topic_spec['tool']} | Category: {topic_spec['category']}")
    print(f"[*] Model Engine: {client.model} ({client.mode})")
    print(f"=======================================================\n")

    guides_json = json.loads(GUIDES_DATA_PATH.read_text(encoding="utf-8"))
    
    prompt = f"""Create a technical guide for:
Title: {topic_spec['title']}
Slug: {slug}
Tool Slug: {topic_spec['tool']}
Category: {topic_spec['category']}
Meta Description: {topic_spec['description']}
Related: {json.dumps(topic_spec.get('related', []))}
"""
    print("[*] Requesting completion from LLM...")
    raw_response = client.generate(prompt)

    try:
        data = json.loads(raw_response)
    except Exception:
        clean_text = raw_response.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        data = json.loads(clean_text)

    metadata = data["metadata"]
    mdx_content = data["mdx_content"]

    # Write MDX file
    mdx_file = GUIDES_CONTENT_DIR / f"{slug}.mdx"
    print(f"[*] Writing MDX to {mdx_file}...")
    mdx_file.write_text(mdx_content, encoding="utf-8")

    # Update guides.json
    print(f"[*] Appending entry to {GUIDES_DATA_PATH}...")
    guides_json.append(metadata)
    GUIDES_DATA_PATH.write_text(json.dumps(guides_json, indent=2, ensure_ascii=False), encoding="utf-8")

    # Verify with build
    build_ok = build_and_verify()

    if not build_ok:
        print("[!] Build verification failed. Rolling back changes...")
        if mdx_file.exists():
            mdx_file.unlink()
        reverted_guides = [g for g in guides_json if g["slug"] != slug]
        GUIDES_DATA_PATH.write_text(json.dumps(reverted_guides, indent=2, ensure_ascii=False), encoding="utf-8")
        print("[!] Rollback complete. Aborting cycle.")
        return False

    if dry_run:
        print("[*] Dry run mode enabled: Reverting build files and skipping git push.")
        if mdx_file.exists():
            mdx_file.unlink()
        reverted_guides = [g for g in guides_json if g["slug"] != slug]
        GUIDES_DATA_PATH.write_text(json.dumps(reverted_guides, indent=2, ensure_ascii=False), encoding="utf-8")
        print("[+] Dry run test succeeded cleanly!")
        return True

    # Append to llms.txt non-destructively
    if LLMS_TXT_PATH.exists():
        llms_text = LLMS_TXT_PATH.read_text(encoding="utf-8")
        guide_url = f"https://edtool79-collab.github.io/hirepulse-tools/guides/{slug}/"
        new_entry = f"- [{metadata['title']}]({guide_url}): {metadata['description']}\n"
        if slug not in llms_text:
            llms_text += new_entry
            LLMS_TXT_PATH.write_text(llms_text, encoding="utf-8")
            print("[+] Updated public/llms.txt")

    # Sync and push
    sync_and_publish(slug, metadata["title"])

    # Update State
    state["published_slugs"].append(slug)
    state["history"].append({
        "slug": slug,
        "title": metadata["title"],
        "tool": metadata["tool"],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })
    save_state(state)
    print(f"\n[✓] Successfully published and indexed guide: {slug}\n")
    return True

def main():
    parser = argparse.ArgumentParser(description="Hermes Model-Agnostic Growth Runner")
    parser.add_argument("--once", action="store_true", help="Execute one autonomous publication cycle")
    parser.add_argument("--cron-loop", type=int, help="Run continuously with an interval of N hours")
    parser.add_argument("--topic", type=str, help="Custom topic title")
    parser.add_argument("--tool", type=str, help="Canonical tool slug for custom topic")
    parser.add_argument("--category", type=str, default="Automation", help="Category for custom topic")
    parser.add_argument("--status", action="store_true", help="Show published topics and queue status")
    parser.add_argument("--dry-run", action="store_true", help="Generate and test build without git commit/push")
    parser.add_argument("--model", type=str, help="LLM model name (overrides env)")
    parser.add_argument("--api-base", type=str, help="Base URL for OpenAI-compatible endpoint")
    parser.add_argument("--api-key", type=str, help="API Key for the model provider")

    args = parser.parse_args()

    client = ModelClient(model=args.model, api_key=args.api_key, api_base=args.api_base)

    if args.status:
        state = load_state()
        print("=== HERMES GROWTH AGENT STATUS ===")
        print(f"Engine Model: {client.model} ({client.mode})")
        print(f"Total Published: {len(state.get('published_slugs', []))}")
        for item in state.get("history", []):
            print(f" - [{item['timestamp']}] {item['slug']} ({item['tool']})")
        return

    if args.topic:
        if not args.tool:
            print("Error: --tool is required when specifying a custom --topic")
            sys.exit(1)
        custom_slug = args.topic.lower().replace(" ", "-").replace("&", "and")
        topic_spec = {
            "slug": custom_slug,
            "tool": args.tool,
            "category": args.category,
            "title": args.topic,
            "description": f"Comprehensive guide to {args.topic} using HirePulse APIs and Python.",
            "related": ["ai-agent-live-data-mcp", "n8n-data-api-workflow"]
        }
        execute_generation_cycle(topic_spec, client=client, dry_run=args.dry_run)
        return

    if args.once:
        execute_generation_cycle(client=client, dry_run=args.dry_run)
        return

    if args.cron_loop:
        interval_sec = args.cron_loop * 3600
        print(f"[*] Starting Hermes loop every {args.cron_loop} hours ({interval_sec}s)...")
        while True:
            try:
                execute_generation_cycle(client=client, dry_run=args.dry_run)
            except Exception as e:
                print(f"[!] Cycle error: {e}")
            print(f"[*] Sleeping for {args.cron_loop} hours...")
            time.sleep(interval_sec)

    parser.print_help()

if __name__ == "__main__":
    main()
