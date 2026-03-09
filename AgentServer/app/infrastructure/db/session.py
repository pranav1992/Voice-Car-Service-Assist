import os
from contextlib import contextmanager

from sqlmodel import SQLModel, Session, create_engine

from .models import Autosave, WorkFlow  # noqa: F401 - ensure models are registered


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/agentdb",
)

# echo can be toggled via env to help debugging SQL
engine = create_engine(DATABASE_URL, echo=os.getenv("SQL_ECHO", "false").lower() == "true")


def init_db() -> None:
    """Create tables if they do not exist."""
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Session:
    """Provide a transactional scope around a series of operations."""
    with Session(engine) as session:
        yield session
