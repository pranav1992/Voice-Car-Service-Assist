from .base import DomainError


class DuplicateWorkflowError(DomainError):
    code = "WORKFLOW_DUPLICATE"

    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Workflow with the name {name} already exists")


class DuplicateNameError(DomainError):
    code = "DUPLICATE_NAME"

    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Name {name} already exists")


class WorkflowNotFoundError(DomainError):
    code = "WORKFLOW_NOT_FOUND"

    def __init__(self, workflow_id):
        self.workflow_id = workflow_id
        super().__init__(f"Workflow {workflow_id} not found")
