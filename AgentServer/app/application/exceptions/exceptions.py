from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request


def exception_handler(app):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc:
                                           RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "detail": "Invalid workflow payload.",
                "errors": exc.errors(),
            },
        )
