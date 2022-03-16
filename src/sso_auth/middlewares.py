from contextvars import ContextVar
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

ctx_var: ContextVar = ContextVar("request")


class ContextRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        ctx_var.set(request)
        response: Response = await call_next(request)
        return response
