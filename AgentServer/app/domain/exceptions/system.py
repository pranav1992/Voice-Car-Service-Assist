from .base import DomainError


class DatabaseUnavailableError(DomainError):
    code = "DATABASE_UNAVAILABLE"

    def __init__(self, message: str = "Database is unavailable"):
        super().__init__(message)


class SystemConfigurationError(DomainError):
    code = "SYSTEM_CONFIGURATION_ERROR"

    def __init__(self, message: str = "System configuration error"):
        super().__init__(message)
