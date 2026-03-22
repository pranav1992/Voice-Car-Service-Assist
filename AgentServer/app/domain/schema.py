from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class WorkflowCreate(BaseModel):
    name: str


class WorkflowResponse(BaseModel):

    id: UUID
    name: str
    created_at: datetime
    name_lower: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class InititialAgent(BaseModel):
    name: str
    workflow_id: UUID
    isInitial: bool


class AgentCreate(BaseModel):
    name: str
    workflow_id: UUID


class Agentresponse(BaseModel):
    id: UUID
    name: str
    workflow_id: UUID
    isInitial: Optional[bool]
    model: str
    temperature: float
    instructions: str
    gaurdrails: str


class PositionResponse(BaseModel):
    id: UUID
    name: str
    Workflow_id: UUID
    x: float
    y: float
    model_config = ConfigDict(from_attributes=True)


class AgentWithPositionResponse(BaseModel):
    id: UUID
    name: str
    workflow_id: UUID
    isInitial: Optional[bool] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    # read from ORM attribute `position_node` but serialize as `position`
    position: Optional[PositionResponse] = Field(
        default=None, validation_alias="position_node"
    )
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=None,
        json_encoders={UUID: str},
    )
