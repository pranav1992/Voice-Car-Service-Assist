
from app.infrastructure.repository.workflow_respository import\
                                                 WorkflowRepository
from app.domain.schema import WorkflowCreate
from app.infrastructure.db.models import WorkFlow
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.domain.exceptions import DuplicateNameError


class WorkflowService:
    def __init__(self, workflow_repository: WorkflowRepository):
        self.workflow_repository = workflow_repository

    def create(self, workflow: WorkflowCreate):
        try:
            workflow_model = WorkFlow(**workflow.model_dump())
            return self.workflow_repository.create(workflow_model)
        except DuplicateNameError as e:
            raise HTTPException(400, f"Workflow '{e.name}' already exists")
        except IntegrityError:
            raise HTTPException(400, "Invalid workflow data")

        except Exception:
            raise HTTPException(500, "Internal server error")

    def get_workflow(self, workflow_id):
        return self.workflow_repository.get_workflow(workflow_id)

    def get_workflow_by_name(self, workflow_name):
        return self.workflow_repository.get_workflow_by_name(workflow_name)

    def get_all_workflows(self):
        return self.workflow_repository.get_all_workflows()

    def delete_workflow(self, workflow_id):
        return self.workflow_repository.delete_workflow(workflow_id)

    def update_workflow(self, workflow_id, workflow):
        return self.workflow_repository.update_workflow(workflow_id, workflow)
