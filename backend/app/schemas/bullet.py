from pydantic import BaseModel


class BulletImproveRequest(BaseModel):
    bullet: str