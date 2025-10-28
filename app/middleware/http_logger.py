import time
import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logger import get_logger


class HTTPLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger = get_logger()
        start_time = time.time()

        response: Response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        logger.info(
            "HTTP Request",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(process_time * 1000, 2),
            },
        )
        return response
