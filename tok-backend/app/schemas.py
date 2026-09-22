from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base schema for listing data
class ListingBase(BaseModel):
    item_name: str
    price: float
    raw_transcript: Optional[str] = None
    is_available: bool = True

# Schema for creating a listing
class ListingCreate(ListingBase):
    pass

# Schema for returning listing data in API responses
class ListingResponse(ListingBase):
    id: int
    vendor_id: int
    created_at: datetime

    class Config:
        from_attributes = True