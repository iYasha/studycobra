import time
import uuid
from typing import Any
from typing import Callable

from starlette.requests import Request
from starlette.responses import Response
from structlog.contextvars import bind_contextvars
from structlog.contextvars import clear_contextvars

import logging

logger = logging.getLogger(__name__)


def get_request_header(request: Request, header_key: str) -> Any:
    if hasattr(request, "headers"):
        return request.headers.get(header_key)

    return None


async def log_request_body_dependency(request: Request) -> None:
    # при аплоаде файла через fastapi.UploadFile содержимое запроса (стрим) уже пуст
    if "multipart/form-data" in request.headers.get("content-type", ""):
        bind_contextvars(request_payload=None)
    else:
        d = await request.body()
        data = bind_contextvars(request_payload=d or None)
        print(data)


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

    bind_contextvars(
        ip=ip,
        method=method,
        path=path,
        url=url,
        request_id=request_id,
        request_payload=None,  # Проставится позже как из Dependency в роуте
    )
    logger.info(
        f"request_started agent: {user_agent} ip: {ip} method: {method} {path} {url} {request_id}"
    )

    request.request_id = request_id  # type: ignore

    response = await call_next(request)

    code = response.status_code
    response_time = time.monotonic() - start_time
    logger.info(
        f"request_finished {code} {response_time} agent: {user_agent} ip: {ip} method: {method} {path} {url} {request_id}"
    )

    return response


async def set_response_time_to_header(request: Request, call_next: Callable) -> Response:
    start_time = time.monotonic()
    response = await call_next(request)
    response.headers["X-Response-Time"] = str(time.monotonic() - start_time)
    return response
