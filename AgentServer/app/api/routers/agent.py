from fastapi import APIRouter
from app.application.services.agent_service import AgentService
from app.domain.schema import AgentCreate
from fastapi import Depends
from app.domain.schema import Agentresponse
from app.api.dependencies.services import get_agent_service


router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)


@router.post("/", response_model=Agentresponse)
def create_agent(agent: AgentCreate, agent_service: AgentService = Depends(
                                                        get_agent_service)):
    return agent_service.create(agent)


@router.put("/", response_model=Agentresponse)
def update_agent(agent: AgentCreate, agent_service: AgentService = Depends(
                                                    get_agent_service)):
    return agent_service.update(agent)


@router.delete("/{id}", response_model=Agentresponse)
def delete_agent(id, agent_service: AgentService = Depends(
                                                    get_agent_service)):
    return agent_service.delete(id)


@router.get("/{id}")
def getAgent(id, agent_service: AgentService = Depends(
                                                    get_agent_service)):
    return agent_service.get_agent(id)
