from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, index=True)

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id")
    )

    job_description = Column(Text)

    match_score = Column(Integer)

    analysis = Column(Text)

    resume = relationship(
        "Resume",
        back_populates="job_matches"
    )