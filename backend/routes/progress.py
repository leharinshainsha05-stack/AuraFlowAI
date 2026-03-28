from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from services.ai_service import ask_claude

router = APIRouter()

class ProgressRequest(BaseModel):
    project_name: str
    project_type: Optional[str] = ""
    deadline: str
    days_remaining: int
    completed_days: List[int]
    sequential_plan: List[dict]
    gaps: Optional[List[str]] = []
    summary: Optional[str] = ""

@router.post("/progress/check")
async def check_progress(data: ProgressRequest):
    total_days = len(data.sequential_plan)
    completed_count = len(data.completed_days)
    remaining_days = total_days - completed_count
    completion_pct = round((completed_count / total_days) * 100) if total_days > 0 else 0

    completed_tasks = []
    remaining_tasks = []
    for item in data.sequential_plan:
        if item.get("day") in data.completed_days:
            completed_tasks.append(f"Day {item['day']}: {item['task']}")
        else:
            remaining_tasks.append(f"Day {item['day']}: {item['task']}")

    system_prompt = """You are AuraFlow AI — a smart project coach for GenZ freelancers.
    A freelancer has updated their progress on a project. Analyze what they've done,
    what's left, and give honest, actionable updated feedback.
    Always respond in pure JSON format with no markdown or backticks."""

    user_prompt = f"""
    Project: {data.project_name}
    Type: {data.project_type}
    Deadline: {data.deadline}
    Days remaining until deadline: {data.days_remaining}
    Total planned days: {total_days}
    Days completed: {completed_count} ({completion_pct}%)
    Days still to go: {remaining_days}

    COMPLETED TASKS:
    {chr(10).join(completed_tasks) if completed_tasks else "None yet"}

    REMAINING TASKS:
    {chr(10).join(remaining_tasks) if remaining_tasks else "All done!"}

    KNOWN GAPS:
    {chr(10).join(data.gaps) if data.gaps else "None"}

    Analyze their progress and give updated feedback.

    Respond ONLY in this JSON format:
    {{
        "completion_percentage": {completion_pct},
        "status": "on_track / at_risk / behind / ahead",
        "status_message": "one sentence on where they stand",
        "pace_analysis": "are they moving fast enough to finish by deadline?",
        "completed_summary": "what has been accomplished so far",
        "next_priority": "the single most important thing to do next",
        "updated_recommendations": [
            "specific actionable tip 1 based on current progress",
            "specific actionable tip 2",
            "specific actionable tip 3"
        ],
        "risk_flags": [
            "any new risks based on current progress"
        ],
        "motivation": "one short encouraging message for the freelancer"
    }}
    """

    result = ask_claude(user_prompt, system_prompt)
    return {"status": "success", "progress_report": result}
