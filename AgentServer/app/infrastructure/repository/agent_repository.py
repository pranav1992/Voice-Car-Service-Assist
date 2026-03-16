
from app.infrastructure.db.models import Agent


class AgentRepository:
    def __init__(self, session):
        self.session = session

    def initialize(self, agent):
        self.session.add(agent)
        self.session.commit()
        self.session.refresh(agent)
        return agent

    def create(self, agent):
        self.session.add(agent)
        self.session.commit()
        self.session.refresh(agent)
        return agent

    def update(self, agent):
        self.session.merge(agent)
        self.session.commit()
        self.session.refresh(agent)
        return agent

    def get_agent(self, agent_id):
        return self.session.get(Agent, agent_id)

    def isNameAlreadyExist(self, name):
        already_exist = self.session.query(Agent).filter(
            Agent.name == name
        ).first()
        return already_exist is not None

    def get_all_agents(self):
        return self.session.query(Agent).all()

    def delete(self, agent_id):
        agent = self.session.get(Agent, agent_id)
        self.session.delete(agent)
        self.session.commit()
        self.session.refresh(agent)
        return agent

    def isInitialized(self, workflow_id):
        initial_agent = (
            self.session.query(Agent)
            .filter(Agent.workflow_id == workflow_id, Agent.isInital)
            .first()
            )
        return initial_agent is not None
