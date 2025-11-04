import functools
from typing import Callable
from fastapi.responses import JSONResponse
import httpx
from app.core.logger import get_logger

logger = get_logger()


def handle_httpx_errors(func: Callable):
    """Decorator to handle httpx errors in proxy endpoints"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Extract path from kwargs for logging
        path = kwargs.get('path', 'unknown')

        try:
            return await func(*args, **kwargs)

        except httpx.HTTPStatusError as e:
            logger.error("HTTP error fetching /%s: %s", path, str(e))
            return JSONResponse(
                status_code=e.response.status_code,
                content={
                    "error": "Failed to fetch from R2",
                    "detail": str(e),
                    "path": path
                }
            )

        except httpx.RequestError as e:
            logger.error("Request error fetching /%s: %s", path, str(e))
            return JSONResponse(
                status_code=502,
                content={
                    "error": "Failed to connect to R2",
                    "detail": str(e),
                    "path": path
                }
            )

        except Exception as e:
            logger.error("Unexpected error fetching /%s: %s", path, str(e))
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "detail": str(e),
                    "path": path
                }
            )

    return wrapper
