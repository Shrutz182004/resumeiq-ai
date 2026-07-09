from pydantic import BaseModel


class ResumeChatRequest(BaseModel):
    resume_id: int
    question: str