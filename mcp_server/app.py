"""Main application factory for the MCP server."""

import logging
from aiohttp import web

from mcp_server.config import get_settings
from mcp_server.api.routes import setup_routes
from mcp_server.middleware import setup_middleware
from mcp_server.services.task_manager import TaskManager
from mcp_server.services.agent_registry import AgentCardRegistry

logger = logging.getLogger(__name__)


async def create_app() -> web.Application:
    """Create and configure the aiohttp application."""
    settings = get_settings()
    app = web.Application()

    # Set up middleware
    setup_middleware(app)

    # Initialize services
    task_manager = TaskManager()
    agent_registry = AgentCardRegistry()

    # Store services in app context
    app["task_manager"] = task_manager
    app["agent_registry"] = agent_registry

    # Set up routes
    setup_routes(app)

    logger.info("Application initialized")
    return app
