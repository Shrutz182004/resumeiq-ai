from pydantic import BaseModel

class JobMatchRequest(BaseModel):
    resume_id: int
    job_description: str


class JobMatchResponse(BaseModel):
    match_score: int
    ats_score: int
    matching_skills: list[str]
    missing_skills: list[str]
    missing_keywords: list[str]
    resume_improvements: list[str]