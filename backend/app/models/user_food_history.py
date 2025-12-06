from sqlalchemy import Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base
from datetime import datetime
from typing import Optional

class UserFoodHistory(Base):
    __tablename__ = "user_food_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    food_id: Mapped[int] = mapped_column(Integer, ForeignKey("foods.id"), nullable=False, index=True)
    interaction_type: Mapped[str] = mapped_column(String, nullable=False) # Type of interaction: "viewed", "liked", "reviewed"
    rating: Mapped[float | None] = mapped_column(Float, nullable=True) # Optional rating (1-5)
    mood_context: Mapped[str | None] = mapped_column(String, nullable=True) # Context at time of interaction (e.g., mood description)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="food_history")
    food: Mapped["Food"] = relationship("Food", back_populates="user_interactions")
