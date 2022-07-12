from fastapi.testclient import TestClient
from starlette import status

import crud
from logger.in_requests.application import DefaultFastAPI
from tests.api.v1.common import TestBase


class TestMostPopularRequests(TestBase):
    """Тесты для проверки работоспособности АПИ популярных запросов"""

    most_popular_request_id = 'df479161-6d4b-47ef-a99d-ce69610d8983'

    def test_create_popular_request(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url('/most-popular-requests/'),
            json={
                "language": "ru",
                "query": "new query",
                "count": 0,
                "index": 1,
                "is_published": True,
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(),
                         ('language', 'query', 'count', 'index', 'is_published', 'is_autocomplete', 'id'))

    def test_get_popular_request(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/most-popular-requests/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(most_popular_request.get('language') for most_popular_request in response_data) == {'ru'}
        self.assert_keys(response_data[0].keys(),
                         ('language', 'query', 'count', 'index', 'is_published', 'is_autocomplete', 'id'))

    def test_get_one_popular_request(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url(f'/most-popular-requests/{self.most_popular_request_id}'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(),
                         ('language', 'query', 'count', 'index', 'is_published', 'is_autocomplete', 'id'))

    def test_update_popular_request(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        request = {
            "language": "ru",
            "query": "updated query",
            "count": 12,
            "index": 4,
            "is_published": False,
            "is_autocomplete": False
        }
        response = client.put(
            self.get_admin_url(f'/most-popular-requests/{self.most_popular_request_id}'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        popular_request = self.get_async_result(crud.MostPopularRequestCRUD.get_one(id=self.most_popular_request_id))
        request['id'] = popular_request.id
        assert popular_request.dict() == request
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_popular_request(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.delete(
            self.get_admin_url(f'/most-popular-requests/{self.most_popular_request_id}'),
            headers=self.get_authorization_header(access_token),
        )
        popular_request = self.get_async_result(crud.MostPopularRequestCRUD.get_one(id=self.most_popular_request_id))
        assert popular_request is None
        assert response.status_code == status.HTTP_204_NO_CONTENT
        popular_requests = self.get_async_result(crud.CategoryCRUD.get_all(language='ru'))
        self.assert_keys([popular_request.index for popular_request in popular_requests],
                         list(range(1, len(popular_requests) + 1))) 
 
    def test_create_popular_request_is_published_error(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        request = {
            "language": "ru",
            "query": "new query",
            "count": 0,
            "index": 1,
            "is_published": True,
        }
        client.post(
            self.get_admin_url('/most-popular-requests/'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        response = client.post(
            self.get_admin_url('/most-popular-requests/'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response_data.get('field_errors')[0] == {'field': 'is_published',
                                                        'message': 'A maximum of 5 requests can be published'}
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_popular_request_is_published_error(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        request = {
                "language": "ru",
                "query": "new query",
                "count": 0,
                "index": 1,
                "is_published": True,
            }
        client.post(
            self.get_admin_url('/most-popular-requests/'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )

        new_popular_search = client.post(
            self.get_admin_url('/most-popular-requests/'),
            json={**request, 'is_published': False},
            headers=self.get_authorization_header(access_token),
        )
        response = client.put(
            self.get_admin_url(f'/most-popular-requests/{new_popular_search.json()["id"]}'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_popular_request_with_various_indexes(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        request = {
            "language": "ru",
            "query": "new query",
            "count": 0,
            "index": 100,
            "is_published": False,
        }
        response_big_index = client.post(
            self.get_admin_url('/most-popular-requests/'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        assert response_big_index.status_code == status.HTTP_200_OK
        most_popular_requests = self.get_async_result(crud.MostPopularRequestCRUD.get_all(language='ru'))
        self.assert_keys([popular_request.index for popular_request in most_popular_requests],
                         [x for x in range(1, len(most_popular_requests) + 1)])

        request['index'] = 2
        response_small_index = client.post(
            self.get_admin_url('/most-popular-requests/'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        assert response_small_index.status_code == status.HTTP_200_OK
        most_popular_requests = self.get_async_result(crud.MostPopularRequestCRUD.get_all(language='ru'))
        self.assert_keys([popular_request.index for popular_request in most_popular_requests],
                         [x for x in range(1, len(most_popular_requests) + 1)])

    def test_update_popular_request_with_various_indexes(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        request = {
            "language": "ru",
            "query": "updated query",
            "count": 12,
            "index": 4,
            "is_published": False,
            "is_autocomplete": False
        }
        response_big_index = client.put(
            self.get_admin_url(f'/most-popular-requests/{self.most_popular_request_id}'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        assert response_big_index.status_code == status.HTTP_204_NO_CONTENT
        categories = self.get_async_result(crud.MostPopularRequestCRUD.get_all(language='ru'))
        self.assert_keys([category.index for category in categories], list(range(1, len(categories) + 1)))

        request['index'] = 2

        response_small_index = client.put(
            self.get_admin_url(f'/most-popular-requests/{self.most_popular_request_id}'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        assert response_small_index.status_code == status.HTTP_204_NO_CONTENT
        popular_requests = self.get_async_result(crud.MostPopularRequestCRUD.get_all(language='ru'))
        self.assert_keys([popular_request.index for popular_request in popular_requests], list(range(1, len(popular_requests) + 1)))

    def test_swap_index_in_popular_request(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        first_popular_request_before = self.get_async_result(crud.MostPopularRequestCRUD.get_one(index=1))
        second_popular_request_before = self.get_async_result(crud.MostPopularRequestCRUD.get_one(index=2))

        response = client.put(
            self.get_admin_url(f'/most-popular-requests/swap/'),
            json={
                "first_obj_pk": 'df479161-6d4b-47ef-a99d-ce69610d8983',
                "second_obj_pk": 'f12dd007-c484-4c02-9832-bbd59c0b3d0f'
            },
            headers=self.get_authorization_header(access_token),
        )
        first_popular_request_after = self.get_async_result(crud.MostPopularRequestCRUD.get_one(index=2))
        second_popular_request_after = self.get_async_result(crud.MostPopularRequestCRUD.get_one(index=1))
        assert first_popular_request_before.id == first_popular_request_after.id
        assert second_popular_request_before.id == second_popular_request_after.id
        assert response.status_code == status.HTTP_204_NO_CONTENT
        popular_requests = self.get_async_result(crud.CategoryCRUD.get_all(language='ru'))
        self.assert_keys([popular_request.index for popular_request in popular_requests], list(range(1, len(popular_requests) + 1)))
