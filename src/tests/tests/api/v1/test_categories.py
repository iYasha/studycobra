from fastapi.testclient import TestClient
from starlette import status

from logger.in_requests.application import DefaultFastAPI
from tests.api.v1.common import TestBase


class TestCategories(TestBase):

    def test_unauthorized_user_cant_see_categories(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        response = client.get(
            self.get_url('/categories')
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_unauthorized_user_cant_see_category(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        response = client.get(
            self.get_url('/categories/675cc7a4-4197-49e5-abf9-1216325fefda')
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_categories(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_token(client)

        response = client.get(
            self.get_url('/categories'),
            headers=self.get_authorization_header(access_token)
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(category.get('language') for category in response_data) == {'ru'}
        assert tuple(response_data[0].keys()) == (
            'created_at', 'updated_at', 'language', 'name', 'file_id', 'index', 'is_active', 'has_meta', 'file',
            'id', 'admin_id', 'meta_link')

    def test_get_categories_with_aa_language(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_token(client)

        response = client.get(
            self.get_url('/categories'),
            headers=self.get_authorization_header(access_token, language='aa')
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_data == []

    def test_get_one_category(
            self,
            app: DefaultFastAPI,
            client: TestClient
    ):
        access_token = self.get_access_token(client)

        response = client.get(
            self.get_url('/categories/675cc7a4-4197-49e5-abf9-1216325fefda'),
            headers=self.get_authorization_header(access_token)
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), (
            'created_at', 'updated_at', 'language', 'name', 'file_id', 'index', 'is_active', 'has_meta', 'file',
            'id', 'admin_id', 'meta_link', 'books', 'collections'))
