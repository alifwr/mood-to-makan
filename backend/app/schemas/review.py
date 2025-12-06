from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ReviewBase(BaseModel):
    rating: float = Field(..., ge=0.0, le=5.0, description="Rating from 0 to 5")
    comment: str = Field(..., min_length=3)
    store_id: Optional[int] = None
    food_id: Optional[int] = None

class ReviewCreate(ReviewBase):
    pass

class Review(BaseModel):
    id: int
    user_id: int
    store_id: Optional[int]
    food_id: Optional[int]
    rating: float
    comment: str
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
