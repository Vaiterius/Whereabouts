from typing import Optional
from uuid import UUID
from datetime import datetime, date

from pydantic import BaseModel, ConfigDict


class TripBase(BaseModel):
    """Base fields for trip data"""

    title: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_private: Optional[bool] = False


class TripCreate(TripBase):
    """Request for trip creation"""

    pass


class TripUpdate(BaseModel):
    """Request for changing trip upload details"""

    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    cover_photo_id: Optional[UUID] = None
    is_private: Optional[bool] = False


class TripResponse(TripBase):
    """Response after fetching data from existing trip"""

    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    # Allows model_validate() to accept SQLAlchemy objects, not just dicts.
    model_config = ConfigDict(from_attributes=True)
