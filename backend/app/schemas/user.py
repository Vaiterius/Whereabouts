from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    """Base fields for user data"""

    email: EmailStr
    first_name: str
    last_name: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None


class UserCreate(UserBase):
    """Request for user account creation"""

    pass  # Replace with password hash when auth is set up.


class UserUpdate(BaseModel):
    """Request for user changing account details"""

    # End user won't necessarily be updating everything.
    # Email changes will be handled via the admin for now.
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None


class UserResponse(UserBase):
    """Response after fetching data from existing user"""

    id: UUID
    created_at: datetime
    last_seen: Optional[datetime] = None

    # Allows model_validate() to accept SQLAlchemy objects, not just dicts.
    model_config = ConfigDict(from_attributes=True)
