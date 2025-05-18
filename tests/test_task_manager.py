"""Unit tests for the TaskManager service."""

import asyncio
import pytest

from mcp_server.services.task_manager import TaskManager
from mcp_server.models.request import SendTaskRequest, SubscribeTaskRequest
from mcp_server.models.task import TaskState


@pytest.fixture
def task_manager():
    """Returns a TaskManager instance for testing."""
    return TaskManager()


@pytest.mark.asyncio
async def test_on_send_task(task_manager):
    """Test synchronous task processing."""
    # Create a valid request
    request = SendTaskRequest(
        id="req-1",
        params={
            "id": "task-1",
            "sessionId": "session-1",
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": "Hello"}]
            }
        }
    )
    
    # Process the request
    response = await task_manager.on_send_task(request)
    
    # Verify response
    assert response.id == "req-1"
    assert response.result is not None
    assert response.result["taskId"] == "task-1"
    assert response.result["state"] == TaskState.COMPLETED
    
    # Verify task was stored
    task = task_manager.get_task("task-1")
    assert task is not None
    assert task.id == "task-1"
    assert task.session_id == "session-1"
    assert len(task.messages) == 2  # User message and response