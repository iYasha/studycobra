from typing import Generator

import pytest
from fastapi.testclient import TestClient
from logger.in_requests.application import DefaultFastAPI
from requests import Session as RequestSession


@pytest.fixture
def client(app: DefaultFastAPI) -> Generator[RequestSession, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def app() -> DefaultFastAPI:
    from main import app as fastapi_app

    return fastapi_app
