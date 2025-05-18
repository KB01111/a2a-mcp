"""Request models for the MCP server."""

from typing import Dict, Any, Optional
from pydantic import BaseModel


class JsonRpcRequest(BaseModel):
    """JSON-RPC 2.0 request model."""

    jsonrpc: str = "2.0"
    id: Any
    method: str
    params: Optional[Dict[str, Any]] = None


class SendTaskRequest(BaseModel):
    """Request model for tasks/send method."""

    id: Any
    params: Dict[str, Any]


class SubscribeTaskRequest(BaseModel):
    """Request model for tasks/sendSubscribe method."""

    id: Any
    params: Dict[str, Any]
