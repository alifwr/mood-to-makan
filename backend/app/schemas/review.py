from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class ReviewBase(BaseModel):
    rating: float = Field(..., ge=0.0, le=5.0, description="Rating from 0 to 5")
    comment: Optional[str] = None
    store_id: Optional[int] = None
    food_id: Optional[int] = None

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
