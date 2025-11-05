import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.core.logger import get_logger

logger = get_logger()


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log incoming requests and their durations"""

    EXCLUDED_PATHS = {
        "/health",
        "/",
    }

    async def dispatch(self, request: Request, call_next):

        if request.url.path in self.EXCLUDED_PATHS:
            response = await call_next(request)
            return response

        # Get client IP (handles proxy headers like X-Forwarded-For)
        client_ip = "unknown"
        if request.client:
            client_ip = request.client.host
        
        # Check for proxy headers (Nginx, Cloudflare, etc.)
        if forwarded_for := request.headers.get("x-forwarded-for"):
            client_ip = forwarded_for.split(",")[0].strip()
        
        # Log request start
        start_time = time.time()
        path = request.url.path
        method = request.method

        # logger.info(f"Request started: {method} {path} from {client_ip}")

        # Process request
        response = await call_next(request)

        # Calculate duration
        duration = time.time() - start_time
        duration_ms = round(duration * 1000, 2)

        # Log request completion
        logger.info(
            f"Request completed: {method} {path} from {client_ip} "
            f"- Status: {response.status_code} - Duration: {duration_ms}ms"
        )

        # Add custom header with duration
        response.headers["X-Response-Time"] = f"{duration_ms}ms"

        return response
