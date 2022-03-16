import datetime
import time
import uuid
from datetime import timedelta
from typing import List
from typing import Union

import jwt
from pydantic import BaseModel

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
