from typing import Generator

import pytest
from _pytest.monkeypatch import MonkeyPatch
from alembic.command import upgrade as alembic_upgrade
from requests import Session as RequestSession
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from starlette.testclient import TestClient

from core.config import settings
from logger.in_requests.application import DefaultFastAPI
from sso_auth.config import SSOAuthConfig
from .common import TestGlobalSession
from .utils import alembic_config_from_url
from .utils import tmp_database

if not settings.TESTING:
    raise ValueError('Please, set TESTING=True in core/config.py to run tests')

pytest_plugins = [
    "tests.mocks.expected_results",
]


@pytest.fixture(scope="session")
def monkeypatch_session() -> MonkeyPatch:
    m = MonkeyPatch()
    yield m
    m.undo()


@pytest.fixture
def prepare_sso_settings(monkeypatch: MonkeyPatch) -> Generator[None, None, None]:
    monkeypatch.setattr(settings, "SSO_AUTH_JWT_VERIFY_SIGNATURE", True)
    monkeypatch.setattr(settings, "SSO_AUTH_VALIDATION_ENABLED", True)
    monkeypatch.setattr(settings, "SSO_AUTH_JWT_ALGORITHMS", ["HS256"])
    monkeypatch.setattr(settings, "SSO_AUTH_JWT_KEY", "some_secret")

    SSOAuthConfig.load_config(lambda: settings)
    yield
    monkeypatch.undo()
    SSOAuthConfig.load_config(lambda: settings)


@pytest.fixture(autouse=True)
def db_session(postgres_engine: Engine) -> Generator[None, None, None]:
    TestGlobalSession.configure(bind=postgres_engine)
    yield
    TestGlobalSession.remove()


@pytest.fixture()
def postgres_engine(migrated_postgres: str) -> Generator[Engine, None, None]:
    """
    SQLAlchemy engine, привязанный к мигрированной базе данных
    """
    engine = create_engine(migrated_postgres, echo=False, isolation_level="READ COMMITTED")
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture()
def migrated_postgres(monkeypatch_session: MonkeyPatch) -> Generator[str, None, None]:
    """
    Quickly creates clean migrated database using temporary database as base.
    """
    with tmp_database() as tmp_url:
        alembic_config = alembic_config_from_url(tmp_url)
        monkeypatch_session.setattr(settings, "DB_URI", tmp_url)
        alembic_upgrade(alembic_config, "head")
        yield tmp_url


@pytest.fixture
def client(app: DefaultFastAPI) -> Generator[RequestSession, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def app() -> DefaultFastAPI:
    from main import app as fastapi_app

    return fastapi_app
