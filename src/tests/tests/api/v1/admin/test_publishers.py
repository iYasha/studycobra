from fastapi.testclient import TestClient
from starlette import status

import crud
from logger.in_requests.application import DefaultFastAPI
from sdk.ordering import OrderingManager
from sdk.pagination import PaginationManager
from tests.api.v1.common import TestBase


class TestPublishers(TestBase):
    """Тесты для проверки работоспособности АПИ издателей"""

    publisher_id = 'f91f38cf-3cf5-401d-a988-0beaec56309a'

    def test_publisher_switch_with_one_active_book(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url(f'/publishers/{self.publisher_id}/active'),
            json={
                'is_active': False,
            },
            headers=self.get_authorization_header(access_token),
        )
        ordering = OrderingManager(params='name')
        pagination = PaginationManager(page=1, page_size=25)
        publishers = self.get_async_result(crud.PublisherCRUD.get_publishers_with_books_count(
            language='ru',
            ordering=ordering,
            pagination=pagination)
        )
        assert not all([publisher.is_active for publisher in publishers.results])
        self.get_async_result(crud.BookCRUD.update(obj_id='f4afa085-601c-4157-9c89-9ae069eeffed', is_active=True))
        publishers = self.get_async_result(crud.PublisherCRUD.get_publishers_with_books_count(
            language='ru',
            ordering=ordering,
            pagination=pagination)
        )
        assert any([publisher.is_active for publisher in publishers.results])
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_inactive_publisher(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url(f'/publishers/{self.publisher_id}/active'),
            json={
                'is_active': False,
            },
            headers=self.get_authorization_header(access_token),
        )
        books = self.get_async_result(crud.BookCRUD.get_all(publisher_id=self.publisher_id, language='ru'))
        assert not all([book.is_active for book in books])
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_active_publisher(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url(f'/publishers/{self.publisher_id}/active'),
            json={
                'is_active': True,
            },
            headers=self.get_authorization_header(access_token),
        )
        books = self.get_async_result(crud.BookCRUD.get_all(publisher_id=self.publisher_id, language='ru'))
        assert all([book.is_active for book in books])
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_create_publisher(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url('/publishers/'),
            json={
                'name': 'Odessa',
                'language': 'en'
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), ('language', 'name', 'created_at', 'updated_at', 'id'))

    def test_get_publishers(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/publishers/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(publisher.get('language') for publisher in response_data.get('results')) == {'ru'}
        self.assert_keys(response_data.get('results')[0].keys(), ('language', 'name', 'created_at', 'updated_at', 'id', 'book_count', 'is_active'))

    def test_get_publishers_dropdown(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/publishers/dropdown/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data[0].keys(), ('id', 'name'))

    def test_get_one_publisher(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url(f'/publishers/{self.publisher_id}'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), ('language', 'name', 'created_at', 'updated_at', 'id'))

    def test_update_publisher(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.put(
            self.get_admin_url(f'/publishers/{self.publisher_id}'),
            json={
                "name": "Odessa"
            },
            headers=self.get_authorization_header(access_token),
        )
        publisher = self.get_async_result(crud.PublisherCRUD.get_one(id=self.publisher_id))
        assert publisher.name == "Odessa"
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_publisher(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.delete(
            self.get_admin_url(f'/publishers/{self.publisher_id}'),
            headers=self.get_authorization_header(access_token),
        )
        publisher = self.get_async_result(crud.PublisherCRUD.get_one(id=self.publisher_id))
        assert publisher is None
        assert response.status_code == status.HTTP_204_NO_CONTENT
