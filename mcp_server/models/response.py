"""Response models for the MCP server."""

from typing import Dict, Any, Optional
from pydantic import BaseModel


class JsonRpcResponse(BaseModel):
    """JSON-RPC 2.0 response model."""

    jsonrpc: str = "2.0"
    id: Any
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None


class SendTaskResponse(BaseModel):
    """Response model for tasks/send method."""

    id: Any
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None


class SubscribeTaskResponse(BaseModel):
    """Response model for tasks/sendSubscribe method."""

    id: Any
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
