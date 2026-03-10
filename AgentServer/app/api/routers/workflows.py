from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.infrastructure.db.session import get_session
from app.domain.schema import WorkflowCreate, WorkflowResponse
from app.application.services.workflow_service import WorkflowService
from app.infrastructure.repository.workflow_respository import\
                                                 WorkflowRepository


router = APIRouter(
    prefix="/workflows",
    tags=["workflows"],
)


@router.post("/create_workflow", response_model=WorkflowResponse)
async def create_workflow(workflow: WorkflowCreate, session: Session = Depends(
                                                                get_session)):
    workflow_service = WorkflowService(WorkflowRepository(session))
    return workflow_service.create(workflow)


@router.get("/all_workflows", response_model=list[WorkflowResponse])
async def get_all_workflows(session: Session = Depends(get_session)):
    workflow_service = WorkflowService(WorkflowRepository(session))
    return workflow_service.get_all_workflows()
