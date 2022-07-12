from fastapi.testclient import TestClient
from starlette import status

import crud
from logger.in_requests.application import DefaultFastAPI
from sso_auth.utils import get_user_data_from_token
from tests.api.v1.common import TestBase


class TestBooks(TestBase):

    def test_unauthorized_user_cant_see_books(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        response = client.get(
            self.get_url('/books')
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_unauthorized_user_cant_see_book(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        response = client.get(
            self.get_url('/books/f4afa085-601c-4157-9c89-9ae069eeffed')
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_books(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_token(client)

        response = client.get(
            self.get_url('/books'),
            headers=self.get_authorization_header(access_token)
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(book.get('language') for book in response_data) == {'ru'}
        self.assert_keys(response_data[0].keys(), (
            'language', 'book_type', 'name', 'publisher_id', 'free_page_count', 'preview_id', 'audio_id', 'background',
            'is_active', 'has_meta', 'created_at', 'updated_at', 'id', 'admin_id', 'meta_link', 'preview', 'audio',
            'page_count'))

    def test_get_books_with_aa_language(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_token(client)

        response = client.get(
            self.get_url('/books'),
            headers=self.get_authorization_header(access_token, language='ea')
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_data == []

    def test_get_one_book(
            self,
            app: DefaultFastAPI,
            client: TestClient
    ):
        access_token = self.get_access_token(client)

        response = client.get(
            self.get_url('/books/f4afa085-601c-4157-9c89-9ae069eeffed'),
            headers=self.get_authorization_header(access_token)
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), (
            'language', 'book_type', 'name', 'publisher_id', 'free_page_count', 'preview_id', 'audio_id', 'background',
            'is_active', 'has_meta', 'created_at', 'updated_at', 'id', 'admin_id', 'meta_link', 'preview', 'audio',
            'pages',
            'page_count', 'is_favorite', 'current_page_id', 'time_code'))

    def test_book_favorite(
            self,
            app: DefaultFastAPI,
            client: TestClient
    ):
        book_id = 'f4afa085-601c-4157-9c89-9ae069eeffed'
        access_token = self.get_access_token(client)

        def add_favorite():
            response = client.post(
                self.get_url(f'/books/favorite/{book_id}'),
                headers=self.get_authorization_header(access_token)
            )
            assert response.status_code == status.HTTP_204_NO_CONTENT

        def get_favorite():
            response = client.get(
                self.get_url(f'/books/favorite/'),
                headers=self.get_authorization_header(access_token)
            )
            assert response.status_code == status.HTTP_200_OK
            return response.json()

        def remove_favorite():
            response = client.delete(
                self.get_url(f'/books/favorite/{book_id}'),
                headers=self.get_authorization_header(access_token)
            )
            assert response.status_code == status.HTTP_204_NO_CONTENT

        add_favorite()
        favorites = get_favorite()
        self.assert_keys(favorites.keys(), ('data', 'recommended'))
        self.assert_keys(favorites['data'][0].keys(), (
            'language', 'book_type', 'name', 'publisher_id', 'free_page_count', 'preview_id', 'audio_id', 'background',
            'is_active', 'has_meta', 'created_at', 'updated_at', 'id', 'admin_id', 'meta_link', 'preview', 'audio',
            'page_count'))
        remove_favorite()
        assert get_favorite()['data'] == []

    def test_vote_for_book(
            self,
            app: DefaultFastAPI,
            client: TestClient
    ):
        book_id = 'f4afa085-601c-4157-9c89-9ae069eeffed'
        access_token = self.get_access_token(client)

        response = client.post(
            self.get_url(f'/books/{book_id}/vote'),
            json={'vote_type': 'like'},
            headers=self.get_authorization_header(access_token)
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_book_activity(
            self,
            app: DefaultFastAPI,
            client: TestClient
    ):
        book_id = 'ace3b113-0980-4ae0-8e24-6d63bd0afa38'
        page_id = '9a93c622-10bb-45f7-86f3-bddddb07c243'
        access_token = self.get_access_token(client)

        response = client.post(
            self.get_url(f'/books/{book_id}/page/{page_id}/activity'),
            json={
                "status": "finished",
                "time_code": 0
            },
            headers=self.get_authorization_header(access_token),
            params={
                'book_id': book_id,
                'page_id': page_id
            }
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        user_data = get_user_data_from_token(access_token)
        book_activity = self.get_async_result(
            crud.BookCRUD.get_activity_by_book_id(book_id=book_id, user_id=user_data.get('sub')))
        page_activity = self.get_async_result(crud.PageCRUD.get_activities(book_activity_id=book_activity.id))
        assert book_activity
        assert page_activity
