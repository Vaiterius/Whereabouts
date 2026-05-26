from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PhotoBase(BaseModel):
    """Base fields for Photo data"""

    title: str
    url: str
    caption: Optional[str] = None
    location: Optional[str] = None
    lat: Optional[float] = None
    long: Optional[float] = None
    notes: Optional[str] = None
    taken_at: Optional[datetime] = None


class PhotoMetadataResponse(BaseModel):
    """Extra photographic data that is optionally attached to the main Photo model"""

    camera_make: Optional[str] = None
    camera_model: Optional[str] = None
    lens: Optional[str] = None
    aperture: Optional[str] = None
    shutter_speed: Optional[str] = None
    iso: Optional[str] = None
    focal_length: Optional[str] = None
    is_film: bool = False
    film_stock: Optional[str] = None
    film_format: Optional[str] = None
    push_pull: Optional[str] = None
    lab: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PhotoCreate(PhotoBase):
    """Request for photo creation"""

    trip_id: Optional[UUID] = None  # May be uploaded without being in a trip.


class PhotoUpdate(BaseModel):
    """Request for changing photo upload details"""

    title: Optional[str] = None
    caption: Optional[str] = None
    location: Optional[str] = None
    lat: Optional[float] = None
    long: Optional[float] = None
    notes: Optional[float] = None
    taken_at: Optional[datetime] = None


class PhotoResponse(PhotoBase):
    """Response after fetching data from existing photo"""

    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]
    photo_metadata: Optional[PhotoMetadataResponse] = None

    # Allows model_validate() to accept SQLAlchemy objects, not just dicts.
    model_config = ConfigDict(from_attributes=True)
