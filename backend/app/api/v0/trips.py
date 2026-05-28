from uuid import UUID


from fastapi import APIRouter, HTTPException

from app.models import Trip
from app.schemas.trip import TripResponse
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
