from pydantic import BaseModel


class JobMatchRequest(BaseModel):
    resume_id: int
    job_description: str