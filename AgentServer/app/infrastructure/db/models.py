from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional, Dict, Any
from uuid import uuid4, UUID
from sqlalchemy import Column, JSON
from pydantic import model_validator


class WorkflowAutosave(SQLModel, table=True):  # draft / working state
    __tablename__ = "autosave"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    workflow_id: UUID = Field(foreign_key="workflow.id")
    name: str = Field(max_length=200, unique=True, index=True)
    description: Optional[str] = Field(default=None, max_length=1000)
    payload: Dict[str, Any] = Field(
        sa_column=Column(JSON, nullable=False),
        description="Workflow graph payload from UI"
        "(nodes, edges, metadata).",
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp the snapshot was stored.",
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp the snapshot was stored.",
    )


class WorkFlow(SQLModel, table=True):  # Persistent Memory / history
    __tablename__ = "workflow"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=200, unique=True, index=True)
    name_lower: Optional[str] = Field(
        default=None, max_length=200, unique=True, index=True
    )
    description: Optional[str] = Field(default=None, max_length=1000)
    payload: Dict[str, Any] = Field(
        sa_column=Column(JSON, nullable=False),
        description="Workflow graph payload from UI"
        "(nodes, edges, metadata).",
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp the snapshot was stored.",
    )

    @model_validator(mode="before")
    @classmethod
    def set_name_lower(cls, data):
        if isinstance(data, dict):
            name = data.get("name")
            if name and not data.get("name_lower"):
                data = {**data, "name_lower": name.lower()}
        return data
