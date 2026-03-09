from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional, Dict, Any
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB


class Autosave(SQLModel, table=True):  # draft / working state
    id: int | None = Field(default=None, primary_key=True)
    name: str
    payload: Dict[str, Any] = Field(
        sa_column=Column(JSONB, nullable=False),
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
    id: int | None = Field(default=None, primary_key=True)
    name: str
    version: Optional[int] = Field(
        default=None,
        description="Monotonic version for committed "
                    "snapshots (null for autosave).",
    )
    tag: Optional[str] = Field(
        default=None,
        max_length=64,
        description="Optional human-readable label "
                    "for a committed snapshot.",
    )
    payload: Dict[str, Any] = Field(
        sa_column=Column(JSONB, nullable=False),
        description="Workflow graph payload from UI"
        "(nodes, edges, metadata).",
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp the snapshot was stored.",
    )
