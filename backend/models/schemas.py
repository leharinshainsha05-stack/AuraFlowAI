from pydantic import BaseModel
from typing import Optional

class SoulSearchRequest(BaseModel):
    project_name: str
    project_type: str
    description: str
    depth: str = "medium"
    specific_url: str = ""

class ProjectPlanRequest(BaseModel):
    soul_report: str
    project_name: str
    deadline_days: int

class PitchDeckRequest(BaseModel):
    soul_report: str
    project_plan: str
    project_name: str
    team_name: str

# Force Pydantic v2 to fully resolve all models
SoulSearchRequest.model_rebuild()
ProjectPlanRequest.model_rebuild()
PitchDeckRequest.model_rebuild()