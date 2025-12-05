from typing import List, Dict, Any
from pydantic import BaseModel, ConfigDict

class ClientBadgeBase(BaseModel):
    badges: List[Dict[str, Any]] = []
    reviewed_stores_id: List[int] = []

class ClientBadgeCreate(ClientBadgeBase):
    client_id: int

class ClientBadgeUpdate(BaseModel):
    badges: List[Dict[str, Any]] = None
    reviewed_stores_id: List[int] = None

class ClientBadge(ClientBadgeBase):
    id: int
    client_id: int

    model_config = ConfigDict(from_attributes=True)
