from .base import DomainError


class InvalidAgentDataError(DomainError):
    code = "INVALID_AGENT_DATA"

    def __init__(self, message: str = "Invalid agent data"):
        super().__init__(message)


class AgentAlreadyInitializedError(DomainError):
    code = "AGENT_ALREADY_INITIALIZED"

    def __init__(
            self,
            message: str = "Agent already initialized for this workflow"):
        super().__init__(message)


class AgentNameAlreadyExist(DomainError):
    code = "AGENT_NAME_EXISTS"

    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Agent name {name} already exists")


class AgentNotFoundError(DomainError):
    code = "AGENT_NOT_FOUND"

    def __init__(self, agent_id):
        self.agent_id = agent_id
        super().__init__(f"Agent {agent_id} not found")
