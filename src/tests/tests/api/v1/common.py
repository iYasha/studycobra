import asyncio

from starlette.datastructures import URLPath

from core.config import settings


class TestBase:
    """ Базовый класс для тестов """

    @classmethod
    def get_url(cls, endpoint: str) -> URLPath:
        return URLPath(f"{settings.API_V1_STR}{endpoint}")

    @classmethod
    def get_admin_url(cls, endpoint: str) -> URLPath:
        return URLPath(f"{settings.API_ADMIN_V1_STR}{endpoint}")

    @classmethod
    def get_async_result(cls, method):
        return asyncio.get_event_loop().run_until_complete(method)

    @classmethod
    def get_authorization_header(cls, token: str, language: str = 'ru') -> dict:
        return {"Authorization": f"Bearer {token}", 'Accept-Language': language}

    @classmethod
    def get_access_token(cls, client, platform='IOS'):
        return client.post(
            cls.get_url('/oauth/register/guest'),
            json={
                'platform': platform
            }
        ).json()['access_token']

    @classmethod
    def get_access_moderator_token(cls, client, platform='IOS'):
        return client.post(
            cls.get_admin_url('/oauth/login'),
            json={
                "password": "string",
                "platform": platform,
                "email": "3example@gmail.com"
            }
        ).json()['access_token']

    @classmethod
    def get_access_admin_token(cls, client, platform='WEB'):
        return client.post(
            cls.get_admin_url('/oauth/login'),
            json={
                "password": "string",
                "platform": platform,
                "email": "1example@gmail.com"
            }
        ).json()['access_token']

    @classmethod
    def assert_keys(cls, a, b):
        assert tuple(sorted(list(a))) == tuple(sorted(list(b)))
