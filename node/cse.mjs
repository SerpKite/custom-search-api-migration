// Call SerpKite's drop-in /customsearch/v1 the way you called Google's Custom Search JSON API.
// Usage: SERPKITE_API_KEY=skt_live_... node cse.mjs ["site:docs.python.org asyncio"] [--check]
const ENDPOINT = "https://api.serpkite.com/customsearch/v1"; // was https://www.googleapis.com/customsearch/v1
const args = process.argv.slice(2).filter((a) => a !== "--check");
const q = args[0] ?? "site:docs.python.org asyncio";

const url = new URL(ENDPOINT);
url.search = new URLSearchParams({ key: process.env.SERPKITE_API_KEY ?? "", cx: "any", q, num: "10" }).toString();
const res = await fetch(url);
if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
const data = await res.json();

if (process.argv.includes("--check")) {
  const expected = ["kind", "searchInformation", "items", "queries"];
  console.log("top-level keys:", Object.keys(data).sort());
  console.log("missing:", expected.filter((k) => !(k in data)));
}
for (const item of data.items ?? []) console.log(`${item.title}\n  ${item.link}`);
console.log("totalResults:", data.searchInformation?.totalResults);
