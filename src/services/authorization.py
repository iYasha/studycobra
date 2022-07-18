import enums
import models
import schemas
from core import security


class AuthorizationService:

    @classmethod
    async def create_session(
            cls,
            user: models.User,
            platform: enums.PlatformType,
            tracking_params: schemas.TrackingSchemaMixin
    ) -> schemas.SessionOut:
        user_info = schemas.UserBase.from_orm(user)
        expires_in = security.get_token_expires()
        session = await models.Session.create(
            user=user,
            platform=platform,
            refresh_token=security.create_refresh_token(user=user_info, user_id=user.uuid),
            **tracking_params.dict()
        )
        session.access_token = security.create_access_token(
            user=user_info,
            user_id=user.uuid,
            session_id=session.uuid,
            expires_in=expires_in
        )
        await session.save()
        return schemas.SessionOut(
            access_token=session.access_token,
            refresh_token=session.refresh_token,
            expires_in=round(expires_in.timestamp()),
        )

