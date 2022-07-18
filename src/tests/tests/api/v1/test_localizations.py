from fastapi.testclient import TestClient
from starlette import status

import crud
from logger.in_requests.application import DefaultFastAPI
from tests.api.v1.common import TestBase


class TestLocalization(TestBase):
    """Тесты для проверки работоспособности АПИ локализации"""

    def test_get_localizations(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_token(client)
        response = client.get(
            self.get_url('/localizations/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data[0].keys(), (
            'created_at', 'updated_at', 'language', 'locale', 'index', 'is_active'
        ))