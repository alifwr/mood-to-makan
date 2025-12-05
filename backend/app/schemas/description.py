from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class DescriptionGenerateRequest(BaseModel):
    name: str = Field(..., description="Food name")
    category: str = Field(..., description="Food category")
    main_ingredients: Optional[List[str]] = Field(None, description="Main ingredients")
    taste_profile: Optional[List[str]] = Field(None, description="Taste profile")
    texture: Optional[List[str]] = Field(None, description="Texture characteristics")
    region: Optional[str] = Field(None, description="Region of origin")
    selling_points: Optional[List[str]] = Field(None, description="Key selling points")
    style: str = Field("promotional", description="Description style: promotional, informational, or casual")
    language: str = Field("en", description="Language code")


class DescriptionEnhanceRequest(BaseModel):
    current_description: str = Field(..., description="Current description to enhance")
    food_name: str = Field(..., description="Food name")
    category: str = Field(..., description="Food category")
    enhance_for: str = Field("promotional", description="Enhancement goal: promotional, seo, or detailed")
    additional_info: Optional[Dict[str, str]] = Field(None, description="Additional context")


class FlavorCharacteristics(BaseModel):
    primary_flavors: List[str] = Field(default_factory=list)
    secondary_flavors: List[str] = Field(default_factory=list)
    texture_description: str
    aroma_notes: str


class DescriptionResponse(BaseModel):
    short_description: str = Field(..., description="Short 1-2 sentence description")
    long_description: str = Field(..., description="Detailed paragraph description")
    selling_points: List[str] = Field(default_factory=list, description="Key selling points")
    flavor_characteristics: Optional[FlavorCharacteristics] = Field(None, description="Flavor details")


class EnhancedDescriptionResponse(BaseModel):
    enhanced_description: str = Field(..., description="The enhanced description")


class PromotionalKeywordsResponse(BaseModel):
    category: str
    selling_points: List[str] = Field(default_factory=list)
    flavors: List[str] = Field(default_factory=list)
    textures: List[str] = Field(default_factory=list)
    moods: List[str] = Field(default_factory=list)
    general: List[str] = Field(default_factory=list)
