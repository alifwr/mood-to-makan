from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Schema for creating a user food history entry
class UserFoodHistoryCreate(BaseModel):
    food_id: int
    interaction_type: str = Field(
        ...,
        description="Type of interaction: viewed, selected, rated"
    )
    rating: Optional[float] = Field(None, ge=1, le=5)
    mood_context: Optional[str] = None


# Schema for user food history response
class UserFoodHistoryResponse(BaseModel):
    id: int
    user_id: int
    food_id: int
    interaction_type: str
    rating: Optional[float]
    mood_context: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# Schema for user food preferences analysis
class UserFoodPreferences(BaseModel):
    favorite_categories: List[str]
    favorite_tastes: List[str]
    favorite_moods: List[str]
    average_rating: Optional[float]
    total_interactions: int
    most_selected_foods: List[dict]
