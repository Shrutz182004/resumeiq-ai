from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base

from sqlalchemy import DateTime
from datetime import datetime


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)

    filepath = Column(String, nullable=False)

    extracted_text = Column(Text)

    ats_score = Column(Integer, default=0)

    created_at = Column(
    DateTime,
    default=datetime.utcnow
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="resumes"
    )

    job_matches = relationship(
        "JobMatch",
        back_populates="resume"
    )