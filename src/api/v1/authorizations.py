from datetime import timedelta
from typing import List, Union
from uuid import UUID

from starlette.responses import Response
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

router = APIRouter()


async def create_session(user: Union[schemas.User, schemas.UserInDB], platform: enums.PlatformType, tracking_params: schemas.TrackingSchemaMixin) -> schemas.SessionOut:
    user_info = schemas.UserInToken.parse_obj(user)
    access_token_expires_in = security.get_token_expires(
        timedelta(
            minutes=settings.SSO_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )
    session = await models.Session.create(user_id=)
    session = await crud.SessionCRUD.create(
        schemas.SessionCreate(
            user_id=user.id,
            platform=platform,
            access_token=security.create_access_token(
                user=user_info, user_id=user.id, expires_in=access_token_expires_in
            ),
            refresh_token=security.create_refresh_token(user=user_info, user_id=user.id),
            **tracking_params.dict(),
        )
    )

    return schemas.SessionOut(
        **session.dict(),
        expires_in=round(access_token_expires_in.timestamp()),
    )


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
    session = await create_session(user, sign_up.platform, tracking_params)
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
async def login(
        *,
        tracking_params: schemas.TrackingSchemaMixin = Depends(deps.get_tracking_data),
        sign_in: schemas.LogIn
) -> schemas.SessionOut:
    """Вход с помощью почты и пароля или Apple Token"""
    user_not_found_or_password_incorrect = ValidationError(
                field_errors=[
                    FieldError(field='email', message='Пользователь с таким email не существует'),
                    FieldError(field='password', message='Пароль неправильный')
                ]
    )
    transaction = await database.transaction()

    try:
        user = await crud.UserCRUD.get_by_email(sign_in.email)
        if not user:
            raise user_not_found_or_password_incorrect
        is_verified = security.verify_password(sign_in.password, user.hashed_password)
        if not is_verified:
            raise user_not_found_or_password_incorrect

        session = await create_session(user, sign_in.platform, tracking_params)
        transaction.commit()
        return session
    except Exception as e:
        await transaction.rollback()
        raise e


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
async def refresh_access_token(
    *,
    tracking_params: schemas.TrackingSchemaMixin = Depends(deps.get_tracking_data),
    access_token: schemas.AccessToken = Depends(deps.get_access_token_without_verify),
    refresh_token: schemas.RefreshAccessToken,
) -> schemas.SessionOut:
    transaction = await database.transaction()
    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        old_session = await crud.SessionCRUD.get_by_tokens(
            access_token=access_token.token, refresh_token=refresh_token.refresh_token
        )
        if old_session is None:
            raise credentials_exception
        user = await crud.UserCRUD.get_by_id(old_session.user_id)
        session = await create_session(user, old_session.platform, tracking_params)
        await crud.SessionCRUD.destroy(obj_id=old_session.id)
        transaction.commit()
        return session
    except Exception as e:
        await transaction.rollback()
        raise e


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
    await crud.SessionCRUD.destroy(obj_id=access_token.session_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)




