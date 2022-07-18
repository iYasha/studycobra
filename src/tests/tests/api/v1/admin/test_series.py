from fastapi.testclient import TestClient
from starlette import status

import crud
from logger.in_requests.application import DefaultFastAPI
from tests.api.v1.common import TestBase


class TestSeries(TestBase):
    """Тесты для проверки работоспособности АПИ серий"""

    series_id = 'eb97c6e9-6fd1-4765-aa84-efeb193836de'

    def test_create_series(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url('/series/'),
            json={
                'language': 'fe',
                'name': 'series name',
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), ('language', 'name', 'created_at', 'updated_at', 'id'))

    def test_get_series_with_search(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/series/'),
            headers=self.get_authorization_header(access_token),
            params={'q': 'Главная серия'}
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(series.get('language') for series in response_data.get('results')) == {'ru'}
        assert response_data.get('results')[0].get('name') == 'Главная серия'

    def test_get_series(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/series/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(collection.get('language') for collection in response_data.get('results')) == {'ru'}
        self.assert_keys(response_data.get('results')[0].keys(), ('language', 'name', 'created_at', 'updated_at', 'id', 'book_count'))

    def test_get_series_dropdown(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/series/dropdown/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data[0].keys(), ('name', 'id'))

    def test_get_one_series(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url(f'/series/{self.series_id}'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), ('language', 'name', 'created_at', 'updated_at', 'id'))

    def test_update_series(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.put(
            self.get_admin_url(f'/series/{self.series_id}'),
            json={
                "name": "new name"
            },
            headers=self.get_authorization_header(access_token),
        )
        get_series = self.get_async_result(crud.SeriesCRUD.get_one(id=self.series_id))
        assert get_series.name == "new name"
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_series(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.delete(
            self.get_admin_url(f'/series/{self.series_id}'),
            headers=self.get_authorization_header(access_token),
        )
        get_series = self.get_async_result(crud.SeriesCRUD.get_one(id=self.series_id))
        assert get_series is None
        assert response.status_code == status.HTTP_204_NO_CONTENT
