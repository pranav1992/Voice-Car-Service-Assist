from app.infrastructure.repository.position_repository import \
                                                PositionRepository


class PositionService:
    def __init__(self, position_repository: PositionRepository):
        self.position_repository = position_repository

    def create(self, position):
        return self.position_repository.create(position)

    def update(self, position):
        return self.position_repository.update(position)

    def delete(self, position_id):
        return self.position_repository.delete(position_id)
