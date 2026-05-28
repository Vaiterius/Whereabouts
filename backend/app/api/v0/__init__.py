from fastapi import APIRouter
from app.api.v0 import trips

router = APIRouter(prefix="/api/v0")

router.include_router(trips.router)
