from datetime import datetime
from enum import Enum as PyEnum
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, Dict, Any
from uuid import uuid4, UUID
from sqlalchemy import Column, Enum as SAEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from pydantic import model_validator


class NodeType(str, PyEnum):
    AGENT = "agent"
    TOOL = "tool"


class WorkFlow(SQLModel, table=True):  # Persistent Memory / history
    __tablename__ = "workflow"
    __table_args__ = (UniqueConstraint("name_lower", name="uq_workflow_name"),)
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=200, index=True)
    name_lower: Optional[str] = Field(
        default=None, max_length=200, index=True
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


class PositionNode(SQLModel, table=True):
    __tablename__ = "positionnode"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=200, index=True)
    Workflow_id: UUID = Field(foreign_key="workflow.id")
    x: float
    y: float


class NodeConfig(SQLModel, table=True):
    __tablename__ = "nodeconfig"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    type: NodeType = Field(
        sa_column=Column(SAEnum(NodeType, name="node_type"), nullable=False)
    )
    Workflow_id: UUID = Field(foreign_key="workflow.id")
    data: Dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column("metadata", JSONB, nullable=False),
        description="Tool config / schema",
        alias="metadata",
    )


class Agent(SQLModel, table=True):
    __tablename__ = "agent"
    __table_args__ = (
        UniqueConstraint("workflow_id", "name", name="uq_agent_workflow_name"),
    )
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=200, index=True)
    workflow_id: UUID = Field(foreign_key="workflow.id")
    position: UUID = Field(foreign_key="positionnode.id")
    config: UUID = Field(foreign_key="nodeconfig.id")
    isInitial: Optional[bool] = Field(default=False)
    position_node: Optional[PositionNode] = Relationship(
        sa_relationship_kwargs={"lazy": "joined"}
    )
    node_config: Optional[NodeConfig] = Relationship(
        sa_relationship_kwargs={"lazy": "joined"}
    )


class Tool(SQLModel, table=True):
    __tablename__ = "tool"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=200, index=True)
    Workflow_id: UUID = Field(foreign_key="workflow.id")
    position: UUID = Field(foreign_key="positionnode.id")
    method: str = Field(max_length=10)
    config: UUID = Field(foreign_key="nodeconfig.id")
    position_node: Optional[PositionNode] = Relationship(
        sa_relationship_kwargs={"lazy": "joined"},
    )
    node_config: Optional[NodeConfig] = Relationship(
        sa_relationship_kwargs={"lazy": "joined"}
    )


class HandOff(SQLModel, table=True):
    __tablename__ = "handoff"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=200, index=True)
    Workflow_id: UUID = Field(foreign_key="workflow.id")
    meta: Dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column("metadata", JSONB, nullable=False),
        description="Workflow graph payload from UI (nodes, edges, metadata).",
    )
