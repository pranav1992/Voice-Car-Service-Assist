from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.infrastructure.db.session import get_session
from app.infrastructure.repository.autosave_repository import\
                                                 AutoSaveRepository
from app.domain.schema import AutoSaveCreateOrUpdate, AutoSaveRead

router = APIRouter(
    prefix="/autosave",
    tags=["autosave"],
)


@router.post("/create_or_update", response_model=AutoSaveRead)
async def create_or_update_autosave(autosave: AutoSaveCreateOrUpdate,
                                    session: Session = Depends(get_session)):
    autosave_repository = AutoSaveRepository(session)
    return autosave_repository.create_or_update(autosave)


@router.post("/update")
async def update_autosave(autosave_id: str, autosave: AutoSaveCreateOrUpdate,
                          session: Session = Depends(get_session)):
    autosave_repository = AutoSaveRepository(session)
    return autosave_repository.update_autosave(autosave_id, autosave)


@router.get("/get_by_workflow/{workflow_id}", response_model=AutoSaveRead)
async def get_autosave_by_workflow(workflow_id: str,
                                   session: Session = Depends(get_session)):
    autosave_repository = AutoSaveRepository(session)
    return autosave_repository.get_autosave_by_workflow(workflow_id)
