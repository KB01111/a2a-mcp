"""Agent registry service for managing Agent Cards."""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class AgentCardRegistry:
    """Registry for managing Agent Cards for multiple agents."""

    def __init__(self):
        """Initialize the agent card registry."""
        self.cards = {}

    def register_agent(self, agent_id: str, card: Dict[str, Any]) -> None:
        """Register an agent's card in the registry.

        Args:
            agent_id: Unique identifier for the agent
            card: Agent card data structure
        """
        self.cards[agent_id] = card
        logger.info(f"Agent registered: {agent_id}")

    def get_agent_card(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve an agent's card from the registry.

        Args:
            agent_id: Unique identifier for the agent

        Returns:
            The agent card if found, None otherwise
        """
        return self.cards.get(agent_id)

    def list_agents(self) -> List[str]:
        """List all registered agents.

        Returns:
            List of agent IDs
        """
        return list(self.cards.keys())

    def remove_agent(self, agent_id: str) -> bool:
        """Remove an agent from the registry.

        Args:
            agent_id: Unique identifier for the agent

        Returns:
            True if agent was removed, False if not found
        """
        if agent_id in self.cards:
            del self.cards[agent_id]
            logger.info(f"Agent removed: {agent_id}")
            return True
        return False
