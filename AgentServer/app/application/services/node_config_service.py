from app.infrastructure.repository.node_config_repository import\
                                                    NodeConfigRepository
from app.domain.schema import NodeConfigCreate
from app.infrastructure.db.models import NodeConfig


class NodeConfigService:
    def __init__(self, node_config_repo: NodeConfigRepository):
        self.node_config_repo = node_config_repo

    def create(self, node_config: NodeConfigCreate):
        data = NodeConfig(**node_config.model_dump())
        return self.node_config_repo.create(data)

    def update(self, node_config):
        pass

    def get(self, node_config_id):
        pass

    def delete(self, node_config_id):
        pass
