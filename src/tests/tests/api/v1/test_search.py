from fastapi.testclient import TestClient
from starlette import status

from logger.in_requests.application import DefaultFastAPI
from tests.api.v1.common import TestBase


class TestSearch(TestBase):
    def test_unauthorized_user_cant_search(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        response = client.get(
            self.get_url('/search/'),
            headers={'language': 'ru'},
            params={'q': 'Покорители'}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_unauthorized_user_cant_see_most_popular(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        response = client.get(
            self.get_url('/search/popular'),
            headers={'language': 'ru'},
            params={'q': 'Покорители'}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_search_result(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_token(client)
        response = client.get(
            self.get_url(f'/search/'),
            headers=self.get_authorization_header(access_token),
            params={'q': 'Покорители'}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), ('books', 'collections', 'categories', 'recommended_books'))
        data = []
        for elem in response_data.values():
            for e in elem:
                if e.get('name'):
                    data.append(e.get('name'))
                else:
                    data.append(e.get('title'))
        for result in data:
            assert 'Покорители' in result

    def test_get_search_popular(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_token(client)
        response = client.get(
            self.get_url(f'/search/popular'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data[0].keys(), ('language', 'query', 'count', 'index', 'is_published',
                                                   'is_autocomplete', 'id'))

    def test_get_search_popular_with_search(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_token(client)
        response = client.get(
            self.get_url(f'/search/popular'),
            headers=self.get_authorization_header(access_token),
            params={'q': 'Скачки'}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data[0].keys(), ('language', 'query', 'count', 'index', 'is_published',
                                                   'is_autocomplete', 'id'))
        for elem in response_data:
            assert elem.get('query') == 'Скачки'
