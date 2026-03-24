
from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import select

from app.infrastructure.db.models import Agent


class AgentRepository:
    def __init__(self, session):
        self.session = session

    def initialize(self, agent):
        self.session.add(agent)
        self.session.flush()
        return agent

    def create(self, agent):
        self.session.add(agent)
        self.session.commit()
        self.session.flush()
        return agent

    def update(self, agent):
        self.session.merge(agent)
        self.session.commit()
        self.session.refresh(agent)
        return agent

    def get_agent(self, agent_id):
        stmt = (
            select(Agent)
            .where(Agent.id == agent_id)
            .options(joinedload(Agent.position_node))
        )
        return self.session.exec(stmt).first()

    def isNameAlreadyExist(self, name):
        already_exist = self.session.exec(
            select(Agent).where(Agent.name == name)
        ).first()
        return already_exist is not None

    def get_all_agents(self, workflow_id):
        """Return all agents for a workflow with their PositionNode eagerly loaded."""

        stmt = (
            select(Agent)
            .where(Agent.workflow_id == workflow_id)
            .options(selectinload(Agent.position_node))
        )

        # materialize the result so FastAPI serializes a concrete list
        return list(self.session.exec(stmt))

    def delete(self, agent_id):
        agent = self.session.get(Agent, agent_id)
        self.session.delete(agent)
        self.session.commit()
        self.session.refresh(agent)
        return agent

    def isInitialized(self, workflow_id):
        initial_agent = self.session.exec(
            select(Agent).where(
                Agent.workflow_id == workflow_id, Agent.isInitial
            )
        ).first()
        return initial_agent is not None
