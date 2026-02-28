"""
Semantic Scholar API wrapper for Nova
Works unauthenticated (lower rate limits) or with an API key.
Set SEMANTIC_SCHOLAR_API_KEY env var when key arrives.
"""

import urllib.request
import urllib.parse
import json
import time
import os

BASE_URL = "https://api.semanticscholar.org/graph/v1"
API_KEY = os.environ.get("SEMANTIC_SCHOLAR_API_KEY", None)
RATE_LIMIT_DELAY = 3  # seconds between requests (unauthenticated = ~1 req/sec)

def _get(endpoint, params):
    url = f"{BASE_URL}{endpoint}?{urllib.parse.urlencode(params)}"
    headers = {"User-Agent": "Nova-SciBot/1.0 (open-source scientific discovery)"}
    if API_KEY:
        headers["x-api-key"] = API_KEY
    req = urllib.request.Request(url, headers=headers)
    time.sleep(RATE_LIMIT_DELAY)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def search_papers(query, limit=5, year_range=None):
    """Search for papers by keyword."""
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,year,authors,abstract,citationCount,openAccessPdf,venue"
    }
    if year_range:
        params["year"] = year_range
    return _get("/paper/search", params)

def get_paper(paper_id, fields="title,year,authors,abstract,citationCount,references"):
    """Get details for a specific paper by ID."""
    params = {"fields": fields}
    return _get(f"/paper/{paper_id}", params)

if __name__ == "__main__":
    print("Testing Semantic Scholar API (unauthenticated)...")
    results = search_papers("AlphaFold protein structure prediction open source", limit=3, year_range="2023-2026")
    for p in results.get("data", []):
        print(f"\n{p.get('year')} — {p.get('title')}")
        print(f"  Citations: {p.get('citationCount', 'N/A')}")
        authors = [a['name'] for a in p.get('authors', [])[:2]]
        print(f"  Authors: {', '.join(authors)}")
        pdf = p.get('openAccessPdf')
        if pdf:
            print(f"  PDF: {pdf.get('url')}")
    print("\nDone.")
