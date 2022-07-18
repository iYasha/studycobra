import json

from fastapi.testclient import TestClient
from starlette import status

import crud
from logger.in_requests.application import DefaultFastAPI
from tests.api.v1.common import TestBase


class TestAdminBooks(TestBase):
    """Тесты для проверки работоспособности АПИ книг и страниц"""

    book_id = 'f4afa085-601c-4157-9c89-9ae069eeffed'
    page_id = '20503794-b40a-4c80-ac13-b6d44a7e38fb'

    def test_create_book(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        request = {
            "language": "ru",
            "book_type": "media",
            "name": "new book",
            "publisher_id": "f91f38cf-3cf5-401d-a988-0beaec56309a",
            "free_page_count": 4,
            "preview_id": "01b5550e-eb27-41e2-949a-392713c1ef3b",
            "audio_id": "4e4f1c15-75c8-41c8-9960-b4d24e3e2721",
            "background": "red",
            "is_active": True,
            "has_meta": False,
            "authors": [
                "2d742eaa-1306-4d83-ad4e-a4f4d7df8ce9"
            ],
            "collections": [
                "6c98229d-34bf-4416-be99-f7ea37dc4754",
                "9af897fb-ce5d-432b-86d9-4340c0f6ea04"
            ],
            "categories": [
                "675cc7a4-4197-49e5-abf9-1216325fefda"
            ],
            "age_groups": [
                "bec877b3-1248-4d16-a09e-6a999e90919d"
            ],
            "series": [
                "eb97c6e9-6fd1-4765-aa84-efeb193836de"
            ],
            "tags": [
                "1b10761d-862b-4494-a22a-9a702e27d1e8"
            ]
        }
        response = client.post(
            self.get_admin_url('/books/'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), ('language', 'book_type', 'name', 'publisher_id', 'free_page_count',
                                                'preview_id', 'audio_id', 'background', 'is_active', 'has_meta',
                                                'created_at', 'updated_at', 'id', 'admin_id', 'meta_link', 'preview',
                                                'audio', 'page_count', 'authors', 'collections', 'categories',
                                                'age_groups', 'series', 'tags', 'like', 'dislike', 'avg_rating'))

    def test_get_books_with_search(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/books/'),
            headers=self.get_authorization_header(access_token),
            params={'q': 'Покорители Глубин. История подводных погружений'}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(book.get('language') for book in response_data.get('results')) == {'ru'}
        assert response_data.get('results')[0].get('name') == 'Покорители Глубин. История подводных погружений'

    def test_get_books(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/books/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(book.get('language') for book in response_data.get('results')) == {'ru'}
        self.assert_keys(response_data.get('results')[0].keys(),
                         ('language', 'book_type', 'name', 'publisher_id', 'free_page_count',
                          'preview_id', 'audio_id', 'background', 'is_active', 'has_meta',
                          'created_at', 'updated_at', 'id', 'admin_id', 'meta_link', 'preview',
                          'audio', 'page_count', 'authors', 'collections', 'categories',
                          'age_groups', 'series', 'tags', 'publisher_title'))

    def test_get_one_book(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url(f'/books/{self.book_id}'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), ('language', 'book_type', 'name', 'publisher_id', 'free_page_count',
                                                'preview_id', 'audio_id', 'background', 'is_active', 'has_meta',
                                                'created_at', 'updated_at', 'id', 'admin_id', 'meta_link', 'preview',
                                                'audio', 'page_count', 'authors', 'collections', 'categories',
                                                'age_groups', 'series', 'tags', 'like', 'dislike', 'avg_rating'))

    def test_update_book(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        request = {
            "language": "ru",
            "book_type": "media",
            "name": "updated",
            "publisher_id": "f91f38cf-3cf5-401d-a988-0beaec56309a",
            "free_page_count": 10,
            "preview_id": "3c772f65-99c6-49db-ada3-2319b0c0b4fa",
            "audio_id": "f910e762-c2aa-4c24-9a25-d4517b0a709c",
            "background": "black",
            "is_active": False,
            "has_meta": True,
            "authors": [
                "9acaff2e-4dae-4dcd-b10d-26c8db0d734f"
            ],
            "collections": [
                "6c98229d-34bf-4416-be99-f7ea37dc4754"
            ],
            "categories": [
                "02da1191-a1ec-411d-a1c2-53ed62d61aa7"
            ],
            "age_groups": [
                "bec877b3-1248-4d16-a09e-6a999e90919d"
            ],
            "series": [],
            "tags": []
        }

        response = client.put(
            self.get_admin_url(f'/books/{self.book_id}'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        book = self.get_async_result(crud.BookCRUD.get_book_detail(book_id=self.book_id))
        book = json.loads(book.json())
        request.update({
            "like": 0,
            "dislike": 0,
            "avg_rating": 0,
            "page_count": book.get('page_count'),
            "audio": book.get('audio'),
            "preview": book.get('preview'),
            "meta_link": book.get('meta_link'),
            "admin_id": book.get('admin_id'),
            "id": book.get('id'),
            "updated_at": book.get('updated_at'),
            "created_at": book.get('created_at')
        })
        assert book == request
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_book(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.delete(
            self.get_admin_url(f'/books/{self.book_id}'),
            headers=self.get_authorization_header(access_token),
        )
        book = self.get_async_result(crud.BookCRUD.get_one(id=self.book_id))
        assert book is None
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_duplicate_book(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url(f'/books/{self.book_id}/duplicate'),
            headers=self.get_authorization_header(access_token),
        )
        assert response.status_code == status.HTTP_200_OK
        except_fields = {'created_at', 'admin_id', 'preview', 'audio', 'meta_link', 'page_count'}
        response_data = {key: value for key, value in response.json().items() if key not in except_fields}
        old_book_pages = self.get_async_result(crud.PageCRUD.get_all(book_id=self.book_id))
        new_book_pages = self.get_async_result(crud.PageCRUD.get_all(book_id=response_data.get('id')))
        assert len(old_book_pages) == len(new_book_pages)
        response_data.pop('id')
        except_fields.add('id')
        old_book = json.loads(self.get_async_result(crud.BookCRUD.get_book_detail(self.book_id)).json(
            exclude=except_fields))
        assert response_data == old_book

    def test_get_books_settings(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/books/settings/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), ('background', 'free_page_count'))

    def test_post_books_settings(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url('/books/settings/'),
            headers=self.get_authorization_header(access_token),
            json={
                "background": "black",
                "free_page_count": 10
            }
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        settings = self.get_async_result(crud.BookCRUD.get_settings_books(language='ru'))
        assert dict(settings) == {"background": "black", "free_page_count": 10}

    def test_get_books_pages(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/books/pages/'),
            params={
                'book_id': self.book_id
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.get('results')[0].keys(),
                         ('book_id', 'name', 'index', 'audio_id', 'image_id', 'time_code',
                          'image_direction', 'created_at', 'updated_at', 'audio', 'image',
                          'id', 'file_name'))

    def test_get_book_excel(
            self,
            app: DefaultFastAPI,
            client: TestClient
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/books/export/'),
            headers=self.get_authorization_header(access_token),
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_books_with_filters(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        # Book types filter
        response = client.get(
            self.get_admin_url('/books/'),
            headers=self.get_authorization_header(access_token),
            params={'book_types': 'time_code'}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(book.get('language') for book in response_data.get('results')) == {'ru'}
        assert set([book.get('book_type') for book in response_data.get('results')]) == {'time_code'}

        # Publisher filter
        response = client.get(
            self.get_admin_url('/books/'),
            headers=self.get_authorization_header(access_token),
            params={'publisher_id': ['315e66f5-d4e2-4eba-8a4e-70ec049e27a5']}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(book.get('language') for book in response_data.get('results')) == {'ru'}
        assert set([book.get('publisher_id') for book in response_data.get('results')]) == {
            '315e66f5-d4e2-4eba-8a4e-70ec049e27a5'}

        # Category filter
        response = client.get(
            self.get_admin_url('/books/'),
            headers=self.get_authorization_header(access_token),
            params={'category_ids': ['675cc7a4-4197-49e5-abf9-1216325fefda']}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(book.get('language') for book in response_data.get('results')) == {'ru'}
        categories = [book.get('categories') for book in response_data.get('results')]
        if categories:
            for category in categories:
                assert '675cc7a4-4197-49e5-abf9-1216325fefda' in category

        # Collection filter
        response = client.get(
            self.get_admin_url('/books/'),
            headers=self.get_authorization_header(access_token),
            params={'collection_ids': ['9af897fb-ce5d-432b-86d9-4340c0f6ea04']}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(book.get('language') for book in response_data.get('results')) == {'ru'}
        collections = [book.get('collections') for book in response_data.get('results')]
        if collections:
            for collection in collections:
                assert '9af897fb-ce5d-432b-86d9-4340c0f6ea04' in collection

        # Author filter
        response = client.get(
            self.get_admin_url('/books/'),
            headers=self.get_authorization_header(access_token),
            params={'author_ids': ['2d742eaa-1306-4d83-ad4e-a4f4d7df8ce9']}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(book.get('language') for book in response_data.get('results')) == {'ru'}
        authors = [book.get('authors') for book in response_data.get('results')]
        if authors:
            for author in authors:
                assert '2d742eaa-1306-4d83-ad4e-a4f4d7df8ce9' in author

        # Age group filter
        response = client.get(
            self.get_admin_url('/books/'),
            headers=self.get_authorization_header(access_token),
            params={'age_group_ids': ['bec877b3-1248-4d16-a09e-6a999e90919d']}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(book.get('language') for book in response_data.get('results')) == {'ru'}
        age_groups = [book.get('age_groups') for book in response_data.get('results')]
        if age_groups:
            for age_group in age_groups:
                assert 'bec877b3-1248-4d16-a09e-6a999e90919d' in age_group

        # Series filter
        response = client.get(
            self.get_admin_url('/books/'),
            headers=self.get_authorization_header(access_token),
            params={'series_ids': ['5a539a6f-5415-4cc6-8473-3f17d28cc071']}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(book.get('language') for book in response_data.get('results')) == {'ru'}
        series = [book.get('series') for book in response_data.get('results')]
        if series:
            for seria in series:
                assert '5a539a6f-5415-4cc6-8473-3f17d28cc071' in seria

        # Tag filter
        response = client.get(
            self.get_admin_url('/books/'),
            headers=self.get_authorization_header(access_token),
            params={'tag_ids': ['096af069-a0e8-4ede-8edc-2a029691abef']}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(book.get('language') for book in response_data.get('results')) == {'ru'}
        tags = [book.get('tags') for book in response_data.get('results')]
        if tags:
            for tag in tags:
                assert '096af069-a0e8-4ede-8edc-2a029691abef' in tag

    def test_create_or_update_pages_for_book(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)

        response = client.get(
            self.get_admin_url('/books/pages/'),
            params={
                'book_id': self.book_id
            },
            headers=self.get_authorization_header(access_token)
        )
        response_data = response.json()
        total_count = response_data.get('total_count')

        request = [
            {
                "name": None,
                "index": 1,
                "audio_id": None,
                "image_id": "6442ed04-e075-4ccb-bb92-41fa17f7077f",
                "time_code": None,
                "image_direction": "left",
                "id": None,
                "is_deleted": False
            },
            {
                "name": "update",
                "index": 2,
                "audio_id": None,
                "image_id": "0bdf3b54-0ad8-49db-b06d-b76ed6d6d368",
                "time_code": None,
                "image_direction": "right",
                "id": "403ea06c-a5c2-4800-b3da-05bc20122f01",
                "is_deleted": False
            },
            {
                "name": None,
                "index": 3,
                "audio_id": None,
                "image_id": "6d9260fc-fee9-497c-a528-37c2cfdd8d6d",
                "time_code": None,
                "image_direction": "left",
                "id": "20503794-b40a-4c80-ac13-b6d44a7e38fb",
                "is_deleted": True
            }
        ]
        response = client.post(
            self.get_admin_url('/books/pages/'),
            headers=self.get_authorization_header(access_token),
            params={'book_id': self.book_id},
            json=request
        )
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        self.assert_keys(response_data.get('results')[0].keys(),
                         ('book_id', 'name', 'index', 'audio_id', 'image_id', 'time_code',
                          'image_direction', 'created_at', 'updated_at', 'audio', 'image',
                          'id', 'file_name'))
        deleted_page = self.get_async_result(crud.PageCRUD.get_one(id='20503794-b40a-4c80-ac13-b6d44a7e38fb'))
        assert deleted_page is None
        updated_page = self.get_async_result(crud.PageCRUD.get_one(id='403ea06c-a5c2-4800-b3da-05bc20122f01'))
        updated_page = dict(updated_page)
        updated_page.update({
            'image_id': str(updated_page.get('image_id')),
            'id': str(updated_page.get('id')),
        })
        pop_elems = ('created_at', 'updated_at', 'book_id', 'audio', 'image', 'file_name')
        for elem in pop_elems:
            updated_page.pop(elem)
        request[1].pop('is_deleted')
        assert dict(updated_page) == request[1]
        assert total_count == response_data.get('total_count')
