from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class UserFoodHistory(Base):
    __tablename__ = "user_food_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False, index=True)
    interaction_type = Column(String, nullable=False) # Type of interaction: "viewed", "liked", "reviewed"
    rating = Column(Float, nullable=True) # Optional rating (1-5)
    mood_context = Column(String, nullable=True) # Context at time of interaction (e.g., mood description)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="food_history")
    food = relationship("Food", back_populates="user_interactions")
