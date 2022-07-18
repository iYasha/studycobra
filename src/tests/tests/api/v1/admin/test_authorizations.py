import time
from uuid import UUID

from fastapi.testclient import TestClient
from starlette import status

import crud
import schemas
from logger.in_requests.application import DefaultFastAPI
from tests.api.v1.common import TestBase


class TestOAuth(TestBase):

    def check_session(
            self,
            session_data: dict,
            user_id: UUID,
    ):
        session = self.get_async_result(crud.SessionCRUD.get_one(user_id=user_id))
        assert isinstance(session, schemas.SessionInDBBase)
        assert session.refresh_token == session_data['refresh_token']
        assert session.access_token == session_data['access_token']
        assert session_data['token_type'] == 'bearer'

    def try_get_me(self,
            app: DefaultFastAPI,
            client: TestClient,
            access_token: str
    ):
        response = client.get(
            self.get_admin_url('/users/me'),
            headers=self.get_authorization_header(access_token)
        )
        return response

    def test_login(
        self,
        app: DefaultFastAPI,
        client: TestClient,
        expected_admin_create,
    ) -> None:
        # Create a user from dummy data
        db_user = self.get_async_result(crud.UserCRUD.create(schemas.UserInDB(**expected_admin_create)))

        # Try to login
        response = client.post(
            self.get_admin_url('/oauth/login'),
            json={
                'email': 'john@gmail.com',
                'password': 'string',
                'platform': 'IOS',
            }
        )
        resp_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(resp_data.keys(), ('access_token', 'refresh_token', 'token_type', 'expires_in'))
        self.check_session(resp_data, db_user.id)

    def test_failed_login(
        self,
        app: DefaultFastAPI,
        client: TestClient,
    ) -> None:
        # Try to login
        response = client.post(
            self.get_admin_url('/oauth/login'),
            json={
                'email': None,
                'password': 'string',
                'platform': 'IOS',
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_refresh_token(
            self,
            app: DefaultFastAPI,
            client: TestClient,
            expected_admin_create,
    ) -> None:
        # Create a user from dummy data
        db_user = self.get_async_result(crud.UserCRUD.create(schemas.UserInDB(**expected_admin_create)))

        # Create session and get access_token
        response = client.post(
            self.get_admin_url('/oauth/login'),
            json={
                'email': 'john@gmail.com',
                'password': 'string',
                'platform': 'IOS',
            }
        )
        resp_data = response.json()
        old_access_token = resp_data['access_token']

        # Check for session is active
        me_response = self.try_get_me(app, client, old_access_token)
        me = me_response.json()
        self.assert_keys(me.keys(), ('name', 'email'))
        assert me_response.status_code == status.HTTP_200_OK

        refresh_data = {
            'access_token': old_access_token,
            'refresh_token': resp_data['refresh_token'],
        }

        # Try to refresh token without session
        response = client.post(
            self.get_admin_url('/oauth/refresh-token'),
            json=refresh_data,
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        time.sleep(1)

        # Get new session and kill old
        response = client.post(
            self.get_admin_url('/oauth/refresh-token'),
            json=refresh_data,
            headers=self.get_authorization_header(old_access_token)
        )
        resp_data = response.json()
        new_access_token = resp_data['access_token']

        assert response.status_code == status.HTTP_200_OK
        self.assert_keys(resp_data.keys(), ('access_token', 'refresh_token', 'token_type', 'expires_in'))

        # Failed request with old session
        me_response = self.try_get_me(app, client, old_access_token)
        assert me_response.status_code == status.HTTP_401_UNAUTHORIZED

        # Success request with new session
        me_response = self.try_get_me(app, client, new_access_token)
        assert me_response.status_code == status.HTTP_200_OK

    def test_logout(
            self,
            app: DefaultFastAPI,
            client: TestClient,
            expected_admin_create,
    ) -> None:
        self.get_async_result(crud.UserCRUD.create(schemas.UserInDB(**expected_admin_create)))

        # Create session and get access_token
        response = client.post(
            self.get_admin_url('/oauth/login'),
            json={
                'email': 'john@gmail.com',
                'password': 'string',
                'platform': 'IOS',
            }
        )
        resp_data = response.json()
        access_token = resp_data['access_token']

        # Check for session is active
        me_response = self.try_get_me(app, client, access_token)
        me = me_response.json()
        self.assert_keys(me.keys(), ('name', 'email'))
        assert me_response.status_code == status.HTTP_200_OK

        # Logout
        # Test logout request
        response = client.delete(
            self.get_admin_url('/oauth/logout'),
            headers=self.get_authorization_header(access_token)
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Check for session is not active
        me_response = self.try_get_me(app, client, access_token)
        assert me_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_reset_password(
            self,
            app: DefaultFastAPI,
            client: TestClient,
            expected_admin_create,
    ) -> None:
        self.get_async_result(crud.UserCRUD.create(schemas.UserInDB(**expected_admin_create)))

        # Create session and get access_token
        response = client.post(
            self.get_admin_url('/oauth/login'),
            json={
                'email': 'john@gmail.com',
                'password': 'string',
                'platform': 'IOS',
            }
        )
        resp_data = response.json()
        access_token = resp_data['access_token']
        assert response.status_code == status.HTTP_200_OK

        response = client.post(
            self.get_admin_url('/oauth/forgot-password'),
            json={
                'email': 'john@gmail.com',
                'platform': 'IOS',
            }
        )
        assert response.status_code == status.HTTP_202_ACCEPTED

        reset_item = self.get_async_result(crud.RestorePasswordCRUD.get_one(
            email='john@gmail.com',
            platform='IOS',
            status='pending'
        ))
        assert reset_item is not None

        # Test restore password request
        response = client.post(
            self.get_admin_url('/oauth/password-reset'),
            json={
                'email': 'john@gmail.com',
                'new_password': 'string1',
                'token': reset_item.verify_token,
            }
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Check for session isn't active
        me_response = self.try_get_me(app, client, access_token)
        assert me_response.status_code == status.HTTP_401_UNAUTHORIZED

        # Try to login with old password
        response = client.post(
            self.get_admin_url('/oauth/login'),
            json={
                'email': 'john@gmail.com',
                'password': 'string',
                'platform': 'IOS',
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Try to login with new password
        response = client.post(
            self.get_admin_url('/oauth/login'),
            json={
                'email': 'john@gmail.com',
                'password': 'string1',
                'platform': 'IOS',
            }
        )
        assert response.status_code == status.HTTP_200_OK

    def test_reset_password_try_max_attempts(
            self,
            app: DefaultFastAPI,
            client: TestClient,
            expected_admin_create,
    ) -> None:
        self.get_async_result(crud.UserCRUD.create(schemas.UserInDB(**expected_admin_create)))

        for i in range(3):
            response = client.post(
                self.get_admin_url('/oauth/forgot-password'),
                json={
                    'email': 'john@gmail.com',
                    'platform': 'IOS',
                }
            )
            assert response.status_code == status.HTTP_202_ACCEPTED
            time.sleep(1)
        response = client.post(
            self.get_admin_url('/oauth/forgot-password'),
            json={
                'email': 'john@gmail.com',
                'platform': 'IOS',
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_reset_password_unknown_user(
            self,
            app: DefaultFastAPI,
            client: TestClient,
            expected_admin_create,
    ) -> None:
        response = client.post(
            self.get_admin_url('/oauth/forgot-password'),
            json={
                'email': 'john1@example.com',
                'platform': 'IOS',
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
