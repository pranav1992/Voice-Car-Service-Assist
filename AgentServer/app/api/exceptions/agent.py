from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    AgentAlreadyInitializedError,
    AgentNameAlreadyExist,
    AgentNotFoundError,
    InvalidAgentDataError,
)


def agent_exception_handler(app):
    @app.exception_handler(InvalidAgentDataError)
    async def invalid_agent_data_handler(
            request: Request, exc: InvalidAgentDataError):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.message},
        )

    @app.exception_handler(AgentAlreadyInitializedError)
    async def agent_already_initialized_handler(
        request: Request, exc: AgentAlreadyInitializedError
    ):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.message},
        )

    @app.exception_handler(AgentNameAlreadyExist)
    async def agent_name_exists_handler(
            request: Request, exc: AgentNameAlreadyExist):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.message, "name": getattr(
                                            exc, "name", None)},
        )

    @app.exception_handler(AgentNotFoundError)
    async def agent_not_found_handler(
            request: Request, exc: AgentNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": exc.message, "agent_id": getattr(
                                            exc, "agent_id", None)},
        )
