from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WorkflowCreate(BaseModel):
    name: str
    description: Optional[str] = None
    payload: Dict[str, Any]


class WorkflowResponse(BaseModel):

    id: UUID
    name: str
    description: Optional[str] = None
    created_at: datetime
    name_lower: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class AutoSaveCreateOrUpdate(BaseModel):
    workflow_id: UUID
    name: str
    description: Optional[str] = None
    payload: Dict[str, Any]


class AutoSaveRead(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    payload: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
