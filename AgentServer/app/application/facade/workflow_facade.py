from sqlmodel import Session
from app.application.services.workflow_service import WorkflowService
from app.application.services.agent_service import AgentService
from app.application.services.position_service import PositionService
from app.infrastructure.repository.position_repository import \
                                                    PositionRepository
from app.infrastructure.repository.workflow_respository import (
    WorkflowRepository,
)
from app.infrastructure.repository.agent_repository import AgentRepository


class WorkflowFacade:

    def __init__(self, session: Session):
        self.workflow_service = WorkflowService(WorkflowRepository(session))
        self.agent_service = AgentService(AgentRepository(session))
        self.position_service = PositionService(PositionRepository(session))

        self.session = session

    def create_workflow_with_initial_agent(self, workflow_data):

        try:
            workflow = self.workflow_service.create(workflow_data)

            position = self.position_service.create()
            position.workflow_id = workflow.id

            agent = self.agent_service.initialize(workflow.id)
            agent.position_id = position.id

            self.session.commit()

            return workflow

        except Exception:
            self.session.rollback()
            raise

    def get_all_agents(self, workflow_id):
        return self.agent_service.get_all_agents(workflow_id=workflow_id)
