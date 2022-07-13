from fastapi import Depends
from fastapi import FastAPI

from .middleware import log_request_body_dependency, set_response_time_to_header
from .middleware import log_request_middleware
from logger.config import configure_structlog_logger


class DefaultFastAPI(FastAPI):
    """Класс приложения FastAPI, логирующий данные запросов."""

    def __init__(self, service_code: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.service_code = service_code
        self.middleware("http")(log_request_middleware)
        self.middleware("http")(set_response_time_to_header)

        configure_structlog_logger(self.service_code)

    def include_router(self, *args, **kwargs) -> None:
        # https://github.com/tiangolo/fastapi/issues/394
        # в middleware еще нельзя получить доступ к содержимому реквеста - только как Dependency
        # поэтому расширяем класс, чтобы он автоматически проставлялся всем роутам
        # само содержимое запроса появится только в ответе
        dependencies = kwargs.get("dependencies")
        if not dependencies:
            dependencies = []

        dependencies.append(Depends(log_request_body_dependency))
        kwargs["dependencies"] = dependencies

        super().include_router(*args, **kwargs)
