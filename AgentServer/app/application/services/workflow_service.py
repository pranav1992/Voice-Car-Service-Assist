from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.infrastructure.repository.workflow_respository import\
                                                 WorkflowRepository
from app.domain.schema import WorkflowCreate
from app.infrastructure.db.models import WorkFlow


class WorkflowService:
    def __init__(self, workflow_repository: WorkflowRepository):
        self.workflow_repository = workflow_repository

    def create(self, workflow: WorkflowCreate):
        try:
            workflow_model = WorkFlow(**workflow.model_dump())
            return self.workflow_repository.create(workflow_model)
        except IntegrityError as e:
            message = str(e.orig) if hasattr(e, "orig") else str(e)
            if "name_lower" in message or\
                    "UNIQUE constraint failed" in message:
                detail = "Workflow name already exists."
            else:
                detail = "Invalid workflow data."
            raise HTTPException(status_code=400, detail=detail)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

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
