import time
import uuid
from typing import Any
from typing import Callable

from starlette.requests import Request
from starlette.responses import Response
from structlog.contextvars import bind_contextvars
from structlog.contextvars import clear_contextvars

from . import logger
from .helpers import get_sso_user_params


def get_request_header(request: Request, header_key: str) -> Any:
    if hasattr(request, "headers"):
        return request.headers.get(header_key)

    return None


async def log_request_body_dependency(request: Request) -> None:
    # при аплоаде файла через fastapi.UploadFile содержимое запроса (стрим) уже пуст
    if "multipart/form-data" in request.headers.get("content-type", ""):
        bind_contextvars(request_payload=None)
    else:
        bind_contextvars(request_payload=await request.body() or None)


async def log_request_middleware(request: Request, call_next: Callable) -> Response:
    """Логирует данные запроса и ответа."""
    clear_contextvars()

    start_time = time.monotonic()

    ip = request.client.host
    method = request.method
    path = request.url.path
    request_id = get_request_header(request, "x-request-id") or str(uuid.uuid4())
    url = str(request.url)
    user_agent = get_request_header(request, "user-agent")

    sso_user_params = get_sso_user_params(getattr(request, "user", None))

    bind_contextvars(
        ip=ip,
        method=method,
        path=path,
        url=url,
        request_id=request_id,
        request_payload=None,  # Проставится позже как из Dependency в роуте
        **sso_user_params,
    )
    logger.info(
        "request_started",
        user_agent=user_agent,
    )

    request.request_id = request_id  # type: ignore

    response = await call_next(request)

    code = response.status_code
    response_time = time.monotonic() - start_time
    logger.info(
        "request_finished",
        code=code,
        response_time=response_time,
    )

    return response
