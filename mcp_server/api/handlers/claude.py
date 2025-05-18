"""Claude-specific handler for A2A integration."""

import json
import logging
from aiohttp import web
from typing import Dict, Any

from mcp_server.services.task_manager import TaskManager
from mcp_server.models.task import TaskState, Message

logger = logging.getLogger(__name__)


class ClaudeHandler:
    """Handler for Claude-specific integrations."""
    
    def __init__(self, task_manager: TaskManager):
        """Initialize the Claude handler.
        
        Args:
            task_manager: The task manager service
        """
        self.task_manager = task_manager
    
    async def handle_claude_request(self, request: web.Request) -> web.Response:
        """Handle requests from Claude Desktop.
        
        Args:
            request: The HTTP request object
            
        Returns:
            JSON response with task results
        """
        try:
            data = await request.json()
            
            # Extract Claude-specific parameters
            prompt = data.get("prompt", "")
            claude_id = data.get("claude_id", f"claude-{id(request)}")
            stream = data.get("stream", False)
            
            # Create A2A task format
            task_id = f"claude-task-{id(request)}"
            task_params = {
                "id": task_id,
                "sessionId": claude_id,
                "message": {
                    "role": "user",
                    "parts": [{
                        "type": "text",
                        "text": prompt
                    }]
                }
            }
            
            # Process request based on streaming preference
            if stream:
                # Create streaming task
                subscribe_request = self.task_manager.create_subscribe_request(
                    id=claude_id,
                    params=task_params
                )
                response = await self.task_manager.on_subscribe_task(subscribe_request)
                
                # Return stream URL and task info
                return web.json_response({
                    "task_id": task_id,
                    "stream_url": response.result.get("streamUrl"),
                    "status": "processing"
                })
            else:
                # Create synchronous task
                send_request = self.task_manager.create_send_request(
                    id=claude_id,
                    params=task_params
                )
                response = await self.task_manager.on_send_task(send_request)
                
                # Extract response text
                result = response.result
                message = result.get("message", {})
                parts = message.get("parts", [])
                response_text = ""
                
                for part in parts:
                    if part.get("type") == "text":
                        response_text += part.get("text", "")
                
                # Return Claude-compatible response
                return web.json_response({
                    "task_id": task_id,
                    "response": response_text,
                    "status": result.get("state", TaskState.COMPLETED)
                })
                
        except Exception as e:
            logger.error(f"Error handling Claude request: {e}")
            return web.json_response({
                "error": "Failed to process Claude request",
                "details": str(e)
            }, status=500)