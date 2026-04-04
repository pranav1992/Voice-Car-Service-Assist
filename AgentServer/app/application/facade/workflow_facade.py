from sqlmodel import Session
from app.application.services.workflow_service import WorkflowService
from app.application.services.agent_service import AgentService
from app.application.facade.agent_facade import AgentFacade
from app.application.services.position_service import PositionService
from app.infrastructure.repository.position_repository import \
                                                    PositionRepository
from app.infrastructure.repository.workflow_respository import \
                                                    WorkflowRepository
from app.domain.schema import WorkflowCreate, InititialAgent
from app.infrastructure.repository.agent_repository import AgentRepository
from app.infrastructure.repository.tool_repository import ToolRepository
from app.application.services.tool_service import ToolService


class WorkflowFacade:

    def __init__(self, session: Session):
        self.workflow_service = WorkflowService(WorkflowRepository(session))
        self.agent_service = AgentService(AgentRepository(session))
        self.agentfacade = AgentFacade(session)
        self.position_service = PositionService(PositionRepository(session))
        self.tool_service = ToolService(ToolRepository(session))
        self.session = session

    def create_workflow_with_initial_agent(
            self, workflow_data: WorkflowCreate):

        try:
            workflow = self.workflow_service.create(workflow_data)
            agent_data = InititialAgent(
                name="start", workflow_id=workflow.id, isInitial=True
            )
            self.agentfacade.initialize_agent(agent_data=agent_data)
            self.session.commit()
            return workflow

        except Exception:
            self.session.rollback()
            raise

    def get_all_agents(self, workflow_id):
        return self.agent_service.get_all_agents(workflow_id=workflow_id)

    def get_all_nodes(self, workflow_id):
        agents = self.agent_service.get_all_agents(workflow_id=workflow_id)
        tools = self.tool_service.get_all_tools(workflow_id=workflow_id)
        return {"agents": agents, "tools": tools}

    def delete_workflow(self, workflow_id):
        try:
            result = self.workflow_service.delete_workflow(workflow_id)
            self.session.commit()
            return result
        except Exception:
            self.session.rollback()
            raise
