from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime, Boolean
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.database import Base
from datetime import datetime

class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    enhanced_description = Column(String, nullable=True)
    category = Column(String, index=True, nullable=False)  # drinks, desserts, main_meals, snacks
    main_ingredients = Column(JSON, default=[], nullable=True)  # List of main ingredients
    taste_profile = Column(JSON, default=[], nullable=False)  # e.g., ["sweet", "spicy", "sour", "savory", "creamy", "fresh"]
    texture = Column(JSON, default=[], nullable=False)  # e.g., ["crispy", "soft", "chewy", "crunchy"]
    mood_tags = Column(JSON, default=[], nullable=True)  # e.g., ["happy", "sad", "stressed", "energetic", "comfort"]
    image_url = Column(String, nullable=True)
    embedding = Column(Vector(1536), nullable=False) # Embedding for semantic search (1536 dimensions for OpenAI embeddings)
    is_valid_food = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    store = relationship("Store", back_populates="foods")
    user = relationship("User", back_populates="foods")
    reviews = relationship("Review", back_populates="food")
    user_interactions = relationship("UserFoodHistory", back_populates="food")
