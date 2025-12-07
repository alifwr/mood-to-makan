from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class StoreBase(BaseModel):
    name: str
    description: Optional[str] = None
    enhanced_description: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    image_url: Optional[str] = None
    suggestion: Optional[str] = None
    suggestion_complete: Optional[bool] = False


class StoreCreate(StoreBase):
    province: Optional[str] = Field(default="string")
    city: Optional[str] = Field(default="string")
    description: Optional[str] = Field(default="string")
    umkm_id: Optional[int] = None


class StoreUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    enhanced_description: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    image_url: Optional[str] = None
    suggestion: Optional[str] = None
    suggestion_complete: Optional[bool] = None

class Store(StoreBase):
    id: int
    umkm_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
