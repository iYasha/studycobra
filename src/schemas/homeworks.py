from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, validator, Field

import enums
from schemas.base import TrackingSchemaMixin, AuditSchemaMixin, UUIDSchemaMixin, QuerySetMixin, BaseSchema
from schemas.groups import GroupTeacher
from schemas.files import File


class HomeworkBase(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    time_terms: datetime
    retakes_count: int
    difficulty_level: enums.DifficultyLevel
    overdue_pass: bool = False

    class Config:
        validate_assignment = True
        use_enum_values = True
        orm_mode = True


class Homework(UUIDSchemaMixin, QuerySetMixin, HomeworkBase):
    author: Optional[GroupTeacher] = None
    additional_files: List[File] = Field(default_factory=list, description='Id\'s of File instance')


class HomeworkCreate(HomeworkBase):
    author_id: Optional[UUID] = Field(default=None, description='Id of GroupTeacher instance that will be check this homework')
    additional_files: List[UUID] = Field(default_factory=list, description='Id\'s of File instance')
