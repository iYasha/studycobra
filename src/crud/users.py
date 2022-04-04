import datetime
from typing import Dict
from typing import List
from typing import Optional
from uuid import UUID

import sqlalchemy as sa
from core.database import database
from crud.base import BaseCRUD
from crud.base import BasePaginator
from pydantic import parse_obj_as

from core import security
import schemas
import models


class UserCRUD(BaseCRUD):
    _model = models.User
    _model_schema = schemas.User

    @classmethod
    async def get_by_email(
            cls,
            email: str,
    ) -> Optional[schemas.UserInDB]:
        query = cls.get_base_query()
        where = sa.and_(cls._model.email == email)
        query = query.where(where)
        result = await database.fetch_one(query)
        if result is None:
            return None
        return schemas.UserInDB.parse_obj(result)


