from typing import Optional
import sqlalchemy as sa

from core.database import database
from crud.base import BaseCRUD
import schemas
import models


class SessionCRUD(BaseCRUD):
    _model = models.Session
    _model_schema = schemas.SessionInDBBase

    @classmethod
    async def get_by_token(
            cls,
            access_token: str,
    ) -> Optional[schemas.SessionInDBBase]:
        query = cls.get_base_query()
        query = query.where(sa.and_(cls._model.access_token == access_token))
        return cls._get_parsed_object(await database.fetch_one(query))

    @classmethod
    async def get_by_tokens(
            cls,
            access_token: str,
            refresh_token: str,
    ) -> Optional[schemas.SessionInDBBase]:
        query = cls.get_base_query()
        query = query.where(sa.and_(cls._model.access_token == access_token, cls._model.refresh_token == refresh_token))
        return cls._get_parsed_object(await database.fetch_one(query))

