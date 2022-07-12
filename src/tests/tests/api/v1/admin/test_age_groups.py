from fastapi.testclient import TestClient
from starlette import status

import crud
from logger.in_requests.application import DefaultFastAPI
from tests.api.v1.common import TestBase


class TestAgeGroups(TestBase):
    """Тесты для проверки работоспособности АПИ возрастных групп"""

    age_group_id = 'df479161-6d4b-47ef-a99d-ce69610d8983'

    def test_create_age_group(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.post(
            self.get_admin_url('/age-groups/'),
            json={
                'language': 'fe',
                'from_age': 4,
                'to_age': 8,
                'is_active': True
            },
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK

        self.assert_keys(response_data.keys(), ('language', 'from_age', 'to_age', 'is_active', 'created_at',
                                                'updated_at', 'id'))

    def test_get_age_groups_is_active_true(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/age-groups/'),
            headers=self.get_authorization_header(access_token),
            params={
                'is_active': True
            }
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(age_group.get('language') for age_group in response_data) == {'ru'}
        assert all([age_group.get('is_active') for age_group in response_data])

    def test_get_age_groups_is_active_false(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/age-groups/'),
            headers=self.get_authorization_header(access_token),
            params={
                'is_active': False
            }
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(age_group.get('language') for age_group in response_data) == {'ru'}
        assert not all([age_group.get('is_active') for age_group in response_data])

    def test_get_age_groups(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/age-groups/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert set(age_group.get('language') for age_group in response_data) == {'ru'}
        self.assert_keys(response_data[0].keys(), ('language', 'from_age', 'to_age', 'is_active', 'created_at',
                                                   'updated_at', 'id', 'book_count'))

    def test_get_age_groups_dropdown(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url('/age-groups/dropdown/'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data[0].keys(), ('from_age', 'to_age', 'id'))

    def test_get_one_age_group(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.get(
            self.get_admin_url(f'/age-groups/{self.age_group_id}'),
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), ('language', 'from_age', 'to_age', 'is_active', 'created_at',
                                                'updated_at', 'id'))

    def test_update_age_group(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.put(
            self.get_admin_url(f'/age-groups/{self.age_group_id}'),
            json={
                'from_age': 1,
                'to_age': 7,
                'is_active': True,
                'language': 'de',
            },
            headers=self.get_authorization_header(access_token),
        )
        get_age_group = self.get_async_result(crud.AgeGroupCRUD.get_one(id=self.age_group_id))
        assert get_age_group.from_age == 1
        assert get_age_group.to_age == 7
        assert get_age_group.is_active
        assert get_age_group.language == 'de'
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_age_group(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.delete(
            self.get_admin_url(f'/age-groups/{self.age_group_id}'),
            headers=self.get_authorization_header(access_token),
        )
        get_age_group = self.get_async_result(crud.AgeGroupCRUD.get_one(id=self.age_group_id))
        assert get_age_group is None
        assert response.status_code == status.HTTP_204_NO_CONTENT
