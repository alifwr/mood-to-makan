from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.core.database import Base
from datetime import datetime

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=True)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)
    rating = Column(Float, nullable=False) # 0-5
    comment = Column(String, nullable=False)
    embedding = Column(Vector(1536), nullable=False)  # For semantic analysis
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

     # Relationships
    user = relationship("User", back_populates="reviews")
    store = relationship("Store", back_populates="reviews")
    food = relationship("Food", back_populates="reviews")
