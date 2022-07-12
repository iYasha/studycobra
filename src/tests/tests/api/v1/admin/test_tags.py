from fastapi.testclient import TestClient
from starlette import status

import crud
from logger.in_requests.application import DefaultFastAPI
from tests.api.v1.common import TestBase


class TestTags(TestBase):
    """Тесты для проверки работоспособности АПИ тегов"""

    tag_id = '1b10761d-862b-4494-a22a-9a702e27d1e8'

    def test_create_tag(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url('/tags/'),
            json={
                'language': 'fe',
                'title': 'tag title',
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), ('language', 'title', 'created_at', 'updated_at', 'id'))

    def test_get_tags_with_search(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/tags/'),
            headers=self.get_authorization_header(access_token),
            params={'q': 'Игры'}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(collection.get('language') for collection in response_data) == {'ru'}
        assert response_data[0].get('title') == 'Игры'

    def test_get_tags(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/tags/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(collection.get('language') for collection in response_data) == {'ru'}
        self.assert_keys(response_data[0].keys(), ('language', 'title', 'created_at', 'updated_at', 'id'))

    def test_get_one_tag(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url(f'/tags/{self.tag_id}'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), ('language', 'title', 'created_at', 'updated_at', 'id'))

    def test_update_tag(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.put(
            self.get_admin_url(f'/tags/{self.tag_id}'),
            json={
                "title": "Updated title",
            },
            headers=self.get_authorization_header(access_token),
        )
        tag = self.get_async_result(crud.TagCRUD.get_one(id=self.tag_id))
        assert tag.title == "Updated title"
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_tag(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.delete(
            self.get_admin_url(f'/tags/{self.tag_id}'),
            headers=self.get_authorization_header(access_token),
        )
        tag = self.get_async_result(crud.TagCRUD.get_one(id=self.tag_id))
        assert tag is None
        assert response.status_code == status.HTTP_204_NO_CONTENT
