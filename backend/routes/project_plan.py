from fastapi import APIRouter
from models.schemas import ProjectPlanRequest
from services.ai_service import ask_claude

router = APIRouter()

@router.post("/project-plan")
async def generate_plan(data: ProjectPlanRequest):
    system_prompt = """You are AuraFlow AI's Project Manager module for GenZ freelancers.
    You create precise, actionable project plans based on deep research.
    Always respond in pure JSON format with no markdown or backticks."""

    user_prompt = f"""
    Based on this Soul Report:
    {data.soul_report}

    Generate a project plan for: {data.project_name}
    Deadline: {data.deadline_days} days from today.

    IMPORTANT: Each phase must contain its own daily_breakdown nested inside it.
    Do NOT have a separate top-level daily_breakdown array.

    Respond ONLY in this JSON format:
    {{
        "project_name": "{data.project_name}",
        "total_days": {data.deadline_days},
        "phases": [
            {{
                "phase": "Phase name",
                "day_range": "Day 1 - Day 2",
                "day_start": 1,
                "day_end": 2,
                "tasks": ["task 1", "task 2"],
                "deliverable": "What gets completed",
                "daily_breakdown": [
                    {{
                        "day": 1,
                        "focus": "Main focus title",
                        "tasks": ["specific task 1", "specific task 2"]
                    }},
                    {{
                        "day": 2,
                        "focus": "Main focus title",
                        "tasks": ["specific task 1", "specific task 2"]
                    }}
                ]
            }}
        ]
    }}

    Make sure every day from 1 to {data.deadline_days} is covered inside a phase's daily_breakdown.
    No day should be missing or repeated.
    """

    result = ask_claude(user_prompt, system_prompt)
    return {"status": "success", "project_plan": result}