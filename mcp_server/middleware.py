"""Middleware for the MCP server."""

import logging
import time
from aiohttp import web

logger = logging.getLogger(__name__)


@web.middleware
async def error_middleware(request: web.Request, handler) -> web.Response:
    """Handle exceptions in request handlers.

    Args:
        request: The HTTP request object
        handler: The request handler function

    Returns:
        The handler's response or an error response
    """
    try:
        return await handler(request)
    except web.HTTPException as ex:
        return web.json_response({"error": ex.reason}, status=ex.status)
    except Exception as ex:
        logger.exception(f"Unhandled exception: {ex}")
        return web.json_response({"error": "Internal server error"}, status=500)


@web.middleware
async def logging_middleware(request: web.Request, handler) -> web.Response:
    """Log request information and timing.

    Args:
        request: The HTTP request object
        handler: The request handler function

    Returns:
        The handler's response
    """
    start_time = time.time()
    logger.info(f"Request started: {request.method} {request.path}")

    response = await handler(request)

    duration = time.time() - start_time
    logger.info(
        f"Request completed: {request.method} {request.path} - {response.status} ({duration:.3f}s)"
    )

    return response


def setup_middleware(app: web.Application) -> None:
    """Set up middleware for the application.

    Args:
        app: The web application
    """
    app.middlewares.append(error_middleware)
    app.middlewares.append(logging_middleware)
