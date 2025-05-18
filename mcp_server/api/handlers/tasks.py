"""Task request handlers for the MCP server."""

import json
import logging
from aiohttp import web
from typing import Dict, Any, Optional

from mcp_server.services.task_manager import TaskManager
from mcp_server.models.task import Task, TaskState
from mcp_server.models.request import (
    JsonRpcRequest,
    SendTaskRequest,
    SubscribeTaskRequest,
)
from mcp_server.models.response import (
    JsonRpcResponse,
    SendTaskResponse,
    SubscribeTaskResponse,
)

logger = logging.getLogger(__name__)


class TasksHandler:
    """Handler for task-related requests."""

    def __init__(self, task_manager: TaskManager):
        """Initialize the tasks handler.

        Args:
            task_manager: The task manager service
        """
        self.task_manager = task_manager

    async def handle_jsonrpc(self, request: web.Request) -> web.Response:
        """Handle JSON-RPC requests.

        Args:
            request: The HTTP request object

        Returns:
            JSON-RPC response
        """
        try:
            data = await request.json()
            jsonrpc_request = JsonRpcRequest(**data)

            # Handle different methods
            if jsonrpc_request.method == "tasks/send":
                send_request = SendTaskRequest(
                    id=jsonrpc_request.id, params=jsonrpc_request.params
                )
                response = await self.task_manager.on_send_task(send_request)
            elif jsonrpc_request.method == "tasks/sendSubscribe":
                subscribe_request = SubscribeTaskRequest(
                    id=jsonrpc_request.id, params=jsonrpc_request.params
                )
                response = await self.task_manager.on_subscribe_task(subscribe_request)
            else:
                response = JsonRpcResponse(
                    id=jsonrpc_request.id,
                    error={
                        "code": -32601,
                        "message": f"Method {jsonrpc_request.method} not found",
                    },
                )

            return web.json_response(response.dict())
        except Exception as e:
            logger.error(f"Error handling JSON-RPC request: {e}")
            return web.json_response(
                {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32603, "message": "Internal error"},
                },
                status=500,
            )

    async def stream_task(self, request: web.Request) -> web.StreamResponse:
        """Stream task updates using Server-Sent Events.

        Args:
            request: The HTTP request object

        Returns:
            Streaming response with task updates
        """
        task_id = request.match_info.get("task_id")
        if not task_id:
            return web.json_response({"error": "Task ID required"}, status=400)

        task = self.task_manager.get_task(task_id)
        if not task:
            return web.json_response({"error": "Task not found"}, status=404)

        # Get or create queue for this task
        sse_queue = self.task_manager.get_or_create_stream_queue(task_id)

        # Set up the SSE response
        response = web.StreamResponse()
        response.headers["Content-Type"] = "text/event-stream"
        response.headers["Cache-Control"] = "no-cache"
        response.headers["Connection"] = "keep-alive"
        await response.prepare(request)

        try:
            # Send initial task state
            task_data = task.dict()
            await response.write(f"data: {json.dumps(task_data)}\n\n".encode("utf-8"))

            # Process events from the queue
            while True:
                event = await sse_queue.get()
                if event is None:  # Termination signal
                    break

                data = json.dumps(event)
                await response.write(f"data: {data}\n\n".encode("utf-8"))

                # If task is in a terminal state, end the stream
                if "state" in event and event["state"] in [
                    TaskState.COMPLETED,
                    TaskState.CANCELED,
                    TaskState.FAILED,
                ]:
                    break

        except ConnectionResetError:
            logger.info(f"Client disconnected from task stream: {task_id}")
        finally:
            # Clean up resources
            self.task_manager.remove_stream_queue(task_id)

        return response
