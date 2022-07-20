from datetime import datetime, timezone
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar
from uuid import UUID

from pydantic import BaseModel, validator
from pydantic.generics import GenericModel
from tortoise import fields

from core.config import settings

BaseModelType = TypeVar("BaseModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class BaseSchema(BaseModel):
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.strftime(settings.DEFAULT_DATETIME_FORMAT)
        }

    @validator('*', pre=True)
    def _iter_to_list(cls, v):
        if isinstance(v, fields.ReverseRelation) and isinstance(v.related_objects, list):
            return list(v)
        return v


class QuerySetMixin(BaseModel):

    @classmethod
    def from_queryset(cls, queryset: list) -> List[BaseModelType]:
        return [cls.from_orm(e) for e in queryset]


class UUIDSchemaMixin(BaseModel):
    uuid: UUID


class PaginatedSchema(GenericModel, Generic[BaseModelType]):
    count: int
    next: Optional[int]  # noqa: A003
    previous: Optional[int]
    results: List[BaseModelType]


class Pagination(BaseModel):
    page: int = 0
    page_size: int = 10


class ExpireSchemaMixin(BaseModel):
    start_at: datetime
    end_at: datetime

    @property
    def block_pass_time(self) -> int:
        utc_now = datetime.now(timezone.utc)
        return (self.end_at - utc_now).seconds


class SoftDeleteSchemaMixin(BaseModel):
    is_deleted: bool = False


class TrackingSchemaMixin(BaseModel):
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class AuditSchemaMixin(BaseModel):
    created_at: datetime
    updated_at: Optional[datetime] = None
