from fastapi import Request
from fastapi.responses import JSONResponse
from app.domain.exceptions import DuplicateNameError


def workflow_exception_handler(app):

    @app.exception_handler(DuplicateNameError)
    async def duplicate_name_exception_handler(request: Request, exc:
                                               DuplicateNameError):
        return JSONResponse(
            status_code=400,
            content={
                "content": f"Workflow with the name {exc.name} already exists"
                },
        )

