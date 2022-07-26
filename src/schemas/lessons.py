from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import Field

from schemas.base import UUIDSchemaMixin, QuerySetMixin, BaseSchema
from schemas.files import File
from schemas.groups import GroupTeacher


class LessonBase(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    start_at: datetime
    end_at: datetime

    class Config:
        validate_assignment = True
        use_enum_values = True
        orm_mode = True


class Lesson(UUIDSchemaMixin, QuerySetMixin, LessonBase):
    pass


class LessonDetail(Lesson):
    teachers: List[GroupTeacher]
    additional_files: List[File]


class LessonCreate(LessonBase):
    teachers: List[UUID] = Field(
        default_factory=list,
        description='Id\'s of GroupTeacher instance that will be assigned to this lesson'
    )
    additional_files: List[UUID] = Field(default_factory=list, description='Id\'s of File instance')


class LessonPartlyUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    additional_files: List[UUID] = Field(default_factory=list, description='Id\'s of File instance')
