
from sqlalchemy.orm import joinedload

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
        return (
            self.session.query(Agent)
            .options(joinedload(Agent.position_node))
            .filter(Agent.id == agent_id)
            .one_or_none()
        )

    def isNameAlreadyExist(self, name):
        already_exist = self.session.query(Agent).filter(
            Agent.name == name
        ).first()
        return already_exist is not None

    def get_all_agents(self, workflow_id):
        # materialize the queryset so FastAPI encodes a concrete list
        return (
            self.session.query(Agent)
            .options(joinedload(Agent.position_node))
            .filter(Agent.workflow_id == workflow_id)
            .all()
        )

    def delete(self, agent_id):
        agent = self.session.get(Agent, agent_id)
        self.session.delete(agent)
        self.session.commit()
        self.session.refresh(agent)
        return agent

    def isInitialized(self, workflow_id):
        initial_agent = (
            self.session.query(Agent)
            .filter(Agent.workflow_id == workflow_id, Agent.isInitial)
            .first()
            )
        return initial_agent is not None
