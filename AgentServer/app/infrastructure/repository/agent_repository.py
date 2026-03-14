

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

    def delete(self, agent):
        self.session.delete(agent)
        self.session.commit()
        self.session.refresh(agent)
        return agent
