from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import workflows
from app.infrastructure.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure tables exist before serving requests
    init_db()
    yield


app = FastAPI(
    title="Car Service Voice Assistant",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(workflows.router)


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
