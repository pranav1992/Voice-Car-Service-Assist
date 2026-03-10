from app.infrastructure.repository.autosave_repository import AutoSaveRepository

class AutoSaveService:
    def __init__(self, autosave_repository: AutoSaveRepository):
        self.autosave_repository = autosave_repository

    
    def create_or_update(self, graph):
        return self.autosave_repository.create_or_update(graph)
    
    def get_autosave_by_workflow(self, workflow_id):
        return self.autosave_repository.get_autosave_by_workflow(workflow_id)
    
    def get_autosave_by_name(self, name):
        return self.autosave_repository.get_autosave_by_name(name)