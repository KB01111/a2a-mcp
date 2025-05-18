"""Task data models for the MCP server."""

from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel


class TaskState(str, Enum):
    """Task state enum."""

    ACTIVE = "active"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


class Part(BaseModel):
    """Message part model."""

    type: str
    text: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    file_data: Optional[Dict[str, Any]] = None


class Message(BaseModel):
    """Message model within a task."""

    role: str
    parts: List[Dict[str, Any]]


class Task(BaseModel):
    """Task model representing a unit of work."""

    id: str
    session_id: Optional[str] = None
    state: TaskState
    messages: List[Message]
    created_at: datetime
    updated_at: datetime
    error: Optional[str] = None
