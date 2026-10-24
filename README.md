# Google Custom Search JSON API shutdown: migrate by changing one URL

Google closed the **Custom Search JSON API** to new customers on January 20, 2026, and **shuts it down on January 1, 2027**. There is no self-serve official replacement. Calls to `https://www.googleapis.com/customsearch/v1` will stop working after that date. This includes LangChain's `GoogleSearchAPIWrapper` and other libraries built on it.

[SerpKite](https://serpkite.com/migrate/google-custom-search-api?utm_source=github&utm_medium=repo&utm_campaign=custom-search-api-migration) serves the same endpoint shape at `https://api.serpkite.com/customsearch/v1`. It accepts the same parameters and returns the same `kind`, `searchInformation`, `items[]` and `queries`. Most apps only change the hostname and the key.

## The change

```diff
- https://www.googleapis.com/customsearch/v1?key=GOOGLE_API_KEY&cx=CSE_ID&q=asyncio
+ https://api.serpkite.com/customsearch/v1?key=SERPKITE_API_KEY&cx=CSE_ID&q=asyncio
```

### Python (requests)

```python
import os, requests

res = requests.get(
    "https://api.serpkite.com/customsearch/v1",   # was https://www.googleapis.com/customsearch/v1
    params={
        "key": os.environ["SERPKITE_API_KEY"],     # was your Google API key
        "cx": "any",                               # accepted for compatibility
        "q": "site:docs.python.org asyncio",
        "num": 10,
    },
    timeout=30,
)
for item in res.json().get("items", []):
    print(item["title"], item["link"])
```

Runnable versions: [`python/cse.py`](python/cse.py) and [`node/cse.mjs`](node/cse.mjs). Each has a `--check` flag that diffs the response keys against the shape your code reads.

## What is the same and what differs

| | Google Custom Search JSON API | SerpKite `/customsearch/v1` |
|---|---|---|
| Parameters | `key`, `cx`, `q`, `start`, `num`, `gl`, `hl`, `lr`, `safe`, `dateRestrict`, `siteSearch`, `searchType=image` | same |
| Response | `kind`, `searchInformation`, `items[]`, `queries` | same |
| Results | your Programmable Search Engine's sites | the whole public Google results page; restrict with `siteSearch` or `site:` |
| Free tier | 100 queries/day | 2,500 credits on signup + 1,000 a month |
| Price | $5 per 1,000, 10,000/day cap | $1.00 → $0.60 per 1,000, no daily cap, credits never expire |
| After Jan 1, 2027 | stops working | keeps working |

If your engine was restricted to a list of sites, pass them as `siteSearch=example.com` or put `site:example.com` in `q`. The `cx` value is accepted but not used to pick sites.

## LangChain

`langchain-google-community`'s `GoogleSearchAPIWrapper` calls the Google endpoint. Switch to [`langchain-serpkite`](https://github.com/SerpKite/langchain-serpkite) (`pip install langchain-serpkite`), which returns Google results with the same tool interface. Or point your HTTP client at the URL above.

## Steps

1. Get a free key at [app.serpkite.com](https://app.serpkite.com?utm_source=github&utm_medium=repo&utm_campaign=custom-search-api-migration).
2. Replace the hostname and key in your config. Run `python python/cse.py --check` against your usual queries.
3. Move site restrictions from your engine's settings into `siteSearch` or `site:`.
4. Remove the Google key before January 1, 2027.

Full guide with a parameter map: [serpkite.com/migrate/google-custom-search-api](https://serpkite.com/migrate/google-custom-search-api?utm_source=github&utm_medium=repo&utm_campaign=custom-search-api-migration).

## Pricing and limits

- Free: 2,500 credits when you sign up with GitHub or Google, then 1,000 credits every month. No card.
- Paid: credit packs from $10, $1.00 down to $0.60 per 1,000 requests. Credits never expire, and failed or empty requests are not billed.
- Details: [serpkite.com/pricing](https://serpkite.com/pricing?utm_source=github&utm_medium=repo&utm_campaign=custom-search-api-migration)

## Links

- Docs: [serpkite.com/docs](https://serpkite.com/docs?utm_source=github&utm_medium=repo&utm_campaign=custom-search-api-migration)
- Python SDK: [SerpKite/serpkite-python](https://github.com/SerpKite/serpkite-python) · `pip install serpkite`
- TypeScript SDK: [SerpKite/serpkite-js](https://github.com/SerpKite/serpkite-js) · `npm install serpkite`
- MCP server for Claude, Cursor and ChatGPT: [SerpKite/serpkite-mcp](https://github.com/SerpKite/serpkite-mcp)
- How SerpKite collects data: [serpkite.com/legal/how-we-collect](https://serpkite.com/legal/how-we-collect)

This repository is maintained by [SerpKite](https://serpkite.com?utm_source=github&utm_medium=repo&utm_campaign=custom-search-api-migration). Results come from logged-out Google result pages. Google has no official API for these results, and SerpKite is not affiliated with Google. MIT licensed.
