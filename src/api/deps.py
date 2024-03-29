from fastapi import Request, HTTPException, status, Depends

import models
from core.security import decode_jwt_token, oauth2_scheme
from schemas import AccessToken, TrackingSchemaMixin


async def get_current_user(token: str = Depends(oauth2_scheme)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    payload: AccessToken = decode_jwt_token(token, AccessToken)
    user = await models.User.get(uuid=payload.sub)
    if not user:
        raise credentials_exception
    return user


async def get_access_token(token: str = Depends(oauth2_scheme)) -> AccessToken:
    payload: AccessToken = decode_jwt_token(token, AccessToken)
    return payload


async def get_tracking_data(
    request: Request
) -> TrackingSchemaMixin:
    return TrackingSchemaMixin(
        ip_address=request.client.host,
        user_agent=request.headers.get('User-Agent')
    )
