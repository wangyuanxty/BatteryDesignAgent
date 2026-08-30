"""Generate the four overview panels with gpt-image-2 via the configured endpoint."""
import base64
import json
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

# Load config from ~/.baoyu-skills/.env
env_path = Path.home() / ".baoyu-skills" / ".env"
cfg = {}
for line in env_path.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        cfg[k.strip()] = v.strip().strip('"').strip("'")

API_KEY = cfg.get("OPENAI_API_KEY")
BASE_URL = cfg.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
MODEL = cfg.get("OPENAI_IMAGE_MODEL", "gpt-image-2")

PROMPTS = {
    "a": "paper/figs/prompts/fig_overview_a.md",
    "b": "paper/figs/prompts/fig_overview_b.md",
    "c": "paper/figs/prompts/fig_overview_c.md",
    "d": "paper/figs/prompts/fig_overview_d.md",
}
OUT = Path("paper/figs/")

def gen(panel):
    prompt = Path(PROMPTS[panel]).read_text(encoding="utf-8")
    body = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "size": "1536x864",  # 16:9 at 2k class
        "quality": "high",
        "n": 1,
    }).encode("utf-8")
    req = Request(
        f"{BASE_URL}/images/generations",
        data=body,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
    )
    with urlopen(req, timeout=600) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    item = data["data"][0]
    if "b64_json" in item:
        raw = base64.b64decode(item["b64_json"])
    else:
        raw = urlopen(item["url"], timeout=300).read()
    out = OUT / f"fig_overview_{panel}.png"
    out.write_bytes(raw)
    print(f"{panel}: wrote {out} ({len(raw)/1024:.0f} KB)")
    return out

def main():
    sys.stdout.reconfigure(encoding="utf-8")  # be safe
    for panel in ["a", "b", "c", "d"]:
        gen(panel)  # sequential: provider concurrency guard
        time.sleep(1)
    print("ALL_DONE")

if __name__ == "__main__":
    main()
