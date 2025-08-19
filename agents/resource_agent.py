# agents/resource_agent.py
from serpapi import GoogleSearch
import concurrent.futures
import re
import os

# Load your SERPAPI key safely
SERP_API_KEY = os.getenv("SERPAPI_API_KEY", "your_serpapi_key_here")

# Clean keywords
def clean_query(raw_query):
    cleaned = re.sub(r"(title|\\d+)", "", raw_query, flags=re.IGNORECASE)
    cleaned = re.sub(r"[^a-zA-Z0-9 ]", "", cleaned)
    cleaned = re.sub(r"\\s+", " ", cleaned).strip()
    words = cleaned.split()[:8]
    return " ".join(words)

# Search using SerpAPI
def serpapi_search(query, max_results=5):
    try:
        params = {
            "engine": "google",
            "q": query,
            "api_key": SERP_API_KEY,
            "num": max_results
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        links = []
        if "organic_results" in results:
            for result in results["organic_results"][:max_results]:
                title = result.get("title", "No Title")
                link = result.get("link", "#")
                links.append({"title": title, "url": link})
        return links
    except Exception as e:
        print(f"Error searching with SerpAPI: {e}")
        return []

# Fetch resources in parallel
def fetch_resources(use_cases):
    resource_dict = {}

    def fetch_for_use_case(use_case):
        title_line = next((line for line in use_case.split("\\n") if line.lower().startswith("title:")), None)
        query = clean_query(title_line) if title_line else "genai ai use case"
        print(f"Searching for: {query}")
        links = serpapi_search(query)
        return query, links

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(fetch_for_use_case, use_cases)
        for query, links in results:
            resource_dict[query] = links

    return resource_dict

# Test run
if __name__ == "__main__":
    dummy_use_cases = [
        "Title: Enhance cybersecurity in Tesla autonomous vehicles",
        "Title: Improve AI-based energy optimization at Tesla Superchargers"
    ]
    results = fetch_resources(dummy_use_cases)
    for q, links in results.items():
        print(f"\n Results for {q}:")
        for link in links:
            print(f"  - {link['title']}: {link['url']}")
