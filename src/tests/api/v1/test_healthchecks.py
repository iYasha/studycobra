from core.config import settings
from fastapi.testclient import TestClient
from starlette import status


def test_readiness(client: TestClient) -> None:
    """Тест хелсчек апи."""

    response = client.get(f"{settings.API_V1_STR}/healthchecks/readiness")
    assert response.status_code == status.HTTP_200_OK
    assert response.text == "Ok"
