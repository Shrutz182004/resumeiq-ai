from pydantic import BaseModel


class RewriteResumeRequest(BaseModel):
    resume_id: int