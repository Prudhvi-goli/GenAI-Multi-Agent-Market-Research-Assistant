import os
import re
from dotenv import load_dotenv
from serpapi import GoogleSearch
from transformers import pipeline
from config import MODEL_NAME, DEVICE

# Load environment variables
load_dotenv()
SERP_API_KEY = os.getenv("SERPAPI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# Set up HuggingFace generator
generator = pipeline(
    "text-generation",
    model=MODEL_NAME,
    device=DEVICE,
    token=HF_TOKEN
)

def clean_query(raw_query: str) -> str:
    """
    Cleans a raw query string by removing unwanted patterns and limiting word count.
    """
    cleaned = re.sub(r"(title|\d+)", "", raw_query, flags=re.IGNORECASE)
    cleaned = re.sub(r"[^a-zA-Z0-9 ]", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    words = cleaned.split()[:8]
    return " ".join(words)

def serpapi_search(query: str, max_results: int = 5) -> list:
    """
    Searches Google using SerpAPI and returns a list of result dictionaries.
    """
    if not SERP_API_KEY:
        raise EnvironmentError("Missing SERPAPI_API_KEY in environment variables.")

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERP_API_KEY,
        "num": max_results
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        links = []
        if "organic_results" in results:
            for result in results["organic_results"][:max_results]:
                title = result.get("title", "No Title")
                link = result.get("link", "#")
                snippet = result.get("snippet", "")
                links.append({"title": title, "url": link, "snippet": snippet})
        return links
    except Exception as e:
        raise RuntimeError(f"Error fetching from SerpAPI: {e}")

def run_research_agent(query: str) -> str:
    """
    Runs the research agent to generate a company research summary based on search results.
    """
    try:
        # Define different search queries
        search_terms = [
            f"{query} AI strategy",
            f"{query} AI competitors",
            f"{query} AI trends"
        ]

        # Fetch and combine snippets
        combined_snippets = []
        all_links = []
        for term in search_terms:
            search_results = serpapi_search(term)
            for result in search_results:
                if result.get("snippet"):
                    combined_snippets.append(result["snippet"][:300])
                all_links.append((result["title"], result["url"]))

        context = "\n\n".join(combined_snippets[:3])

        prompt = f"""
        You are a senior market research analyst. Based on the following information, write a structured, concise research summary (~300 words) about the company's AI strategy and market position.

        Context:
        {context}

        Summary:
        """

        # Generate output
        response = generator(
            prompt,
            max_new_tokens=400,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True,
            truncation=True,
            pad_token_id=generator.tokenizer.eos_token_id
        )

        generated_text = response[0]["generated_text"].strip()
        summary = generated_text[len(prompt):].strip()

        if all_links:
            summary += "\n\n### Sources:\n"
            for title, url in all_links[:5]:
                if title.strip() and url.strip():
                    summary += f"- [{title}]({url})\n"

        return summary

    except Exception as e:
        return f"Error in research agent: {str(e)}"

# Test run
if __name__ == "__main__":
    print("Testing Research Agent with 'Tesla'")
    print(run_research_agent("Tesla"))
