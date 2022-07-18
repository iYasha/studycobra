import datetime
import os
import time
import uuid
from argparse import Namespace
from contextlib import contextmanager
from datetime import timedelta
from types import SimpleNamespace
from typing import Callable
from typing import Generator
from typing import List
from typing import Optional
from typing import Union

import jwt
from alembic.config import Config
from pydantic import BaseModel
from sqlalchemy_utils import create_database
from sqlalchemy_utils import drop_database
from sqlalchemy_utils.functions import database_exists
from yarl import URL

from core.config import settings

SECRET_KEY = "some_secret"
JWT_ALGORITHM = "HS256"


def get_fake_uuid(*, to_str: bool = True, constant: bool = False) -> Union[uuid.UUID, str]:
    """Возвращает сгенерированный uuid для не существующих объектов

    Если передан `constant=True`, возвратит один и тот же uuid4
    """
    if constant:
        return "500cf41e-876e-457e-9aec-28f51998508c"
    result = uuid.uuid4()
    return str(result) if to_str else result


def _ordering(reverse: bool = False) -> Callable:
    return lambda x, y: (x >= y) if reverse else (x <= y)


def is_ordered(lst: list, key: Callable, *, reverse: bool = False) -> bool:
    """
    Проверяет, отсортирован ли список :lst по возрастанию.

    Если :reverse = True, по убыванию

    :key - по какому полю проверять:
        lambda x: x.id
    Example:
        lst = [1,2,3]

        is_ordered(lst, lambda x: x)
    """
    return all(_ordering(reverse)(key(lst[i]), key(item)) for i, item in enumerate(lst[1:]))


class AccessTokenData(BaseModel):
    exp: int
    email: str = "test@sbap.ru"
    sso_user_id: int = 1
    sid: str = "01234567890"
    given_name: str = "Test"
    family_name: str = "Testovich"
    groups: List[str] = []
    permissions: List[str] = []


def create_access_token(
    groups: List[str] = None,
    permissions: List[str] = None,
) -> str:
    if groups is None:
        groups = []
    if permissions is None:
        permissions = []

    token_exp = datetime.datetime.now() + timedelta(hours=1)

    access_token_data = AccessTokenData(
        exp=time.mktime(token_exp.timetuple()), groups=groups, permissions=permissions
    )
    return jwt.encode(
        payload=access_token_data.dict(),
        key=SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def create_expired_access_token(
    groups: List[str] = None,
    permissions: List[str] = None,
) -> str:
    if groups is None:
        groups = []
    if permissions is None:
        permissions = []

    token_exp = datetime.datetime.now() - timedelta(hours=1)

    access_token_data = AccessTokenData(
        exp=time.mktime(token_exp.timetuple()), groups=groups, permissions=permissions
    )
    return jwt.encode(
        payload=access_token_data.dict(),
        key=SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


@contextmanager
def tmp_database(**kwargs) -> Generator[str, None, None]:
    if kwargs.get("template"):
        db_url = URL(settings.DB_URI).path.replace("_template_", "_test_")
    else:
        db_url = URL(settings.DB_URI).path.replace("_test_", "_template_")

    tmp_db_url = str(URL(settings.DB_URI).with_path(db_url))

    if database_exists(tmp_db_url):
        drop_database(tmp_db_url)

    create_database(tmp_db_url, **kwargs)

    try:
        yield tmp_db_url
    finally:
        drop_database(tmp_db_url)


def make_alembic_config(
    cmd_opts: Union[Namespace, SimpleNamespace], base_path: str = settings.PROJECT_ROOT
) -> Config:
    # Replace path to alembic.ini file to absolute
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config)

    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts)

    # Replace path to alembic folder to absolute
    alembic_location = config.get_main_option("script_location")
    if not os.path.isabs(alembic_location):
        config.set_main_option("script_location", os.path.join(base_path, alembic_location))
    if cmd_opts.pg_url:
        config.set_main_option("sqlalchemy.url", cmd_opts.pg_url)

    return config


def alembic_config_from_url(pg_url: Optional[str] = None) -> Config:
    """
    Provides Python object, representing alembic.ini file.
    """
    cmd_options = SimpleNamespace(
        config="alembic.ini",
        name="alembic",
        pg_url=pg_url,
        raiseerr=False,
        x=None,
    )
    return make_alembic_config(cmd_options)
