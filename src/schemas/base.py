from datetime import datetime, timezone
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar
from uuid import UUID

from pydantic import BaseModel
from pydantic.generics import GenericModel

BaseModelType = TypeVar("BaseModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class UUIDSchemaMixin(BaseModel):
    id: UUID


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
