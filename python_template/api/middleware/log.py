from uuid import uuid4

from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class LogMiddleware(BaseHTTPMiddleware):
    """Middleware to fully trace and log requests and responses."""

    @classmethod
    def get_logger(cls, request: Request):
        """Get the bound logger from the request if any."""
        return request.state.logger if hasattr(request.state, "logger") else logger

    async def dispatch(self, request: Request, call_next):
        # get or generate request ID
        request_id = request.headers.get("x-request-id", str(uuid4()))
        bound_logger = logger.bind(request_id=request_id)

        # set in request.state for access in endpoints
        request.state.request_id = request_id
        request.state.logger = bound_logger

        # log request details
        bound_logger.trace(f"{request.method} {request.url}")
        sanitized_headers = {
            key: (
                "****"
                if key.lower() in ["authorization", "proxy-authorization"]
                else value
            )
            for key, value in request.headers.items()
        }
        bound_logger.trace(f"Headers: {sanitized_headers}")

        response = await call_next(request)

        response.headers["X-Request-ID"] = request_id
        bound_logger.trace(f"Completed request with status {response.status_code}")
        return response
