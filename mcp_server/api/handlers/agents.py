"""Agent handlers for the MCP server."""

import logging
from aiohttp import web
from typing import Dict, Any

from mcp_server.services.agent_registry import AgentCardRegistry

logger = logging.getLogger(__name__)


class AgentsHandler:
    """Handler for agent-related requests."""

    def __init__(self, agent_registry: AgentCardRegistry):
        """Initialize the agents handler.

        Args:
            agent_registry: The agent registry service
        """
        self.agent_registry = agent_registry

    async def list_agents(self, request: web.Request) -> web.Response:
        """List all registered agents.

        Args:
            request: The HTTP request object

        Returns:
            List of agent IDs
        """
        agents = self.agent_registry.list_agents()
        return web.json_response({"agents": agents})

    async def get_agent(self, request: web.Request) -> web.Response:
        """Get agent card by ID.

        Args:
            request: The HTTP request object

        Returns:
            Agent card data
        """
        agent_id = request.match_info.get("agent_id")
        if not agent_id:
            return web.json_response({"error": "Agent ID required"}, status=400)

        agent_card = self.agent_registry.get_agent_card(agent_id)
        if not agent_card:
            return web.json_response({"error": "Agent not found"}, status=404)

        return web.json_response(agent_card)

    async def register_agent(self, request: web.Request) -> web.Response:
        """Register a new agent with its card.

        Args:
            request: The HTTP request object

        Returns:
            Registration confirmation
        """
        try:
            data = await request.json()
            if not data.get("id") or not data.get("card"):
                return web.json_response(
                    {"error": "Agent ID and card required"}, status=400
                )

            agent_id = data["id"]
            agent_card = data["card"]

            self.agent_registry.register_agent(agent_id, agent_card)
            logger.info(f"Registered agent: {agent_id}")

            return web.json_response({"status": "success", "id": agent_id})
        except Exception as e:
            logger.error(f"Error registering agent: {e}")
            return web.json_response({"error": "Failed to register agent"}, status=500)
