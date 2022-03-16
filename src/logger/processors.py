from logging import Logger

DEFAULT_SERVICE_CODE = "default"  # код сервиса для поля в логе `source` по-умолчанию


def add_service_code(logger: Logger, method_name: str, event_dict: dict) -> dict:
    """Добавляет код сервиса-источника в лог."""
    event_dict["source"] = getattr(logger, "service_code", None) or DEFAULT_SERVICE_CODE

    return event_dict
