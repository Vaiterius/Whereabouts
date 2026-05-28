from typing import Generator, Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


engine = create_engine(
    "sqlite:///database.db", echo=True, connect_args={"check_same_thread": False}
)


def get_session() -> Generator:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
