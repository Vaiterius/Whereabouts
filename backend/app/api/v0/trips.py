from uuid import UUID


from fastapi import APIRouter, HTTPException

from app.models import Trip
from app.schemas.trip import TripCreate, TripResponse
from app.database import SessionDep

router = APIRouter(prefix="/trips", tags=["trips"])


@router.get("/{trip_id}")
def get_trip(trip_id: UUID, session: SessionDep) -> TripResponse:
    """Return a specific trip

    TODO: Switch IDs to slugs and make slug history table.
    """
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip could not be found")
    return TripResponse.model_validate(trip)


@router.post("/", status_code=201)
def create_trip(
    trip: TripCreate,
    session: SessionDep,
) -> TripResponse:
    """Create a new trip"""
    trip = Trip(**trip.model_dump(), author_id="3fa85f64-5717-4562-b3fc-2c963f66afa6")
    session.add(trip)
    session.commit()
    return TripResponse.model_validate(trip)
