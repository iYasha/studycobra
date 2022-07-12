from fastapi.testclient import TestClient
from starlette import status

import crud
from logger.in_requests.application import DefaultFastAPI
from tests.api.v1.common import TestBase


class TestAuthors(TestBase):
    """Тесты для проверки работоспособности АПИ авторов"""

    author_id = 'c0d6fba3-52f0-4655-a4ca-dc5efe031fce'

    def test_create_author(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url('/authors/'),
            json={
                'language': 'fe',
                'name': 'Nikolay Gogol',
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), ('language', 'name', 'created_at', 'updated_at', 'id'))

    def test_get_authors_with_search(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/authors/'),
            headers=self.get_authorization_header(access_token, language='en'),
            params={'q': 'Lev Tolstoy'}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(authors.get('language') for authors in response_data.get('results')) == {'en'}
        assert response_data.get('results')[0].get('name') == 'Lev Tolstoy'

    def test_get_authors(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/authors/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(collection.get('language') for collection in response_data.get('results')) == {'ru'}
        self.assert_keys(response_data.get('results')[0].keys(), ('language', 'name', 'created_at', 'updated_at',
                                                                  'id', 'book_count'))

    def test_get_authors_dropdown(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/authors/dropdown/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data[0].keys(), ('name', 'id'))

    def test_get_one_author(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url(f'/authors/{self.author_id}'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), ('language', 'name', 'created_at', 'updated_at', 'id'))

    def test_update_author(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.put(
            self.get_admin_url(f'/authors/{self.author_id}'),
            json={
                "name": "Nikolay Gogol"
            },
            headers=self.get_authorization_header(access_token),
        )
        get_author = self.get_async_result(crud.AuthorCRUD.get_one(id=self.author_id))
        assert get_author.name == "Nikolay Gogol"
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_author(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.delete(
            self.get_admin_url(f'/authors/{self.author_id}'),
            headers=self.get_authorization_header(access_token),
        )
        get_author = self.get_async_result(crud.AuthorCRUD.get_one(id=self.author_id))
        assert get_author is None
        assert response.status_code == status.HTTP_204_NO_CONTENT
