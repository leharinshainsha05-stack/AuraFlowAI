from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional
from pydantic import BaseModel
import fitz  # pymupdf
from docx import Document
import io
from datetime import date, datetime
from services.ai_service import ask_claude
from services.research_service import research_project

router = APIRouter()

# ── Single project models ──────────────────────────────────────────
def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    text = ""
    try:
        if filename.endswith(".pdf"):
            pdf = fitz.open(stream=file_bytes, filetype="pdf")
            for page in pdf:
                text += page.get_text()
        elif filename.endswith(".docx"):
            doc = Document(io.BytesIO(file_bytes))
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif filename.endswith(".txt"):
            text = file_bytes.decode("utf-8")
        else:
            text = file_bytes.decode("utf-8", errors="ignore")
    except Exception as e:
        text = f"Could not extract text: {str(e)}"
    return text


@router.post("/file-manager/upload")
async def upload_files(
    project_name: str = Form(...),
    deadline: str = Form(...),
    files: List[UploadFile] = File(...)
):
    # Calculate exact days remaining
    today = date.today()
    deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
    days_remaining = (deadline_date - today).days

    if days_remaining <= 0:
        days_remaining = 1

    # Extract text from all files
    all_text = ""
    file_names = []
    for file in files:
        content = await file.read()
        text = extract_text_from_file(content, file.filename)
        all_text += f"\n\n--- File: {file.filename} ---\n{text}"
        file_names.append(file.filename)

    all_text = all_text[:6000]

    # Real web research
    print(f"🔍 Researching market trends for {project_name}...")
    try:
        web_research = research_project(
            project_name=project_name,
            project_type="brand identity design freelance project",
            depth="quick"
        )
        web_research = web_research[:3000]
    except Exception as e:
        web_research = "No web research available."
        print(f"Research error: {e}")

    system_prompt = """You are AuraFlow AI — an advanced strategic engine for GenZ freelancers.
    You deeply analyze project files, understand the project type, cross-reference real market trends,
    and generate intelligent, deadline-aware project plans.
    You never copy-paste from documents — you synthesize, expand, and connect ideas strategically.
    Always respond in pure JSON format with no markdown or backticks."""

    user_prompt = f"""
    You are analyzing a real freelance project. Here are the details:

    Project Name: {project_name}
    Deadline: {deadline} ({days_remaining} days remaining from today)
    Files uploaded: {', '.join(file_names)}

    FILE CONTENTS (extract intelligence from this):
    {all_text}

    REAL MARKET RESEARCH (use this to add current trends):
    {web_research}

    Your job is to:
    1. READ the file contents deeply and understand the project type
    2. DETECT what kind of project this is (Brand Identity, UI/UX, Development, etc.)
    3. EXTRACT deadlines ONLY from the document — if none found, say No internal deadlines found
    4. EXPAND the Ideas section — don't copy paste, connect ideas strategically
    5. GENERATE a sequential plan for EXACTLY {days_remaining} days
    6. PRIORITIZE tasks in logical build order based on the project type
    7. FLAG any gaps or missing elements in the brief

    For a Brand Identity project the logical order is:
    Research → Moodboard → Logo → Color System → Typography → Pattern Language → Menu UX → Digital Touchpoints → App Interface → Packaging → Final Delivery

    For a UI/UX project:
    Research → User Flows → Wireframes → Visual Design → Prototyping → Testing → Handoff

    For a Development project:
    Architecture → Backend → Frontend → Integration → Testing → Deployment

    Respond ONLY in this JSON format:
    {{
        "project_name": "{project_name}",
        "project_type": "detected project type",
        "deadline": "{deadline}",
        "days_remaining": {days_remaining},
        "requirements": ["requirement 1", "requirement 2"],
        "ideas": ["expanded idea 1 — why it matters", "idea 2 connected to trend"],
        "layouts": ["layout element with reasoning"],
        "technical_specs": ["technical spec with context"],
        "deadlines": ["deadlines found IN THE DOCUMENT ONLY — if none say No internal deadlines found"],
        "gaps": ["missing element 1", "missing element 2"],
        "market_insights": ["real trend from web research"],
        "sequential_plan": [
            {{
                "day": 1,
                "date": "YYYY-MM-DD",
                "task": "specific task name",
                "details": "what exactly to do",
                "priority": "high/medium/low",
                "deliverable": "what gets completed"
            }}
        ],
        "summary": "intelligent strategic summary"
    }}

    CRITICAL: sequential_plan MUST have exactly {days_remaining} entries.
    CRITICAL: deadlines field must ONLY contain dates found inside uploaded files.
    CRITICAL: ideas must be expanded and connected, not copied.
    """

    result = ask_claude(user_prompt, system_prompt)
    return {"status": "success", "segregated_data": result}


