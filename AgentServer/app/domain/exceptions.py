class DomainExceptions(Exception):
    """Base class for all domain-level errors"""
    pass


class DuplicateNameError(DomainExceptions):
    """Raised when a workflow with the same name already exists"""
    def __init__(self, name: str):
        self.name = name
        super().__init__(name)


class InvalidAgentDataError(DomainExceptions):
    """Raised when the agent data is invalid"""
    pass


class AgentAlreadyInitializedError(DomainExceptions):
    """Raised when the agent is already initialized"""
    pass
