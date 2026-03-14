from fastapi import Request
from fastapi.responses import JSONResponse
from app.domain.exceptions import (
    InvalidAgentDataError, AgentAlreadyInitializedError)


def agent_exception_handler(app):
    @app.exception_handler(InvalidAgentDataError)
    async def invalid_agent_data_exception_handler(request: Request, exc:
                                                   InvalidAgentDataError):
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid agent data."},
        )

    @app.exception_handler(AgentAlreadyInitializedError)
    async def agent_already_initialized_exception_handler(
                                            request: Request, exc:
                                            AgentAlreadyInitializedError):
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid agent data."},
        )
