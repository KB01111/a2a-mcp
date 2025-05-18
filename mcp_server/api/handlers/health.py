"""Health check handler for the MCP server."""

from aiohttp import web


async def health_check(request: web.Request) -> web.Response:
    """Handle health check requests.

    Args:
        request: The HTTP request object

    Returns:
        HTTP response with status information
    """
    return web.json_response({"status": "healthy"})
