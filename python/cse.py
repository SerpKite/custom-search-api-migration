"""Call SerpKite's drop-in /customsearch/v1 the way you called Google's Custom Search JSON API.

Usage: SERPKITE_API_KEY=skt_live_... python cse.py ["site:docs.python.org asyncio"] [--check]
"""
import os
import sys

import requests

ENDPOINT = "https://api.serpkite.com/customsearch/v1"  # was https://www.googleapis.com/customsearch/v1
args = [a for a in sys.argv[1:] if a != "--check"]
q = args[0] if args else "site:docs.python.org asyncio"

res = requests.get(
    ENDPOINT,
    params={"key": os.environ["SERPKITE_API_KEY"], "cx": "any", "q": q, "num": 10},
    timeout=30,
)
res.raise_for_status()
data = res.json()

if "--check" in sys.argv:
    expected = {"kind", "searchInformation", "items", "queries"}
    missing = expected - data.keys()
    print("top-level keys:", sorted(data.keys()))
    print("missing:", sorted(missing) or "none")
    item_keys = {"title", "link", "snippet", "displayLink"}
    for item in data.get("items", [])[:1]:
        print("item keys missing:", sorted(item_keys - item.keys()) or "none")

for item in data.get("items", []):
    print(f"{item['title']}\n  {item['link']}")
print("totalResults:", data.get("searchInformation", {}).get("totalResults"))
