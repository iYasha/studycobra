import pytest
from _pytest.monkeypatch import MonkeyPatch
from fastapi.testclient import TestClient
from starlette import status

from logger.in_requests.application import DefaultFastAPI
from sdk import healthchecks as hc_utils


class TestHealthChecks:
    """Тесты для проверки работоспособности АПИ"""

    def test_readiness(self, app: DefaultFastAPI, client: TestClient) -> None:
        response = client.get(app.url_path_for("readiness"))
        assert response.status_code == status.HTTP_200_OK
        assert response.text == "Ok"

    def test_check_database(self, app: DefaultFastAPI, client: TestClient) -> None:
        response = client.get(app.url_path_for("check_database"))
        assert response.status_code == status.HTTP_200_OK
        assert response.text == "1"

    def test_sentry_debug(self, app: DefaultFastAPI, client: TestClient) -> None:
        with pytest.raises(Exception):
            client.get(app.url_path_for("sentry_debug"))

    def test_no_liveness(
        self, app: DefaultFastAPI, client: TestClient, monkeypatch: MonkeyPatch
    ) -> None:
        monkeypatch.setattr(hc_utils, "check_memory_usage", lambda: "no_success")
        response = client.get(app.url_path_for("liveness"))
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        monkeypatch.undo()

    def test_liveness(self, app: DefaultFastAPI, client: TestClient) -> None:
        response = client.get(app.url_path_for("liveness"))
        assert response.status_code == status.HTTP_200_OK, response.json()
        assert response.json() == {
            "DatabaseBackend": "working",
            "DefaultFileStorageHealthCheck": "working",
            "DiskUsage": "working",
            "MemoryUsage": "working",
            "RabbitMQHealthCheck": "working",
        }
