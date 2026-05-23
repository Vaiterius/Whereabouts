from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    # Note: Mapped[<type>] already directly implies non-nullable
    first_name: Mapped[str]
    last_name: Mapped[str]
    avatar_url: Mapped[Optional[str]]
    bio: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    last_seen: Mapped[Optional[datetime]]


class Photo(Base):
    __tablename__ = "photo"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    author_id: Mapped[UUID] = mapped_column(ForeignKey("user_account.id"))
    trip_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("trips.id")
    )  # Photos can be uploaded without belonging to a trip.
    title: Mapped[str]
    url: Mapped[str]
    caption: Mapped[Optional[str]]
    location: Mapped[Optional[str]]
    lat: Mapped[Optional[float]]
    long: Mapped[Optional[float]]
    notes: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]]
    taken_at: Mapped[Optional[datetime]]


class PhotoMetadata(Base):
    """1 to 1 with the Photo model"""

    __tablename__ = "photo_metadata"

    photo_id: Mapped[UUID] = mapped_column(ForeignKey("photo.id"), primary_key=True)
    camera_make: Mapped[Optional[str]]
    camera_model: Mapped[Optional[str]]
    lens: Mapped[Optional[str]]
    aperture: Mapped[Optional[str]]
    shutter_speed: Mapped[Optional[str]]
    iso: Mapped[Optional[str]]
    focal_length: Mapped[Optional[str]]
    is_film: Mapped[bool] = mapped_column(default=False)
    film_stock: Mapped[Optional[str]]
    film_format: Mapped[Optional[str]]
    push_pull: Mapped[Optional[str]]
    lab: Mapped[Optional[str]]


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    author_id: Mapped[UUID] = mapped_column(ForeignKey("user_account.id"))
    title: Mapped[str]
    description: Mapped[str]
    cover_photo_id: Mapped[Optional[str]] = mapped_column(ForeignKey("photo.id"))
    is_private: Mapped[bool] = mapped_column(default=False)  # Just in case.
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]]
