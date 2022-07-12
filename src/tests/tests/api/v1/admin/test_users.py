import json

from fastapi.testclient import TestClient
from starlette import status

import crud
from logger.in_requests.application import DefaultFastAPI
from tests.api.v1.common import TestBase


class TestUsers(TestBase):
    """Тесты для проверки работоспособности АПИ администраторов"""

    user_id = '5d8ef459-e940-4ab3-b50d-5f01e527ef48'
    moderator_id = '03524d9f-ea5b-4398-8180-5532a5dda74e'
    admin_id = 'fde12fa7-d37d-497f-aee2-275f8c245982'

    def test_users_cant_see_administrators(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        urls_list_get = ['/users/', f'/users/{self.user_id}', '/users/me']
        urls_list_put = [f'/users/{self.user_id}', f'/users/me/', f'/users/{self.user_id}/email/', f'/users/me/email/',
                         f'/users/{self.user_id}/password/', f'/users/me/password/']
        response = client.post(
            self.get_admin_url('/users/'),
        )
        for url in urls_list_get:
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
            response = client.get(
                self.get_admin_url(url),
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        for url in urls_list_put:
            response = client.put(
                self.get_admin_url(url),
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
        response = client.delete(
            self.get_admin_url(f'/users/{self.user_id}')
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_moderators_cant_crud_administrators(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_moderator_token(client)
        urls_list_put = [f'/users/{self.user_id}', f'/users/{self.user_id}/email/', f'/users/{self.user_id}/password/']
        response = client.post(
            self.get_admin_url('/users/'),
            headers=self.get_authorization_header(access_token),
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        for url in urls_list_put:
            response = client.put(
                self.get_admin_url(url),
                headers=self.get_authorization_header(access_token),
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
        response = client.delete(
            self.get_admin_url(f'/users/{self.user_id}'),
            headers=self.get_authorization_header(access_token),
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_administrators(
            self,
            app: DefaultFastAPI,
            client: TestClient
    ) -> None:
        tokens = [self.get_access_moderator_token(client), self.get_access_admin_token(client)]
        for access_token in tokens:
            response = client.get(
                self.get_admin_url('/users/'),
                headers=self.get_authorization_header(access_token),
            )
            response_data = response.json()
            assert response.status_code == status.HTTP_200_OK
            self.assert_keys(response_data[0].keys(), ('created_at', 'updated_at', 'id', 'name', 'email', 'surname',
                                                       'user_status', 'last_entrance', 'index',
                                                       ))

    def test_get_administrator(
            self,
            app: DefaultFastAPI,
            client: TestClient
    ) -> None:
        tokens = [self.get_access_moderator_token(client), self.get_access_admin_token(client)]
        for access_token in tokens:
            response = client.get(
                self.get_admin_url(f'/users/{self.user_id}'),
                headers=self.get_authorization_header(access_token),
            )
            response_data = response.json()
            assert response.status_code == status.HTTP_200_OK
            self.assert_keys(response_data.keys(), ('created_at', 'updated_at', 'id', 'name', 'email', 'surname',
                                                    'user_status', 'last_entrance', 'index',
                                                    ))

    def test_get_me(
            self,
            app: DefaultFastAPI,
            client: TestClient
    ) -> None:
        tokens = [self.get_access_moderator_token(client), self.get_access_admin_token(client)]
        for access_token in tokens:
            response = client.get(
                self.get_admin_url(f'/users/me'),
                headers=self.get_authorization_header(access_token),
            )
            response_data = response.json()
            assert response.status_code == status.HTTP_200_OK
            self.assert_keys(response_data.keys(), ('name', 'email'))

    def test_update_administrator_self(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:

        admin_data = {
            self.get_access_moderator_token(client): self.moderator_id,
            self.get_access_admin_token(client): self.admin_id
        }
        for access_token, admin_id in admin_data.items():
            request = {
                "name": "updated user",
                "surname": "surname updated user",
            }
            response = client.put(
                self.get_admin_url(f'/users/me/'),
                json=request,
                headers=self.get_authorization_header(access_token),
            )
            user = self.get_async_result(crud.UserCRUD.get_one(id=admin_id))
            data = json.loads(user.json())
            request.update({
                'created_at': data.get('created_at'),
                'updated_at': data.get('updated_at'),
                'id': data.get('id'),
                'email': data.get('email'),
                'user_status': data.get('user_status'),
                'last_entrance': data.get('last_entrance'),
                'index': data.get('index'),
            })
            assert request == data
            assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_update_administrator_email_self(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        admin_data = {
            self.get_access_moderator_token(client): self.moderator_id,
            self.get_access_admin_token(client): self.admin_id
        }
        for access_token, admin_id in admin_data.items():
            request = {
                "email": f"{admin_id}updated@example.com"
            }
            response = client.put(
                self.get_admin_url(f'/users/me/email/'),
                json=request,
                headers=self.get_authorization_header(access_token),
            )
            user = self.get_async_result(crud.UserCRUD.get_one(id=admin_id))
            data = json.loads(user.json())
            request.update({
                'created_at': data.get('created_at'),
                'updated_at': data.get('updated_at'),
                'id': data.get('id'),
                'name': data.get('name'),
                'surname': data.get('surname'),
                'user_status': data.get('user_status'),
                'last_entrance': data.get('last_entrance'),
                'index': data.get('index')
            })
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert request == data

    def test_update_administrator_password_self(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        admin_data = {
            self.get_access_moderator_token(client): self.moderator_id,
            self.get_access_admin_token(client): self.admin_id
        }
        for access_token, admin_id in admin_data.items():
            new_pass = "Hld92dsl32l"
            old_password = self.get_async_result(crud.UserCRUD.get_hashed_password(admin_id))
            wrong_response = client.put(
                self.get_admin_url(f'/users/me/password'),
                json={
                    "password": new_pass,
                    "repeat_password": new_pass,
                    "old_password": 'string' + 'wrong'
                },
                headers=self.get_authorization_header(access_token),
            )
            assert wrong_response.status_code == status.HTTP_400_BAD_REQUEST
            right_response = client.put(
                self.get_admin_url(f'/users/me/password'),
                json={
                    "password": new_pass,
                    "repeat_password": new_pass,
                    "old_password": 'string'
                },
                headers=self.get_authorization_header(access_token),
            )
            new_password = self.get_async_result(crud.UserCRUD.get_hashed_password(admin_id))
            assert old_password != new_password
            assert right_response.status_code == status.HTTP_204_NO_CONTENT

    def test_create_administrator(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        request = {
            "name": "new_user",
            "email": "new_user@example.com",
            "surname": "string",
            "user_status": "admin"
        }
        response = client.post(
            self.get_admin_url('/users/'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(response_data.keys(), ('created_at', 'updated_at', 'id', 'name', 'email', 'surname',
                                                'user_status', 'last_entrance', 'index',
                                                ))
        users = self.get_async_result(crud.UserCRUD.get_all_administrators())
        self.assert_keys([user.index for user in users if user.index != None],
                         list(range(1, len(users) + 1)))

        response = client.post(
            self.get_admin_url('/users/'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_administrator(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        request = {
            "name": "updated user",
            "surname": "surname updated user",
            "user_status": "admin"
        }
        response = client.put(
            self.get_admin_url(f'/users/{self.user_id}'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        user = self.get_async_result(crud.UserCRUD.get_one(id=self.user_id))
        data = json.loads(user.json())

        request.update({
            'created_at': data.get('created_at'),
            'updated_at': data.get('updated_at'),
            'id': data.get('id'),
            'email': data.get('email'),
            'last_entrance': data.get('last_entrance'),
            'index': data.get('index'),
        })
        assert request == data
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_update_administrator_email(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        request = {
            "email": "updated@example.com"
        }
        response = client.put(
            self.get_admin_url(f'/users/{self.user_id}/email/'),
            json=request,
            headers=self.get_authorization_header(access_token),
        )
        user = self.get_async_result(crud.UserCRUD.get_one(id=self.user_id))
        data = json.loads(user.json())
        request.update({
            'created_at': data.get('created_at'),
            'updated_at': data.get('updated_at'),
            'id': data.get('id'),
            'name': data.get('name'),
            'surname': data.get('surname'),
            'user_status': data.get('user_status'),
            'last_entrance': data.get('last_entrance'),
            'index': data.get('index')
        })
        assert request == data
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_update_administrator_password(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)

        new_pass = "Hld92dsl32l"
        old_password = self.get_async_result(crud.UserCRUD.get_hashed_password(self.user_id))
        response = client.put(
            self.get_admin_url(f'/users/{self.user_id}/password/'),
            json={
                "password": new_pass,
                "repeat_password": new_pass
            },
            headers=self.get_authorization_header(access_token),
        )
        new_password = self.get_async_result(crud.UserCRUD.get_hashed_password(self.user_id))
        assert old_password != new_password
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_administrator(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ) -> None:
        access_token = self.get_access_admin_token(client)
        response = client.delete(
            self.get_admin_url(f'/users/{self.user_id}'),
            headers=self.get_authorization_header(access_token),
        )
        user = self.get_async_result(crud.UserCRUD.get_one(id=self.user_id))
        assert user is None
        assert response.status_code == status.HTTP_204_NO_CONTENT
        users = self.get_async_result(crud.UserCRUD.get_all_administrators())
        self.assert_keys([user.index for user in users if user.index != None],
                         list(range(1, len(users) + 1)))
