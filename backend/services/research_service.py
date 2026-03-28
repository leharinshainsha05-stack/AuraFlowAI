from tavily import TavilyClient
import os
from dotenv import load_dotenv
import httpx
from bs4 import BeautifulSoup

load_dotenv()
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def research_project(project_name: str, project_type: str, depth: str) -> str:
    if depth == "quick":
        max_results = 5
        queries = [
            f"{project_type} market trends 2025",
            f"{project_name} competitors analysis"
        ]
    elif depth == "medium":
        max_results = 8
        queries = [
            f"{project_type} market trends 2025",
            f"{project_name} competitors weaknesses",
            f"{project_type} target audience insights",
            f"{project_type} industry gaps opportunities"
        ]
    else:  # deep
        max_results = 10
        queries = [
            f"{project_type} market trends 2025",
            f"{project_name} competitors deep analysis",
            f"{project_type} target audience demographics",
            f"{project_type} industry gaps and opportunities",
            f"{project_name} pricing analysis",
            f"{project_type} latest news innovations",
            f"{project_type} customer pain points"
        ]

    all_results = []
    for query in queries:
        try:
            response = client.search(
                query=query,
                max_results=max_results,
                search_depth="advanced"
            )
            for result in response.get("results", []):
                all_results.append({
                    "query": query,
                    "title": result.get("title", ""),
                    "content": result.get("content", ""),
                    "url": result.get("url", "")
                })
        except Exception as e:
            print(f"Search error for '{query}': {e}")

    formatted = ""
    for i, r in enumerate(all_results):
        formatted += f"\n--- Result {i+1} ---\n"
        formatted += f"Query: {r['query']}\n"
        formatted += f"Title: {r['title']}\n"
        formatted += f"Content: {r['content']}\n"
        formatted += f"Source: {r['url']}\n"

    return formatted


def fetch_url_content(url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = httpx.get(url, timeout=10, follow_redirects=True, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        return text[:6000]
    except Exception as e:
        return f"Failed to fetch URL: {e}"