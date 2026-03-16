from fastapi import Request
from fastapi.responses import JSONResponse
from app.domain.exceptions import (
    InvalidAgentDataError, AgentAlreadyInitializedError,AgentNameAlreadyExist)


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
            content={"detail": "initial agent for this workflow already exist! if you need any change please modify it."},
        )
    
    @app.exception_handler(AgentNameAlreadyExist)
    async def agent_name_already_exist(request: Request, exc: AgentNameAlreadyExist):
        return JSONResponse(
            status_code=400,
            content={"detail": f"Agent name {exc.name} already exist!"}
        )
