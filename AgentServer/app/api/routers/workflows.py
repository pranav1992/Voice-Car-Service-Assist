from fastapi import APIRouter, Depends
from app.domain.schema import WorkflowCreate, WorkflowResponse, Agentresponse
from app.application.services.workflow_service import WorkflowService
from app.application.facade.workflow_facade import WorkflowFacade
from app.api.dependencies.services import (
                                    get_workflow_service, get_workflow_facade)


router = APIRouter(
    prefix="/workflows",
    tags=["workflows"],
)


@router.post("/", response_model=WorkflowResponse)
def create_workflow(workflow: WorkflowCreate, workflowFacade:
                    WorkflowFacade = Depends(get_workflow_facade)):
    return workflowFacade.create_workflow_with_initial_agent(workflow)


@router.get("/get_all", response_model=list[WorkflowResponse])
def get_all_workflows(workflow_service: WorkflowService = Depends(
                                                get_workflow_service)):
    return workflow_service.get_all_workflows()


@router.get("/get_all_agent/{id}", response_model=list[Agentresponse])
def get_all_agents(id, workflowFacade: WorkflowFacade = Depends(
                                                    get_workflow_facade)):
    return workflowFacade.get_all_agents(id)
