class DomainError(Exception):
    """Base class for all domain-level errors with an optional error code."""

    code: str = "DOMAIN_ERROR"

    def __init__(self, message: str = "Something went wrong"):
        self.message = message
        super().__init__(message)
