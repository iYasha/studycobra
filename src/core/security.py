from datetime import timedelta, datetime
from typing import TypeVar, Type
from uuid import UUID

from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi import HTTPException
from passlib.context import CryptContext
import jwt
from pydantic import ValidationError
from starlette import status

from core.config import settings
import schemas
from sdk.exceptions import FieldError
from exceptions import ValidationError as ValidationErrorException

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl='login', tokenUrl='login')
PayloadSchema = TypeVar('PayloadSchema', bound=schemas.BaseToken)


def get_jwt_algorithm() -> str:
    if isinstance(settings.SSO_AUTH_JWT_ALGORITHMS, list):
        return next(iter(settings.SSO_AUTH_JWT_ALGORITHMS))
    return settings.SSO_AUTH_JWT_ALGORITHMS


def get_token_expires(expires_delta: timedelta = None) -> datetime:
    if expires_delta:
        return datetime.utcnow() + expires_delta
    return datetime.utcnow() + timedelta(
            minutes=settings.SSO_ACCESS_TOKEN_EXPIRE_MINUTES
        )


def create_jwt_token(
    body: schemas.BaseToken,
) -> str:
    encoded_jwt = jwt.encode(body.dict(), settings.SSO_AUTH_JWT_KEY, algorithm=get_jwt_algorithm())
    return encoded_jwt


def decode_jwt_token(token: str, payload_schema: Type[PayloadSchema], verify: bool = True) -> PayloadSchema:
    try:
        payload = jwt.decode(
            token, settings.SSO_AUTH_JWT_KEY, algorithms=[get_jwt_algorithm()], options={'verify_signature': verify}
        )
        payload.update({'token': token})
        return payload_schema(**payload)
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token invalid or expired.',
        )


def create_access_token(user: schemas.UserBase, user_id: UUID, session_id: UUID, expires_in: datetime = None):
    expires_delta = timedelta(
        minutes=settings.SSO_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    if expires_in:
        expires = expires_in
    else:
        expires = get_token_expires(expires_delta)
    body = schemas.AccessToken(
        iat=datetime.utcnow(),
        exp=expires,
        sub=str(user_id),
        user=user.dict(),
        session_id=str(session_id)
    )
    return create_jwt_token(body)


def create_refresh_token(user: schemas.UserBase, user_id: UUID):
    expires_delta = timedelta(
        minutes=settings.SSO_REFRESH_TOKEN_EXPIRE_MINUTES
    )
    body = schemas.RefreshToken(
        iat=datetime.utcnow(),
        exp=get_token_expires(expires_delta),
        sub=str(user_id),
        user=user.dict()
    )
    return create_jwt_token(body)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password + settings.SECRET_KEY, hashed_password)


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password + settings.SECRET_KEY)
