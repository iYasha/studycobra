from typing import Any
from typing import List
from typing import Tuple

import pytest
from fastapi.routing import APIRoute
from sso_auth.utils import is_ignored_path
from main import app as fs_app
from starlette import convertors
from starlette import status
from starlette.testclient import TestClient
from tests.utils import create_access_token
from tests.utils import create_expired_access_token
from tests.utils import get_fake_uuid


def generate_param_by_convertor(param: convertors.Convertor) -> Any:
    if isinstance(param, convertors.UUIDConvertor):
        return get_fake_uuid(constant=True)
    if isinstance(param, convertors.StringConvertor):
        return "some_string"
    raise NotImplementedError("Неизвестный тип конвертора")


def all_routes() -> List[Tuple[str, str]]:
    routes: List[Tuple[str, str]] = []
    route: APIRoute
    for route in fs_app.routes:
        if is_ignored_path(route.path):
            continue

        if route.param_convertors:
            params = {
                param_name: generate_param_by_convertor(convertor)
                for param_name, convertor in route.param_convertors.items()
            }
            url = route.url_path_for(route.name, **params)
        else:
            url = route.url_path_for(route.name)
        method = list(route.methods)[0]
        routes.append((url, method))
    return routes


@pytest.mark.usefixtures("prepare_sso_settings")
@pytest.mark.parametrize("url, method", all_routes())
def test_has_permissions(client: TestClient, url: str, method: str) -> None:
    """
    Тест, который проверяет, что все ручки сервиса защищены пермишенами.
    """
    token = create_access_token()

    headers = {"Authorization": f"Bearer {token}"}
    res = client.request(
        method=method,
        url=url,
        headers=headers,
        json={},
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN, res.json()
    assert res.json()["error_message"] == "no permission to perform this action"


@pytest.mark.usefixtures("prepare_sso_settings")
@pytest.mark.parametrize("url, method", all_routes())
def test_expired_token(client: TestClient, url: str, method: str) -> None:
    """
    Тест, который проверяет, что все ручки сервиса защищены пермишенами.
    """
    token = create_expired_access_token()

    headers = {"Authorization": f"Bearer {token}"}
    res = client.request(
        method=method,
        url=url,
        headers=headers,
        json={},
    )

    assert res.status_code == status.HTTP_401_UNAUTHORIZED, res.json()
    assert res.json()["error_message"] == "expired token signature"


@pytest.mark.usefixtures("prepare_sso_settings")
@pytest.mark.parametrize("url, method", all_routes())
def test_invalid_token(client: TestClient, url: str, method: str) -> None:
    """
    Тест, который проверяет, что все ручки сервиса защищены пермишенами.
    """
    token = "some_broken_token"

    headers = {"Authorization": f"Bearer {token}"}
    res = client.request(
        method=method,
        url=url,
        headers=headers,
        json={},
    )

    assert res.status_code == status.HTTP_401_UNAUTHORIZED, res.json()
    assert res.json()["error_message"] == "invalid token"


@pytest.mark.usefixtures("prepare_sso_settings")
@pytest.mark.parametrize("url, method", all_routes())
def test_token_not_found(client: TestClient, url: str, method: str) -> None:
    """
    Тест, который проверяет, что все ручки сервиса защищены пермишенами.
    """
    res = client.request(
        method=method,
        url=url,
        headers={},
        json={},
    )

    assert res.status_code == status.HTTP_401_UNAUTHORIZED, res.json()
    assert res.json()["error_message"] == "token not found"
