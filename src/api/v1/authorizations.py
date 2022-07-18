from datetime import timedelta
from typing import List, Union
from uuid import UUID

from starlette.responses import Response
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import atomic

import enums
from core import security
from core.config import settings
from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi import status

from exceptions import ValidationError
from exceptions.schemas import ExceptionModel
import schemas
import models
from sdk.exceptions import FieldError
from api import deps
import services

router = APIRouter()


@router.post(
    '/register',
    response_model=schemas.SessionOut,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Validation Error',
            'model': ExceptionModel,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'Server Error',
            'model': ExceptionModel,
        },
    },
)
@atomic()
async def register(
        *,
        tracking_params: schemas.TrackingSchemaMixin = Depends(deps.get_tracking_data),
        sign_up: schemas.SignUp
) -> schemas.SessionOut:
    """Регистрация с помощью почты и пароля"""

    is_user_exists = await models.User.exists(email=sign_up.email)
    if is_user_exists:
        raise ValidationError(
            field_errors=[FieldError(field='email', message='Пользователь с таким email уже существует')]
        )

    create_user = schemas.UserInDB(
        **sign_up.dict()
    )

    if sign_up.password is not None:
        create_user.hashed_password = security.get_password_hash(sign_up.password)

    user = await models.User.create(**create_user.dict(exclude_unset=True))
    session = await services.AuthorizationService.create_session(user, sign_up.platform, tracking_params)
    return session


@router.post(
    '/login',
    response_model=schemas.SessionOut,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Validation Error',
            'model': ExceptionModel,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'Server Error',
            'model': ExceptionModel,
        },
    },
)
@atomic()
async def login(
        *,
        tracking_params: schemas.TrackingSchemaMixin = Depends(deps.get_tracking_data),
        sign_in: schemas.LogIn
) -> schemas.SessionOut:
    """Вход с помощью почты и пароля"""

    user_not_found_or_password_incorrect = ValidationError(
                field_errors=[
                    FieldError(field='email', message='Пользователь с таким email не существует'),
                    FieldError(field='password', message='Пароль неправильный')
                ]
    )

    try:
        user = await models.User.get(email=sign_in.email)
    except DoesNotExist:
        raise user_not_found_or_password_incorrect

    is_verified = security.verify_password(sign_in.password, user.hashed_password)
    if not is_verified:
        raise user_not_found_or_password_incorrect

    session = await services.AuthorizationService.create_session(user, sign_in.platform, tracking_params)
    return session


@router.post(
    '/refresh-token',
    response_model=schemas.SessionOut,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'description': 'Token invalid or expired.',
            'model': ExceptionModel,
        },
    },
)
@atomic()
async def refresh_access_token(
    *,
    tracking_params: schemas.TrackingSchemaMixin = Depends(deps.get_tracking_data),
    access_token: schemas.AccessToken = Depends(deps.get_access_token),
    refresh_token: str = Body(..., embed=True),
) -> schemas.SessionOut:
    """Если приходит 401 ответ, то нужно попробовать обновить токен"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        old_session = await models.Session.get(
            access_token=access_token.token, refresh_token=refresh_token
        ).prefetch_related('user')
    except DoesNotExist:
        raise credentials_exception

    session = await services.AuthorizationService.create_session(old_session.user, old_session.platform, tracking_params)
    await models.Session.filter(uuid=old_session.uuid).delete()
    return session


@router.delete(
    '/logout',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_404_NOT_FOUND: {
            'description': 'Token invalid or expired.',
            'model': ExceptionModel,
        },
    },
)
async def logout(
    *,
    access_token: schemas.AccessToken = Depends(deps.get_access_token),
) -> Response:
    await models.Session.get(uuid=access_token.session_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)




