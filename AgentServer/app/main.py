from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import workflows
from app.infrastructure.db.engine import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure tables exist before serving requests
    create_db_and_tables()
    yield


app = FastAPI(
    title="Agent Server",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(workflows.router)


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
