#!/usr/bin/env python3
"""Minimal integration client for the deployed Frio Intel flow.

Any system in a customer's stack talks to the deployment exactly like
this -- a Slack bot, a BI tool, an internal portal: one POST to start a
run, then poll GET /status until the finished brief comes back.

Usage:
    uv run python scripts/ask_frio.py

Needs CREWAI_BEARER (the deployment's bearer token) in .env or the
environment. FRIO_INTEL_API_URL overrides the deployment URL.
"""
import json
import os
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

API_URL = os.environ.get(
    "FRIO_INTEL_API_URL",
    "https://frio-intel-4c0ce13b-d159-4994-869b-79ac3664-25981cec.crewai.com",
)
DEFAULT_QUESTION = "Should Frio Beverage Company enter the functional beverage category?"
REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"
POLL_SECONDS = 5


def api(path: str, payload: dict | None = None) -> dict:
    token = os.environ.get("CREWAI_BEARER")
    if not token:
        sys.exit("Set CREWAI_BEARER in .env (deployment bearer token from the AMP dashboard)")
    req = urllib.request.Request(
        API_URL + path,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def main() -> None:
    print("Frio Market Intelligence -- deployed on CrewAI AMP")
    print(f"  endpoint: {API_URL}")
    question = input(f"\nQuestion [{DEFAULT_QUESTION}]: ").strip() or DEFAULT_QUESTION

    kickoff_id = api("/kickoff", {"inputs": {"question": question}})["kickoff_id"]
    print(f"\n  run started: {kickoff_id}")
    print("  (watch it live in the AMP Traces tab)\n")

    started, state = time.monotonic(), ""
    while True:
        status = api(f"/status/{kickoff_id}")
        if status["state"] != state:
            state = status["state"]
            print(f"  [{time.monotonic() - started:5.1f}s] {state}")
        if state in ("SUCCESS", "FAILED", "ERROR"):
            break
        time.sleep(POLL_SECONDS)

    if state != "SUCCESS":
        sys.exit(f"\nRun ended in {state}: {json.dumps(status, indent=2)[:800]}")

    result = status["result"]
    if isinstance(result, str):
        result = json.loads(result)

    slug = "frio-brief-" + "".join(c if c.isalnum() else "-" for c in question.lower())[:60].strip("-")
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    html_path = REPORTS_DIR / f"{slug}.html"
    (REPORTS_DIR / f"{slug}.md").write_text(result["report_markdown"])
    html_path.write_text(result["report_html"])

    print(f"\n  brief saved: {html_path}")
    webbrowser.open(html_path.as_uri())


if __name__ == "__main__":
    main()
