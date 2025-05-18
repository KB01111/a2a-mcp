"""Entry point for the MCP server."""

import asyncio
import logging
from aiohttp import web

from mcp_server.app import create_app
from mcp_server.config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def main() -> None:
    """Initialize and run the MCP server."""
    settings = get_settings()
    app = await create_app()

    logger.info(f"Starting MCP server on {settings.host}:{settings.port}")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, settings.host, settings.port)

    try:
        await site.start()
        logger.info(f"MCP server running at http://{settings.host}:{settings.port}")
        # Run forever
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        logger.info("Shutting down MCP server")
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
