from pydantic import BaseModel


class InterviewQuestionRequest(BaseModel):
    resume_id: int