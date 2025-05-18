"""Route definitions for the MCP server API."""

import logging
from aiohttp import web

from mcp_server.api.handlers.tasks import TasksHandler
from mcp_server.api.handlers.agents import AgentsHandler
from mcp_server.api.handlers.health import health_check

logger = logging.getLogger(__name__)


def setup_routes(app: web.Application) -> None:
    """Set up routes for the application."""
    # Create handlers
    tasks_handler = TasksHandler(app["task_manager"])
    agents_handler = AgentsHandler(app["agent_registry"])

    # Health check
    app.router.add_get("/health", health_check)
    app.router.add_get("/ready", health_check)

    # A2A JSON-RPC endpoint
    app.router.add_post("/", tasks_handler.handle_jsonrpc)

    # Tasks streaming endpoint
    app.router.add_get("/tasks/{task_id}/stream", tasks_handler.stream_task)

    # Agent discovery endpoints
    app.router.add_get("/agents", agents_handler.list_agents)
    app.router.add_get("/agents/{agent_id}", agents_handler.get_agent)
    app.router.add_post("/agents", agents_handler.register_agent)

    logger.info("Routes configured")
