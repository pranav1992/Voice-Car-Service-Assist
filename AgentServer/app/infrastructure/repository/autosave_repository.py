from app.infrastructure.db.models import WorkflowAutosave
from datetime import datetime


class AutoSaveRepository:
    def __init__(self, session):
        self.session = session

    def create_or_update(self, graph):
        autosave = self.session.query(WorkflowAutosave).filter(
            WorkflowAutosave.workflow_id == graph.workflow_id
        ).first()

        if autosave:
            autosave.payload = graph.payload
            autosave.updated_at = datetime.now()
            autosave.name = graph.name
        else:
            autosave = WorkflowAutosave(
                workflow_id=graph.workflow_id,
                name=graph.name, 
                payload=graph.payload,
                description=graph.description
            )

        self.session.add(autosave)
        self.session.commit()
        self.session.refresh(autosave)
        return autosave

    def update_autosave(self, autosave_id, graph):
        autosave = self.session.get(WorkflowAutosave, autosave_id)
        if autosave is None:
            raise Exception("Autosave not found")
        autosave.payload = graph.payload
        autosave.updated_at = datetime.now()
        autosave.name = graph.name
        autosave.description = graph.description
        self.session.commit()
        self.session.refresh(autosave)
        return autosave

    def get_autosave_by_workflow(self, workflow_id):
        return self.session.query(WorkflowAutosave).filter(
            WorkflowAutosave.workflow_id == workflow_id
        ).first()

    def get_autosave_by_name(self, name):
        return self.session.query(WorkflowAutosave).filter(
            WorkflowAutosave.name == name
        ).first()
