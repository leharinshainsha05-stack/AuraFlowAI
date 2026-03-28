from fastapi import APIRouter
from models.schemas import PitchDeckRequest
from services.ai_service import ask_claude

router = APIRouter()

@router.post("/pitch-deck")
async def generate_pitch(data: PitchDeckRequest):
    system_prompt = """You are AuraFlow AI's Pitch Deck module — built for GenZ freelancers.
    You create sharp, client-winning pitch decks that are specific, confident, and trend-aware.
    Never be generic. Every slide must reference real details from the soul report and project plan.
    Always respond in pure JSON format with no markdown or backticks."""

    user_prompt = f"""
    Create a freelancer pitch deck for {data.project_name} by {data.team_name}.

    Use these as your source of truth:
    Soul Report: {data.soul_report}
    Project Plan: {data.project_plan}

    Generate exactly 7 slides tailored for a FREELANCER pitching to a CLIENT.
    Be specific, punchy, and confident. No corporate fluff. No SDGs.
    Reference real trends, real competitor weaknesses, and real deliverables from the data above.

    Respond ONLY in this JSON format:
    {{
        "slides": [
            {{
                "slide_number": 1,
                "title": "What I'll Build For You",
                "content": "Specific description of exactly what will be delivered — reference the project name and real features",
                "key_point": "One bold, confident statement about the outcome"
            }},
            {{
                "slide_number": 2,
                "title": "Why This Matters Right Now",
                "content": "Market proof — use REAL trends from the soul report to show why this project is timely and necessary",
                "key_point": "The single most compelling market stat or trend"
            }},
            {{
                "slide_number": 3,
                "title": "Where Competitors Are Failing",
                "content": "Use the competitor demerits from soul report — show the gaps in the market that this project fills",
                "key_point": "The biggest weakness in the market right now"
            }},
            {{
                "slide_number": 4,
                "title": "My Approach & Methodology",
                "content": "How the project will be executed — reference the actual phases and methodology from the project plan",
                "key_point": "What makes this approach better than alternatives"
            }},
            {{
                "slide_number": 5,
                "title": "Timeline & Milestones",
                "content": "Specific timeline with key milestones pulled from the project plan — be concrete with dates and deliverables",
                "key_point": "The final delivery date and main deliverable"
            }},
            {{
                "slide_number": 6,
                "title": "What You Get",
                "content": "List all concrete deliverables the client receives — be specific about files, features, and quality",
                "key_point": "The most impressive deliverable"
            }},
            {{
                "slide_number": 7,
                "title": "Let's Work Together",
                "content": "Strong call to action — confident, direct, GenZ energy. Reference the project name and team name",
                "key_point": "One closing line that seals the deal"
            }}
        ]
    }}
    """

    result = ask_claude(user_prompt, system_prompt)
    return {"status": "success", "pitch_deck": result}