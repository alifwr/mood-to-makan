from sqlalchemy import Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import List

class ReviewAnalysis(Base):
    __tablename__ = "review_analysis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    review_id: Mapped[int] = mapped_column(Integer, ForeignKey("reviews.id"), nullable=False)
    detected_problems: Mapped[List[str]] = mapped_column(JSON, default=[], nullable=True)
    
    # Relationships
    review: Mapped["Review"] = relationship("Review")
