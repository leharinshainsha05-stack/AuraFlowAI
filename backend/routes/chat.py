from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from services.ai_service import ask_claude

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []
    projects: Optional[List[dict]] = []

@router.post("/chat")
async def chat(request: ChatRequest):
    # Build project context
    project_context = ""
    if request.projects:
        project_context = "\n\nHERE ARE THE USER'S CURRENT PROJECTS:\n"
        for p in request.projects:
            project_context += f"""
--- {p.get('project_name', 'Unknown')} ---
Type: {p.get('project_type', 'Unknown')}
Deadline: {p.get('deadline', 'Unknown')}
Days Remaining: {p.get('days_remaining', 'Unknown')}
Summary: {p.get('summary', '')[:200] if p.get('summary') else 'No summary'}
Gaps: {', '.join(p.get('gaps', [])[:2]) if p.get('gaps') else 'None'}
"""

    system_prompt = f"""You are AuraFlow AI — a smart personal project assistant for GenZ freelancers.
You have full knowledge of the user's current projects and deadlines.
You give concise, actionable advice. You are friendly, direct, and strategic.
You remember the conversation history and refer back to it naturally.
Never give generic advice — always reference the user's actual projects and deadlines.
Keep responses under 150 words unless asked for detail.
{project_context}

Today's date: 2026-03-25
When suggesting what to work on, always prioritize by closest deadline.
If a project has less than 5 days left, treat it as URGENT."""

    # Build message history for context
    messages_for_ai = ""
    for msg in request.history[-6:]:  # last 6 messages for context
        role = "User" if msg.role == "user" else "AuraFlow"
        messages_for_ai += f"{role}: {msg.content}\n"
    
    user_prompt = f"""Previous conversation:
{messages_for_ai}

User's new message: {request.message}

Respond as AuraFlow AI assistant:"""

    result = ask_claude(user_prompt, system_prompt)
    return {"status": "success", "response": result}