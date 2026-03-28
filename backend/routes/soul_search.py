from fastapi import APIRouter
from models.schemas import SoulSearchRequest
from services.ai_service import ask_claude
from services.research_service import research_project, fetch_url_content

router = APIRouter()

DEPTH_LABELS = {
    "quick": "10-minute quick scan",
    "medium": "45-minute medium research",
    "deep": "2-hour deep dive intensive research"
}

@router.post("/soul-search")
async def soul_search(data: SoulSearchRequest):
    depth_label = DEPTH_LABELS.get(data.depth, "45-minute medium research")

    # Step 1 — Real web research via Tavily
    print(f"🔍 Starting {depth_label} for {data.project_name}...")
    web_research = research_project(
        project_name=data.project_name,
        project_type=data.project_type,
        depth=data.depth
    )
    web_research = web_research[:8000]

    # Step 1b — Deep Fetch if URL provided
    url_content = ""
    if data.specific_url:
        print(f"🔗 Deep Fetching: {data.specific_url}")
        fetched = fetch_url_content(data.specific_url)
        url_content = f"\n\n--- SPECIFIC URL/PAPER CONTENT (user provided) ---\n{fetched[:4000]}"

    # Step 2 — AI compresses into Soul Report
    system_prompt = """You are AuraFlow AI — a Universal Strategic Engine for GenZ freelancers.
    You have just completed real web research on a project.
    Your job is to compress this research into a powerful Soul Report.
    Always respond in pure JSON format with no markdown or backticks."""

    user_prompt = f"""
    Based on this REAL web research data:
    {web_research}
    {url_content}

    Project Name: {data.project_name}
    Project Type: {data.project_type}
    Description: {data.description}
    Research Depth: {depth_label}

    Generate a comprehensive Soul Report with these exact sections:
    1. market_trends: Top 5 REAL trends found from the web research
    2. competitor_demerits: Top 5 REAL competitor weaknesses found
    3. cultural_vibe: The emotional tone and audience mindset based on research
    4. technical_requirements: Key technical considerations found
    5. soul_summary: One powerful paragraph — the Core Soul and unique positioning
    6. key_sources: Top 3 sources used in research (title + url)

    Respond ONLY in this JSON format:
    {{
        "market_trends": [...],
        "competitor_demerits": [...],
        "cultural_vibe": "...",
        "technical_requirements": [...],
        "soul_summary": "...",
        "key_sources": [
            {{"title": "...", "url": "..."}}
        ]
    }}
    """

    result = ask_claude(user_prompt, system_prompt)
    return {"status": "success", "soul_report": result}