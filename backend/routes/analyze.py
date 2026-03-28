from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from services.ai_service import ask_claude
from datetime import datetime, date
import json

router = APIRouter()

@router.post("/analyze")
async def analyze_file(
    project_name: str = Form(...),
    deadline: str = Form(...),
    file: UploadFile = File(...)
):
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")
    today = date.today().strftime("%Y-%m-%d")
    deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
    days_remaining = (deadline_date - date.today()).days

    prompt = f"""You are AuraFlow AI, a Universal Strategic Engine and expert project analyst.
Deeply analyze this project brief and return ONLY valid JSON with NO extra text, NO markdown, NO code blocks.

Project Name: {project_name}
Deadline: {deadline}
Today: {today}
Days Remaining: {days_remaining}
File Content:
{text[:3000]}

Return this exact JSON with RICH, DETAILED, EXPANDED content in every field:
{{
  "project_name": "{project_name}",
  "project_type": "specific project type",
  "deadline": "{deadline}",
  "days_remaining": {days_remaining},
  "summary": "Write a detailed 3-4 sentence paragraph covering what the project is, its complexity, key focus areas, and success criteria",
  "requirements": ["detailed requirement 1", "detailed requirement 2", "detailed requirement 3", "detailed requirement 4"],
  "ideas": ["deeply expanded creative idea 1 with implementation detail", "expanded idea 2 with how to build it", "expanded idea 3", "expanded idea 4"],
  "layouts": ["specific layout description 1", "layout description 2", "layout description 3"],
  "technical_specs": ["specific tech stack item 1", "tech spec 2", "tech spec 3", "tech spec 4"],
  "deadlines": ["specific milestone with date 1", "milestone 2", "milestone 3"],
  "market_insights": ["deep market insight 1", "insight 2", "insight 3"],
  "gaps": ["specific gap found in brief 1", "gap 2", "gap 3"],
  "sequential_plan": [
    {{"day": 1, "date": "YYYY-MM-DD", "task": "task name", "details": "detailed description", "deliverable": "concrete deliverable", "priority": "high"}}
  ]
}}

CRITICAL: Generate sequential_plan for ALL {days_remaining} days — every single day from day 1 to day {days_remaining} must have an entry. No gaps. Calculate each date starting from {today}."""

    result = ask_claude(prompt)
    start = result.find('{')
    end = result.rfind('}') + 1
    parsed = json.loads(result[start:end])

    return JSONResponse(content={
        "status": "success",
        "segregated_data": json.dumps(parsed)
    })