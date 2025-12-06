from sqlalchemy import Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.core.database import Base
from datetime import datetime
from typing import Optional

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    store_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("stores.id"), nullable=True)
    food_id: Mapped[int] = mapped_column(Integer, ForeignKey("foods.id"), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False) # 0-5
    comment: Mapped[str] = mapped_column(String, nullable=False)
    embedding: Mapped[Vector] = mapped_column(Vector(1536), nullable=False)  # For semantic analysis
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

     # Relationships
    user: Mapped["User"] = relationship("User", back_populates="reviews")
    store: Mapped["Store"] = relationship("Store", back_populates="reviews")
    food: Mapped["Food"] = relationship("Food", back_populates="reviews")
