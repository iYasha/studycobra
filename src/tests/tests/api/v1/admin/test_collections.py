import json

from fastapi.testclient import TestClient
from starlette import status

import crud
import schemas
from logger.in_requests.application import DefaultFastAPI
from tests.api.v1.common import TestBase


class TestAdminCollections(TestBase):
    collection_id = '9af897fb-ce5d-432b-86d9-4340c0f6ea04'
    collection_id_with_books = '6c98229d-34bf-4416-be99-f7ea37dc4754'
    book_id = 'f4afa085-601c-4157-9c89-9ae069eeffed'

    def test_create_collection(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url('/collections/'),
            json={
                "language": "ru",
                "title": "Collection name",
                "cover_type": "image",
                "file_id": "6442ed04-e075-4ccb-bb92-41fa17f7077f",
                "text_color": "string",
                "background_color": "string",
                "index": 2,
                "has_meta": False,
                "is_active": False
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), (
            'created_at', 'updated_at', 'id', 'language', 'title', 'cover_type', 'file_id', 'text_color',
            'background_color', 'index', 'has_meta', 'is_active', 'admin_id', 'meta_link', 'file'))

    def test_get_collections_with_search(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/collections/'),
            headers=self.get_authorization_header(access_token),
            params={
                'q': 'Бизнес'
            }
        )
        response_data = response.json()
        assert set(collection.get('language') for collection in response_data.get('results')) == {'ru'}
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.get('results')[0].get('title'), 'Бизнес')

    def test_get_collections(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/collections/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(collection.get('language') for collection in response_data.get('results')) == {'ru'}
        self.assert_keys(response_data.get('results')[0].keys(), (
            'created_at', 'updated_at', 'id', 'language', 'title', 'cover_type', 'file_id', 'text_color',
            'background_color', 'index', 'has_meta', 'is_active', 'admin_id', 'meta_link', 'file', 'age_groups'))

    def test_get_collections_dropdown(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/collections/dropdown/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data[0].keys(), ('id', 'title'))

    def test_get_one_collection(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url(f'/collections/{self.collection_id}'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), (
            'created_at', 'updated_at', 'id', 'language', 'title', 'cover_type', 'file_id', 'text_color',
            'background_color', 'index', 'has_meta', 'is_active', 'admin_id', 'meta_link', 'file'))

    def test_update_collections(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.put(
            self.get_admin_url(f'/collections/{self.collection_id}'),
            json={
                "language": "en",
                "title": "string",
                "cover_type": "image",
                "file_id": "0bdf3b54-0ad8-49db-b06d-b76ed6d6d368",
                "text_color": "#000000",
                "background_color": "#111111",
                "index": 0,
                "has_meta": False,
                "is_active": True
            },
            headers=self.get_authorization_header(access_token),
        )
        collection = self.get_async_result(crud.CollectionAdminCRUD.get_one(id=self.collection_id))
        collection = json.loads(collection.json())
        assert collection == {
            "created_at": collection.get('created_at'),
            "updated_at": collection.get('updated_at'),
            "id": self.collection_id,
            "language": "en",
            "title": "string",
            "cover_type": "image",
            "file_id": "0bdf3b54-0ad8-49db-b06d-b76ed6d6d368",
            "text_color": "#000000",
            "background_color": "#111111",
            "index": 0,
            "has_meta": False,
            "is_active": True,
            "admin_id": collection.get('admin_id'),
            "meta_link": None,
            "file": None
        }
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_collection(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.delete(
            self.get_admin_url(f'/collections/{self.collection_id}'),
            headers=self.get_authorization_header(access_token),
        )
        collection = self.get_async_result(crud.CollectionAdminCRUD.get_one(id=self.collection_id))
        assert collection is None
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_get_books_for_collection(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/collections/books/'),
            headers=self.get_authorization_header(access_token),
            params={
                'collection_id': self.collection_id_with_books,
                'page': 1,
                'page_size': 25
            }
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(book.get('language') for book in response_data.get('results')) == {'ru'}
        self.assert_keys(response_data.get('results')[0].keys(), (
            'language', 'book_type', 'name', 'publisher_id', 'free_page_count', 'preview_id', 'audio_id',
            'background', 'is_active', 'has_meta', 'created_at', 'updated_at', 'id', 'admin_id', 'meta_link',
            'preview', 'audio', 'page_count', 'index', 'categories', 'publisher_title'))

    def test_create_or_update_books_for_collection(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        request = {
            "collection_id": None,
            "book_id": "f4afa085-601c-4157-9c89-9ae069eeffed",
            "index": 3,
            "is_active": True
        }
        response = client.post(
            self.get_admin_url('/collections/books/'),
            json=[
                request
            ],
            params={
                'collection_id': self.collection_id,
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        books = self.get_async_result(crud.BookCollectionCRUD.get_all(collection_id=self.collection_id))
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.get('results')[0].keys(), (
            'language', 'book_type', 'name', 'publisher_id', 'free_page_count', 'preview_id', 'audio_id',
            'background', 'is_active', 'has_meta', 'created_at', 'updated_at', 'id', 'admin_id', 'meta_link',
            'preview', 'audio', 'page_count', 'index', 'categories', 'publisher_title'))
        self.assert_keys(books[0].dict().keys(), ('book_id', 'collection_id', 'index', 'is_active'))
        assert books == [schemas.BookCollection.parse_obj({**request, 'collection_id': self.collection_id})]

    def test_get_collections_settings(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/collections/settings/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), ('text_color', 'background_color', 'use_default_cover'))

    def test_post_collections_settings(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url('/collections/settings/'),
            headers=self.get_authorization_header(access_token),
            json={
                "text_color": "#fff000",
                "background_color": "#000000",
                "cover_type": "default"
            }
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        settings = self.get_async_result(crud.CollectionAdminCRUD.get_settings(language='ru'))
        assert dict(settings) == {'text_color': '#fff000', 'background_color': '#000000',
                                  'use_default_cover': True}

    def test_get_collection_preview(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url(f'/collections/{self.collection_id_with_books}/preview/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(),
                         ('name', 'background_color', 'text_color', 'file_id', 'inner_image', 'books'))
        self.assert_keys(response_data.get('books')[0].keys(), ('preview_id', 'preview', 'background'))

    def test_duplicate_collection(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url(f'/collections/{self.collection_id_with_books}/duplicate/'),
            headers=self.get_authorization_header(access_token),
        )
        assert response.status_code == status.HTTP_200_OK
        except_fields = {'created_at', 'admin_id', 'file', 'meta_link'}
        response_data = {key: value for key, value in response.json().items() if key not in except_fields}
        old_books = self.get_async_result(crud.BookCollectionCRUD.get_all(collection_id=self.collection_id_with_books))
        old_books = [book.dict(exclude={'collection_id'}) for book in old_books]
        new_books = self.get_async_result(crud.BookCollectionCRUD.get_all(collection_id=response_data['id']))
        new_books = [book.dict(exclude={'collection_id'}) for book in new_books]
        assert old_books == new_books
        old_collection = json.loads(
            self.get_async_result(crud.CollectionAdminCRUD.get_one(id=self.collection_id_with_books)).json(
                exclude=except_fields))
        response_data.pop('id')
        old_collection.pop('id')
        assert response_data == old_collection
