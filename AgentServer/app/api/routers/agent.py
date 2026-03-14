from fastapi import APIRouter
from app.application.services import agent_service
from app.domain.schema import AgentCreate


router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)


@router.post("/create_agent")
def create_agent(agent: AgentCreate):
    return agent_service.create(agent)


@router.post("/initialize_agent")
def initialize_agent(agent: AgentCreate):
    return agent_service.initialize(agent)


@router.put("/update_agent")
def update_agent(agent: AgentCreate):
    return agent_service.update(agent)


@router.delete("/delete_agent")
def delete_agent(agent: AgentCreate):
    return agent_service.delete(agent)
