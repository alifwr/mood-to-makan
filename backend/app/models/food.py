from sqlalchemy import Integer, String, ForeignKey, JSON, DateTime, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from pgvector.sqlalchemy import Vector
from app.core.database import Base
from datetime import datetime
from typing import List, Optional, Any

class Food(Base):
    __tablename__ = "foods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    store_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("stores.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    enhanced_description: Mapped[str | None] = mapped_column(String, nullable=True)
    category: Mapped[str] = mapped_column(String, index=True, nullable=False)  # drinks, desserts, main_meals, snacks
    main_ingredients: Mapped[List[str] | None] = mapped_column(JSON, default=[], nullable=True)  # List of main ingredients
    taste_profile: Mapped[List[str]] = mapped_column(JSON, default=[], nullable=False)  # e.g., ["sweet", "spicy", "sour", "savory", "creamy", "fresh"]
    texture: Mapped[List[str]] = mapped_column(JSON, default=[], nullable=False)  # e.g., ["crispy", "soft", "chewy", "crunchy"]
    mood_tags: Mapped[List[str] | None] = mapped_column(JSON, default=[], nullable=True)  # e.g., ["happy", "sad", "stressed", "energetic", "comfort"]
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    embedding: Mapped[Vector] = mapped_column(Vector(1536), nullable=False) # Embedding for semantic search (1536 dimensions for OpenAI embeddings)
    is_valid_food: Mapped[bool | None] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    store: Mapped["Store"] = relationship("Store", back_populates="foods")
    user: Mapped["User"] = relationship("User", back_populates="foods")
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="food")
    user_interactions: Mapped[List["UserFoodHistory"]] = relationship("UserFoodHistory", back_populates="food")
