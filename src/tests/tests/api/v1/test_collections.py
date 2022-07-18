from fastapi.testclient import TestClient
from starlette import status

from logger.in_requests.application import DefaultFastAPI
from tests.api.v1.common import TestBase


class TestCollections(TestBase):
    collection_id = '6c98229d-34bf-4416-be99-f7ea37dc4754'

    def test_unauthorized_user_cant_get_collection(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        response = client.get(
            self.get_url(f'/collections/{self.collection_id}')
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_collection(
            self,
            app: DefaultFastAPI,
            client: TestClient
    ) -> None:
        access_token = self.get_access_token(client)
        response = client.get(
            self.get_url(f'/collections/{self.collection_id}'),
            headers=self.get_authorization_header(access_token)
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), (
        'created_at', 'updated_at', 'title', 'cover_type', 'text_color', 'language', 'background_color', 'is_active',
        'file_id', 'file', 'id', 'books', 'is_favorite'))
        assert len(response_data['books']) == 3

    def test_collections_favorite(
            self,
            app: DefaultFastAPI,
            client: TestClient
    ):
        access_token = self.get_access_token(client)

        def add_favorite():
            response = client.post(
                self.get_url(f'/collections/favorite/{self.collection_id}'),
                headers=self.get_authorization_header(access_token)
            )
            assert response.status_code == status.HTTP_204_NO_CONTENT

        def get_favorite():
            response = client.get(
                self.get_url(f'/collections/favorite/'),
                headers=self.get_authorization_header(access_token)
            )
            assert response.status_code == status.HTTP_200_OK
            return response.json()

        def remove_favorite():
            response = client.delete(
                self.get_url(f'/collections/favorite/{self.collection_id}'),
                headers=self.get_authorization_header(access_token)
            )
            assert response.status_code == status.HTTP_204_NO_CONTENT

        add_favorite()
        favorites = get_favorite()
        self.assert_keys(favorites['data'][0].keys(), (
        'created_at', 'updated_at', 'title', 'cover_type', 'text_color', 'language', 'background_color', 'is_active',
        'file_id', 'file', 'id', 'books', 'is_favorite'))
        assert len(favorites['data'][0]['books']) != 0
        remove_favorite()
        assert get_favorite()['data'] == []

    def test_collections_recommendations_by_book_id(
            self,
            app: DefaultFastAPI,
            client: TestClient
    ):
        book_id = 'ace3b113-0980-4ae0-8e24-6d63bd0afa38'

        access_token = self.get_access_token(client)
        response = client.get(
            self.get_url(f'/collections/recommendations/'),
            headers=self.get_authorization_header(access_token),
            params={
                'book_id': book_id,
                'limit': 4,
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert all([x['id'] != book_id for x in response.json()])

    def test_collections_recommendations_by_collection_id(
            self,
            app: DefaultFastAPI,
            client: TestClient
    ):
        book_id = 'ace3b113-0980-4ae0-8e24-6d63bd0afa38'
        collection_id = '6c98229d-34bf-4416-be99-f7ea37dc4754'

        access_token = self.get_access_token(client)
        response = client.get(
            self.get_url(f'/collections/recommendations/'),
            headers=self.get_authorization_header(access_token),
            params={
                'book_id': book_id,
                'collection_id': collection_id,
                'limit': 4,
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert all([x['id'] != book_id for x in response.json()])
