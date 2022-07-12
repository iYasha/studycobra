import time
from uuid import UUID

from fastapi.testclient import TestClient
from starlette import status

import crud
import enums
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
            self.get_url('/user/me'),
            headers=self.get_authorization_header(access_token)
        )
        return response

    def test_registration(
        self,
        app: DefaultFastAPI,
        client: TestClient,
    ) -> None:
        response = client.post(
            self.get_url('/oauth/register'),
            json={
                'name': 'Ivan',
                'email': 'test@gmail.com',
                'password': '12345678',
                'platform': 'IOS',
            }
        )
        resp_data = response.json()
        assert response.status_code == status.HTTP_200_OK

        user = self.get_async_result(crud.UserCRUD.get_by_email(email='test@gmail.com', user_types=enums.UserStatus.user_status()))
        assert isinstance(user, schemas.UserInDB)
        assert user.name == 'Ivan'
        assert user.email == 'test@gmail.com'

        self.assert_keys(resp_data.keys(), ('access_token', 'refresh_token', 'token_type', 'expires_in'))
        self.check_session(resp_data, user.id)

    def test_login(
        self,
        app: DefaultFastAPI,
        client: TestClient,
        expected_user_create,
    ) -> None:
        # Create a user from dummy data
        db_user = self.get_async_result(crud.UserCRUD.create(schemas.UserInDB(**expected_user_create)))

        # Try to login
        response = client.post(
            self.get_url('/oauth/login'),
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
            self.get_url('/oauth/login'),
            json={
                'email': None,
                'password': 'string',
                'platform': 'IOS',
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_guest_login(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ):
        response = client.post(
            self.get_url('/oauth/register/guest'),
            json={
                'platform': 'IOS',
            }
        )

        assert response.status_code == status.HTTP_200_OK
        resp_data = response.json()
        self.assert_keys(resp_data.keys(), ('access_token', 'refresh_token', 'token_type', 'expires_in'))

    def test_apple_login(
            self,
            app: DefaultFastAPI,
            client: TestClient,
    ):
        response = client.post(
            self.get_url('/oauth/apple'),
            json={
                'name': 'John',
                'platform': 'IOS',
                'apple_token': 'eyJraWQiOiJXNldjT0tCIiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJodHRwczovL2FwcGxlaWQuYXBwbGUuY29tIiwiYXVkIjoiY29tLm1ldGFwcm9qZWN0LmRldi5sZWdpc3RhcHAiLCJleHAiOjE2NDg2NDY4MzIsImlhdCI6MTY0ODU2MDQzMiwic3ViIjoiMDAwMDE0LjM4MmNmZWUzNzlmZjQyMzg4NTk5ODE2OWE4OTVmMzcyLjEzMzIiLCJjX2hhc2giOiJsSHBRWmNuRTROdjFlQXc0Uks4SUlnIiwiZW1haWwiOiJjbmFwNTVxNHR4QHByaXZhdGVyZWxheS5hcHBsZWlkLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjoidHJ1ZSIsImlzX3ByaXZhdGVfZW1haWwiOiJ0cnVlIiwiYXV0aF90aW1lIjoxNjQ4NTYwNDMyLCJub25jZV9zdXBwb3J0ZWQiOnRydWUsInJlYWxfdXNlcl9zdGF0dXMiOjJ9.J1SlWAzJ9HfPx6mt44yFnRaaFB8aWzGJMq08D3-Izyc0ab-1kZaEI1esHmDpZ2Jv9n84tcWfHUxFFqxrHdg0LvGuJmLB_Pq04qar_GMV6OCgnPGyq9SUKEeq1ysF8LC69Qds3raKi6CM-6MS89zzPy4XmMBANwPllZ-difh3Sj6P7_5qvSBqNfURQSkXqX3YKMtVRErXDcYbcB_1fPdLXikAZvLHqb6N0Da3m51NUWDl8yQl8APrjHl1IPB-NPmuH6p21LnpY2W5GHCtNgWaHLnBPlyvDQvUYyXxhzVNcuZXTY-LBrPz6b1BZnBWxrbuLnqsTNdCFmdbLxjCMCZVkQ',
            }
        )

        assert response.status_code == status.HTTP_200_OK
        resp_data = response.json()
        self.assert_keys(resp_data.keys(), ('access_token', 'refresh_token', 'token_type', 'expires_in'))

    def test_refresh_token(
            self,
            app: DefaultFastAPI,
            client: TestClient,
            expected_user_create,
    ) -> None:
        # Create a user from dummy data
        db_user = self.get_async_result(crud.UserCRUD.create(schemas.UserInDB(**expected_user_create)))

        # Create session and get access_token
        response = client.post(
            self.get_url('/oauth/login'),
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
            self.get_url('/oauth/refresh-token'),
            json=refresh_data,
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        time.sleep(1)

        # Get new session and kill old
        response = client.post(
            self.get_url('/oauth/refresh-token'),
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
            expected_user_create,
    ) -> None:
        self.get_async_result(crud.UserCRUD.create(schemas.UserInDB(**expected_user_create)))

        # Create session and get access_token
        response = client.post(
            self.get_url('/oauth/login'),
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
            self.get_url('/oauth/logout'),
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
            expected_user_create,
    ) -> None:
        self.get_async_result(crud.UserCRUD.create(schemas.UserInDB(**expected_user_create)))

        # Create session and get access_token
        response = client.post(
            self.get_url('/oauth/login'),
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
            self.get_url('/oauth/forgot-password'),
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
            self.get_url('/oauth/password-reset'),
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
            self.get_url('/oauth/login'),
            json={
                'email': 'john@gmail.com',
                'password': 'string',
                'platform': 'IOS',
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Try to login with new password
        response = client.post(
            self.get_url('/oauth/login'),
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
            expected_user_create,
    ) -> None:
        self.get_async_result(crud.UserCRUD.create(schemas.UserInDB(**expected_user_create)))

        for i in range(3):
            response = client.post(
                self.get_url('/oauth/forgot-password'),
                json={
                    'email': 'john@gmail.com',
                    'platform': 'IOS',
                }
            )
            assert response.status_code == status.HTTP_202_ACCEPTED
            time.sleep(1)
        response = client.post(
            self.get_url('/oauth/forgot-password'),
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
            expected_user_create,
    ) -> None:
        response = client.post(
            self.get_url('/oauth/forgot-password'),
            json={
                'email': 'john1@example.com',
                'platform': 'IOS',
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_reset_password_guest_user(
            self,
            app: DefaultFastAPI,
            client: TestClient,
            expected_user_create,
    ) -> None:
        # Register guest user
        response = client.post(
            self.get_url('/oauth/register/guest'),
            json={
                'platform': 'IOS'
            }
        )
        resp_data = response.json()
        assert response.status_code == status.HTTP_200_OK

        me_response = self.try_get_me(app, client, resp_data['access_token'])
        assert me_response.status_code == status.HTTP_200_OK
        me = me_response.json()

        response = client.post(
            self.get_url('/oauth/forgot-password'),
            json={
                'email': me['email'],
                'platform': 'IOS',
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_authorized_user_update_password(
            self,
            app: DefaultFastAPI,
            client: TestClient,
            expected_user_create,
    ) -> None:

        email = 'test@gmail.com'
        old_password = '12345678'
        new_password = 'string'

        def register_user() -> str:
            nonlocal old_password, email
            response = client.post(
                self.get_url('/oauth/register'),
                json={
                    'name': 'Vasya',
                    'email': email,
                    'password': old_password,
                    'platform': 'IOS',
                }
            )
            assert response.status_code == status.HTTP_200_OK
            return response.json()['access_token']

        def login_with_old_password():
            nonlocal old_password, email
            response = client.post(
                self.get_url('/oauth/login'),
                json={
                    'email': email,
                    'password': old_password,
                    'platform': 'IOS',
                }
            )
            assert response.status_code == status.HTTP_400_BAD_REQUEST

        def login_with_new_password():
            nonlocal new_password, email
            response = client.post(
                self.get_url('/oauth/login'),
                json={
                    'email': email,
                    'password': new_password,
                    'platform': 'IOS',
                }
            )
            assert response.status_code == status.HTTP_200_OK

        def try_to_update_password(access_token: str) -> None:
            nonlocal old_password, new_password
            response = client.patch(
                self.get_url('/user/me'),
                json={
                    'old_password': old_password,
                    'password': new_password
                },
                headers=self.get_authorization_header(access_token)
            )
            assert response.status_code == status.HTTP_204_NO_CONTENT

        def fail_update_password(access_token: str) -> None:
            nonlocal new_password
            response = client.patch(
                self.get_url('/user/me'),
                json={
                    'password': new_password,
                },
                headers=self.get_authorization_header(access_token)
            )
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        token = register_user()
        fail_update_password(token)
        try_to_update_password(token)
        login_with_old_password()
        login_with_new_password()
