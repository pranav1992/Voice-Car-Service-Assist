from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    DuplicateWorkflowError,
    WorkflowNotFoundError,
)


def workflow_exception_handler(app):

    @app.exception_handler(DuplicateWorkflowError)
    async def duplicate_workflow_handler(
            request: Request, exc: DuplicateWorkflowError):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.message, "name": getattr(
                                            exc, "name", None)},
        )

    @app.exception_handler(WorkflowNotFoundError)
    async def workflow_not_found_handler(
            request: Request, exc: WorkflowNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": exc.message, "workflow_id": getattr(
                                            exc, "workflow_id", None)},
        )
