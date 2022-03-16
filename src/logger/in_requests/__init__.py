"""Логгер входящих запросов к сервисам внутри системы."""

import structlog

logger = structlog.getLogger(__name__)
