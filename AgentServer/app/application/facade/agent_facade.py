from sqlmodel import Session
from app.application.services.position_service import PositionService
from app.infrastructure.repository.position_repository import \
                                                    PositionRepository
from app.application.services.agent_service import AgentService
from app.infrastructure.repository.agent_repository import AgentRepository
from app.domain.schema import AgentCreate


class AgentFacade:
    def __init__(self, session: Session):
        self.agent_service = AgentService(AgentRepository(session))
        self.position_service = PositionService(PositionRepository(session))
        self.session = session

    def create_agent(self, agent_data: AgentCreate):
        agent = self.agent_service.create(agent_data)
        position = self.position_service.create()
        agent.position_id = position.id
        self.session.commit()
        return agent

    def get_agent(self, agent_id):
        return self.agent_service.get_agent(agent_id)
