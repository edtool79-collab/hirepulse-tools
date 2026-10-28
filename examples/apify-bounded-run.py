"""One bounded Apify run. Never retries a run-start request."""
import json, os, sys, time
from pathlib import Path
import requests

actor, input_path, cap = sys.argv[1], sys.argv[2], float(sys.argv[3])
if not 0 < cap <= 1:
    raise SystemExit("Choose a positive event-charge cap up to $1 for this example.")
headers = {"Authorization": "Bearer " + os.environ["APIFY_TOKEN"]}
payload = json.loads(Path(input_path).read_text(encoding="utf-8"))
api = "https://api.apify.com/v2"
# This POST is deliberately not retried. If its response is lost, check
# Apify Console for the run before starting another one.
response = requests.post(api + "/actors/" + actor.replace("/", "~") + "/runs",
    headers=headers, json=payload, params={"maxTotalChargeUsd": cap,
    "timeout": 120, "memory": 512, "restartOnError": "false"}, timeout=35)
response.raise_for_status()
run = response.json()["data"]
print("Started run:", run["id"], flush=True)
deadline = time.monotonic() + 180
while run["status"] in {"READY", "RUNNING", "TIMING-OUT", "ABORTING"}:
    if time.monotonic() >= deadline:
        raise SystemExit("Polling stopped; inspect run " + run["id"] + " in Console.")
    time.sleep(2)
    response = requests.get(api + "/actor-runs/" + run["id"], headers=headers, timeout=35)
    response.raise_for_status()
    run = response.json()["data"]
if run["status"] != "SUCCEEDED":
    raise SystemExit("Run " + run["id"] + " ended " + run["status"] + "; inspect logs.")
response = requests.get(api + "/datasets/" + run["defaultDatasetId"] + "/items",
    headers=headers, params={"format": "json", "limit": 20}, timeout=35)
response.raise_for_status()
rows = response.json()
Path("result.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
if not rows:
    print("No dataset rows. Inspect the run OUTPUT and logs for source diagnostics.")
else:
    print("Saved", len(rows), "rows (up to 20) to result.json; review availability fields.")
