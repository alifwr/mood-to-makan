from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Base schema with common fields
class FoodBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str
    enhanced_description: Optional[str] = None
    category: str = Field(..., description="Category: drinks, desserts, main_meals, snacks")
    price: float = Field(default=0.0, ge=0)
    main_ingredients: List[str] = Field(default_factory=list)
    taste_profile: List[str] = Field(default_factory=list, description="e.g., sweet, spicy, sour, savory, creamy, fresh")
    texture: List[str] = Field(default_factory=list, description="e.g., crispy, soft, chewy, crunchy")
    mood_tags: List[str] = Field(default_factory=list, description="e.g., happy, sad, stressed, energetic, comfort")
    image_url: Optional[str] = None

# Schema for creating a new food
class FoodCreate(FoodBase):
    store_id: Optional[int] = None

# Schema for updating a food
class FoodUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: str
    enhanced_description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    main_ingredients: Optional[List[str]] = None
    taste_profile: Optional[List[str]] = None
    texture: Optional[List[str]] = None
    mood_tags: Optional[List[str]] = None
    store_id: Optional[int] = None
    image_url: Optional[str] = None

# Schema for food response
class FoodResponse(FoodBase):
    id: int
    store_id: Optional[int] = None
    is_valid_food: bool 
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schema for food search/recommendation request
class FoodSearchRequest(BaseModel):
    query: str = Field(..., description="Search query or mood description")
    category: Optional[str] = None
    taste_preferences: Optional[List[str]] = None
    exclude_ingredients: Optional[List[str]] = None
    limit: int = Field(default=10, ge=1, le=50)

# Schema for recommendation response with similarity score
class FoodRecommendationItem(BaseModel):
    food: FoodResponse
    similarity_score: Optional[float] = None
    reason: Optional[str] = None

class FoodRecommendationResponse(BaseModel):
    recommendations: List[FoodRecommendationItem]
    query: str
    total_results: int
