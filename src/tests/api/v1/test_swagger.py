from starlette.testclient import TestClient

from core.config import settings


def test_swagger_ok(client: TestClient) -> None:
    docs_response = client.get(settings.docs_url)
    assert docs_response.status_code == 200

    openapi_response = client.get(settings.openapi_url)
    assert openapi_response.status_code == 200
