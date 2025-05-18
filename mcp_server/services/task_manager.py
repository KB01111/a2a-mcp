"""Task management service for the MCP server."""

import logging
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

from mcp_server.models.task import Task, TaskState, Message
from mcp_server.models.request import SendTaskRequest, SubscribeTaskRequest
from mcp_server.models.response import SendTaskResponse, SubscribeTaskResponse

logger = logging.getLogger(__name__)


class TaskManager:
    """Manages tasks and their lifecycle."""

    def __init__(self, persistence_layer=None):
        """Initialize the task manager."""
        self.tasks: Dict[str, Task] = {}
        self.stream_queues: Dict[str, asyncio.Queue] = {}
        self.persistence_layer = persistence_layer

    async def on_send_task(self, request: SendTaskRequest) -> SendTaskResponse:
        """Handle synchronous task requests."""
        # Basic validation
        if not request.params or not request.params.get("id"):
            return SendTaskResponse(
                id=request.id, error={"code": -32602, "message": "Invalid params"}
            )

        # Create task
        task_id = request.params.get("id")
        task = Task(
            id=task_id,
            session_id=request.params.get("sessionId"),
            state=TaskState.ACTIVE,
            messages=[Message(**request.params.get("message", {}))],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.tasks[task_id] = task

        # Persist if needed
        if self.persistence_layer:
            await self.persistence_layer.save_task(task)

        # Mock processing
        response_message = Message(
            role="agent",
            parts=[{"type": "text", "text": "Task processed successfully"}],
        )
        task.messages.append(response_message)
        task.state = TaskState.COMPLETED

        return SendTaskResponse(
            id=request.id,
            result={
                "taskId": task.id,
                "state": task.state,
                "message": response_message.dict(),
            },
        )

    async def on_subscribe_task(
        self, request: SubscribeTaskRequest
    ) -> SubscribeTaskResponse:
        """Handle streaming task subscription requests."""
        # Basic validation
        if not request.params or not request.params.get("id"):
            return SubscribeTaskResponse(
                id=request.id, error={"code": -32602, "message": "Invalid params"}
            )

        # Create task
        task_id = request.params.get("id")
        task = Task(
            id=task_id,
            session_id=request.params.get("sessionId"),
            state=TaskState.ACTIVE,
            messages=[Message(**request.params.get("message", {}))],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.tasks[task_id] = task

        # Persist if needed
        if self.persistence_layer:
            await self.persistence_layer.save_task(task)

        # Start processing asynchronously
        asyncio.create_task(self._process_task_async(task))

        return SubscribeTaskResponse(
            id=request.id,
            result={
                "taskId": task.id,
                "state": task.state,
                "streamUrl": f"/tasks/{task_id}/stream",
            },
        )

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID."""
        return self.tasks.get(task_id)

    def get_or_create_stream_queue(self, task_id: str) -> asyncio.Queue:
        """Get or create a queue for streaming updates."""
        if task_id not in self.stream_queues:
            self.stream_queues[task_id] = asyncio.Queue()
        return self.stream_queues[task_id]
        
    def create_send_request(self, id: str, params: Dict[str, Any]) -> SendTaskRequest:
        """Create a SendTaskRequest object.
        
        Args:
            id: Request identifier
            params: Task parameters
            
        Returns:
            SendTaskRequest object
        """
        return SendTaskRequest(id=id, params=params)
        
    def create_subscribe_request(self, id: str, params: Dict[str, Any]) -> SubscribeTaskRequest:
        """Create a SubscribeTaskRequest object.
        
        Args:
            id: Request identifier
            params: Task parameters
            
        Returns:
            SubscribeTaskRequest object
        """
        return SubscribeTaskRequest(id=id, params=params)

    def remove_stream_queue(self, task_id: str) -> None:
        """Remove a stream queue."""
        if task_id in self.stream_queues:
            del self.stream_queues[task_id]

    async def _process_task_async(self, task: Task) -> None:
        """Process a task asynchronously."""
        queue = self.get_or_create_stream_queue(task.id)

        try:
            # Update to processing
            await asyncio.sleep(1)
            task.state = TaskState.PROCESSING
            await queue.put({"state": task.state})

            # Simulate incremental processing
            await asyncio.sleep(1)
            parts = [{"type": "text", "text": "Processing task..."}]
            await queue.put({"partialMessage": {"role": "agent", "parts": parts}})

            # Final result
            await asyncio.sleep(1)
            parts = [{"type": "text", "text": "Task completed successfully"}]
            response_message = Message(role="agent", parts=parts)
            task.messages.append(response_message)
            task.state = TaskState.COMPLETED

            await queue.put({"state": task.state, "message": response_message.dict()})

        except Exception as e:
            logger.error(f"Error processing task {task.id}: {e}")
            task.state = TaskState.FAILED
            task.error = str(e)
            await queue.put({"state": task.state, "error": task.error})
