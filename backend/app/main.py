from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.models import Base
from app.database import engine
from app.api.v0 import trips


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load Pre-app startup stuff.
    Base.metadata.create_all(engine)

    yield  # App runs.

    # Do post-app shutdown stuff.
    pass


app = FastAPI(lifespan=lifespan)

app.include_router(trips.router)