# ── Multi-project models ───────────────────────────────────────────
class ProjectSummary(BaseModel):
    project_name: str
    project_type: Optional[str] = "Unknown"
    deadline: str
    days_remaining: int
    requirements: Optional[List[str]] = []
    ideas: Optional[List[str]] = []
    layouts: Optional[List[str]] = []
    technical_specs: Optional[List[str]] = []
    sequential_plan: Optional[List[dict]] = []
    summary: Optional[str] = ""
    gaps: Optional[List[str]] = []

class MultiProjectRequest(BaseModel):
    projects: List[ProjectSummary]


@router.post("/file-manager/multi-project")
async def manage_multiple_projects(data: MultiProjectRequest):

    projects_summary = ""
    for i, p in enumerate(data.projects):
        projects_summary += f"""
--- Project {i+1} ---
Name: {p.project_name}
Type: {p.project_type}
Deadline: {p.deadline}
Days Remaining: {p.days_remaining}
Requirements: {', '.join(p.requirements[:3]) if p.requirements else 'None'}
Current Plan Days: {len(p.sequential_plan)}
Gaps: {', '.join(p.gaps[:2]) if p.gaps else 'None'}
Summary: {p.summary[:200] if p.summary else 'None'}
"""

    system_prompt = """You are AuraFlow AI — an advanced multi-project manager for GenZ freelancers.
    You analyze multiple simultaneous projects, detect deadline conflicts, and create an optimized
    combined daily plan that helps the freelancer complete ALL projects on time.
    You know a person can only work 8 hours a day.
    Always respond in pure JSON format with no markdown or backticks."""

    user_prompt = f"""
    A freelancer has {len(data.projects)} simultaneous projects. Analyze all and create
    an optimized master plan.

    HERE ARE ALL THE PROJECTS:
    {projects_summary}

    Your job:
    1. DETECT any deadline conflicts
    2. PRIORITIZE projects by deadline urgency and complexity
    3. CREATE a combined day-by-day master plan — assign hours per project per day
    4. ENSURE all projects can be completed by their deadlines
    5. FLAG any projects at risk of missing deadline
    6. GIVE specific recommendations

    Respond ONLY in this JSON format:
    {{
        "total_projects": {len(data.projects)},
        "analysis_summary": "one paragraph overview",
        "priority_order": [
            {{
                "rank": 1,
                "project_name": "name",
                "deadline": "date",
                "days_remaining": 0,
                "reason": "why this is highest priority"
            }}
        ],
        "conflicts": [
            {{
                "type": "conflict type",
                "projects_involved": ["project1", "project2"],
                "description": "what the conflict is",
                "severity": "high/medium/low"
            }}
        ],
        "master_plan": [
            {{
                "day": 1,
                "date": "YYYY-MM-DD",
                "schedule": [
                    {{
                        "project": "project name",
                        "hours": 4,
                        "task": "specific task",
                        "priority": "high/medium/low"
                    }}
                ],
                "total_hours": 8
            }}
        ],
        "at_risk_projects": [
            {{
                "project_name": "name",
                "reason": "why at risk",
                "recommendation": "what to do"
            }}
        ],
        "recommendations": ["tip 1", "tip 2", "tip 3"]
    }}

    CRITICAL: max 8 hours total per day across all projects.
    CRITICAL: prioritize by closest deadline.
    CRITICAL: master_plan covers from today until the furthest deadline.
    """

    result = ask_claude(user_prompt, system_prompt)
    return {"status": "success", "multi_project_plan": result}
