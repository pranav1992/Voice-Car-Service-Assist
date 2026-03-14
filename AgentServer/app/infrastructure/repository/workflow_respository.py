from app.infrastructure.db.models import WorkFlow
from sqlalchemy.exc import IntegrityError
from app.domain.exceptions import DuplicateNameError


class WorkflowRepository:
    def __init__(self, session):
        self.session = session

    def create(self, workflow: WorkFlow):
        # preempt duplicate names to return a clean error
        try:
            if workflow.name:
                existing_name = (
                    self.session.query(WorkFlow)
                    .filter(WorkFlow.name_lower == workflow.name.lower())
                    .first()
                )
                if existing_name:
                    raise DuplicateNameError(workflow.name)
            if not workflow.name_lower and workflow.name:
                workflow.name_lower = workflow.name.lower()

            self.session.add(workflow)
            self.session.commit()
            self.session.refresh(workflow)
            return workflow
        except IntegrityError:
            self.session.rollback()
            raise

    def get_workflow(self, workflow_id):
        return self.session.get(WorkFlow, workflow_id)

    def get_workflow_by_name(self, workflow_name):
        return self.session.query(WorkFlow).filter(
            WorkFlow.name == workflow_name).first()

    def get_all_workflows(self):
        return self.session.query(WorkFlow).all()

    def delete_workflow(self, workflow_id):
        workflow = self.session.get(WorkFlow, workflow_id)
        if workflow:
            self.session.delete(workflow)
            self.session.commit()
            self.session.refresh(workflow)
            return workflow

    def update_workflow(self, workflow_id, workflow):
        self.session.merge(workflow)
        self.session.commit()
        self.session.refresh(workflow)
        return workflow
