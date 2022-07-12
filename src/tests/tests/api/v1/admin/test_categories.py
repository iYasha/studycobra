import json

from fastapi.testclient import TestClient
from starlette import status

import crud
import schemas
from logger.in_requests.application import DefaultFastAPI
from tests.api.v1.common import TestBase


class TestAdminCategories(TestBase):
    """Тесты для проверки работоспособности АПИ категорий"""

    category_id = '675cc7a4-4197-49e5-abf9-1216325fefda'
    book_id = 'f4afa085-601c-4157-9c89-9ae069eeffed'
    collection_id = '6c98229d-34bf-4416-be99-f7ea37dc4754'

    def test_create_category(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url('/categories/'),
            json={
                "language": "en",
                "name": "string",
                "file_id": "6442ed04-e075-4ccb-bb92-41fa17f7077f",
                "index": 3,
                "is_active": False,
                "has_meta": False
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), (
            'created_at', 'updated_at', 'language', 'name', 'file_id', 'index', 'is_active', 'has_meta', 'file', 'id',
            'admin_id', 'meta_link'))

    def test_get_categories_with_search(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/categories/'),
            headers=self.get_authorization_header(access_token),
            params={'q': 'Саморазвитие'}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(category.get('language') for category in response_data.get('results')) == {'ru'}
        assert response_data.get('results')[0].get('name') == 'Саморазвитие'

    def test_get_categories(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/categories/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(category.get('language') for category in response_data.get('results')) == {'ru'}
        self.assert_keys(response_data.get('results')[0].keys(), (
            'created_at', 'updated_at', 'language', 'name', 'file_id', 'index', 'is_active', 'has_meta', 'file',
            'id', 'admin_id', 'books', 'collections', 'meta_link'))
        assert isinstance(response_data.get('results')[0]['books'], int)
        assert isinstance(response_data.get('results')[0]['collections'], int)

    def test_get_categories_dropdown(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/categories/dropdown/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data[0].keys(), ('name', 'id'))

    def test_get_one_category(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url(f'/categories/{self.category_id}'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(tuple(response_data.keys()), (
            'created_at', 'updated_at', 'language', 'name', 'file_id', 'index', 'is_active', 'has_meta', 'file', 'id',
            'admin_id', 'meta_link'))

    def test_update_category(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.put(
            self.get_admin_url(f'/categories/{self.category_id}'),
            json={
                "language": "ru",
                "name": "naw name",
                "file_id": "01b5550e-eb27-41e2-949a-392713c1ef3b",
                "index": 1,
                "is_active": False,
                "has_meta": False
            },
            headers=self.get_authorization_header(access_token),
        )
        category = self.get_async_result(crud.CategoryAdminCRUD.get_one(id=self.category_id))

        data = json.loads(category.json())
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert data == {
            'created_at': data.get('created_at'),
            'updated_at': data.get('updated_at'),
            'language': 'ru',
            'name': 'naw name',
            'file_id': '01b5550e-eb27-41e2-949a-392713c1ef3b',
            'index': 1,
            'is_active': False,
            'has_meta': False,
            'file': None,
            'id': '675cc7a4-4197-49e5-abf9-1216325fefda',
            'admin_id': 1,
            'meta_link': data.get('meta_link')
        }

    def test_delete_category(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.delete(
            self.get_admin_url(f'/categories/{self.category_id}'),
            headers=self.get_authorization_header(access_token),
        )
        category = self.get_async_result(crud.CategoryCRUD.get_one(id=self.category_id))
        book_categories = self.get_async_result(crud.BookCategoryCRUD.get_one(category_id=self.category_id))
        collection_categories = self.get_async_result(
            crud.CollectionCategoryCRUD.get_one(category_id=self.category_id))
        assert category is None
        assert book_categories is None
        assert collection_categories is None
        assert response.status_code == status.HTTP_204_NO_CONTENT
        categories = self.get_async_result(crud.CategoryCRUD.get_all(language='ru'))
        self.assert_keys([category.index for category in categories], list(range(1, len(categories) + 1)))

    def test_get_books_for_category(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/categories/books/'),
            headers=self.get_authorization_header(access_token),
            params={
                'category_id': self.category_id,
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
            'preview', 'audio', 'page_count', 'index', 'age_groups', 'publisher_title'))

    def test_create_or_update_books_for_category(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        request = {
            "category_id": None,
            "book_id": "f4afa085-601c-4157-9c89-9ae069eeffed",
            "index": 3,
            "is_active": True
        }
        response = client.post(
            self.get_admin_url('/categories/books/'),
            json=[
                request
            ],
            params={
                'category_id': self.category_id,
                'page': 1,
                'page_size': 25
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        books = self.get_async_result(crud.BookCategoryCRUD.get_all(category_id=self.category_id))
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.get('results')[0].keys(), (
            'language', 'book_type', 'name', 'publisher_id', 'free_page_count', 'preview_id', 'audio_id',
            'background', 'is_active', 'has_meta', 'created_at', 'updated_at', 'id', 'admin_id', 'meta_link',
            'preview', 'audio', 'page_count', 'index', 'age_groups', 'publisher_title'))
        self.assert_keys(books[0].dict().keys(), ('book_id', 'category_id', 'index', 'is_active'))
        assert books == [schemas.BookCategory.parse_obj({**request, 'category_id': self.category_id})]

    def test_get_collections_for_category(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/categories/collections/'),
            headers=self.get_authorization_header(access_token),
            params={
                'category_id': self.category_id,
                'page': 1,
                'page_size': 25
            }
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(collection.get('language') for collection in response_data.get('results')) == {'ru'}
        self.assert_keys(response_data.get('results')[0].keys(), (
            'created_at', 'updated_at', 'title', 'cover_type', 'text_color', 'language', 'background_color',
            'is_active', 'file_id', 'file', 'id', 'index', 'age_groups', 'admin_id'))

    def test_create_or_update_collections_for_category(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        request = {
            "category_id": None,
            "collection_id": "9af897fb-ce5d-432b-86d9-4340c0f6ea04",
            "index": 3,
            "is_active": True
        }
        response = client.post(
            self.get_admin_url('/categories/collections/'),
            json=[
                request
            ],
            params={
                'category_id': self.category_id,
                'page': 1,
                'page_size': 25
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        collections = self.get_async_result(crud.CollectionCategoryCRUD.get_all(category_id=self.category_id))
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.get('results')[0].keys(), (
            'created_at', 'updated_at', 'title', 'cover_type', 'text_color', 'language', 'background_color',
            'is_active', 'file_id', 'file', 'id', 'index', 'age_groups', 'admin_id'))
        self.assert_keys(collections[0].dict().keys(), ('collection_id', 'category_id', 'index', 'is_active'))
        assert collections == [schemas.CollectionCategory.parse_obj({**request, 'category_id': self.category_id})]

    def test_duplicate_category(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url(f'/categories/{self.category_id}/duplicate/'),
            headers=self.get_authorization_header(access_token),
        )
        assert response.status_code == status.HTTP_200_OK
        except_fields = {'created_at', 'admin_id', 'file', 'meta_link', 'index'}
        response_data = {key: value for key, value in response.json().items() if key not in except_fields}

        old_books = self.get_async_result(crud.BookCategoryCRUD.get_all(category_id=self.category_id))
        old_books = [book.dict(exclude={'category_id'}) for book in old_books]
        new_books = self.get_async_result(crud.BookCategoryCRUD.get_all(category_id=response_data['id']))
        new_books = [book.dict(exclude={'category_id'}) for book in new_books]
        assert old_books == new_books

        old_collections = self.get_async_result(crud.CollectionCategoryCRUD.get_all(category_id=self.category_id))
        old_collections = [book.dict(exclude={'category_id'}) for book in old_collections]
        new_collections = self.get_async_result(crud.CollectionCategoryCRUD.get_all(category_id=response_data['id']))
        new_collections = [book.dict(exclude={'category_id'}) for book in new_collections]
        assert old_collections == new_collections

        old_collection = json.loads(self.get_async_result(crud.CategoryAdminCRUD.get_one(id=self.category_id)).json(
            exclude=except_fields))
        response_data.pop('id')
        old_collection.pop('id')
        assert response_data == old_collection
        categories = self.get_async_result(crud.CategoryCRUD.get_all(language='ru'))
        self.assert_keys([category.index for category in categories], list(range(1, len(categories) + 1)))

    def test_create_category_with_various_indexes(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        request = {
            "language": "ru",
            "name": "string",
            "file_id": "6442ed04-e075-4ccb-bb92-41fa17f7077f",
            "index": 100,
            "is_active": False,
            "has_meta": False
        }
        response_big_index = client.post(
            self.get_admin_url('/categories/'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        assert response_big_index.status_code == status.HTTP_200_OK
        categories = self.get_async_result(crud.CategoryCRUD.get_all(language='ru'))
        self.assert_keys([category.index for category in categories], list(range(1, len(categories) + 1)))

        request['index'] = 2
        response_small_index = client.post(
            self.get_admin_url('/categories/'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        assert response_small_index.status_code == status.HTTP_200_OK
        categories = self.get_async_result(crud.CategoryCRUD.get_all(language='ru'))
        self.assert_keys([category.index for category in categories], list(range(1, len(categories) + 1)))

    def test_update_category_with_various_indexes(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        request = {
            "language": "ru",
            "name": "naw name",
            "file_id": "01b5550e-eb27-41e2-949a-392713c1ef3b",
            "index": 1,
            "is_active": False,
            "has_meta": False
        }
        response_big_index = client.put(
            self.get_admin_url(f'/categories/{self.category_id}'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        assert response_big_index.status_code == status.HTTP_204_NO_CONTENT
        categories = self.get_async_result(crud.CategoryAdminCRUD.get_all(language='ru'))
        self.assert_keys([category.index for category in categories], list(range(1, len(categories) + 1)))

        request['index'] = 2

        response_small_index = client.put(
            self.get_admin_url(f'/categories/{self.category_id}'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        assert response_small_index.status_code == status.HTTP_204_NO_CONTENT
        categories = self.get_async_result(crud.CollectionCategoryCRUD.get_all(language='en'))
        self.assert_keys([category.index for category in categories], list(range(1, len(categories) + 1)))

    def test_swap_index_in_categories(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        first_category_before = self.get_async_result(
            crud.CategoryCRUD.get_one(id='675cc7a4-4197-49e5-abf9-1216325fefda'))
        second_category_before = self.get_async_result(
            crud.CategoryCRUD.get_one(id='02da1191-a1ec-411d-a1c2-53ed62d61aa7'))

        response = client.put(
            self.get_admin_url(f'/categories/swap/'),
            json={
                "first_obj_pk": '675cc7a4-4197-49e5-abf9-1216325fefda',
                "second_obj_pk": '02da1191-a1ec-411d-a1c2-53ed62d61aa7'
            },
            headers=self.get_authorization_header(access_token),
        )
        first_category_after = self.get_async_result(
            crud.CategoryCRUD.get_one(id='675cc7a4-4197-49e5-abf9-1216325fefda'))
        second_category_after = self.get_async_result(
            crud.CategoryCRUD.get_one(id='02da1191-a1ec-411d-a1c2-53ed62d61aa7'))
        assert first_category_before.index == second_category_after.index
        assert first_category_after.index == second_category_before.index
        assert response.status_code == status.HTTP_204_NO_CONTENT
        categories = self.get_async_result(crud.CategoryCRUD.get_all(language='en'))
        self.assert_keys([category.index for category in categories], list(range(1, len(categories) + 1)))
