from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    DatabaseUnavailableError,
    DomainError,
    SystemConfigurationError,
)


def system_exception_handler(app):
    @app.exception_handler(DatabaseUnavailableError)
    async def database_unavailable_handler(
            request: Request, exc: DatabaseUnavailableError):
        return JSONResponse(
            status_code=503,
            content={"detail": exc.message},
        )

    @app.exception_handler(SystemConfigurationError)
    async def system_configuration_handler(
            request: Request, exc: SystemConfigurationError):
        return JSONResponse(
            status_code=500,
            content={"detail": exc.message},
        )

    # Fallback for any uncaught DomainError to keep responses consistent
    @app.exception_handler(DomainError)
    async def domain_error_handler(
            request: Request, exc: DomainError):
        return JSONResponse(
            status_code=500,
            content={"detail": exc.message},
        )
