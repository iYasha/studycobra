from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, validator
from tortoise import fields

import enums
from schemas.base import TrackingSchemaMixin, AuditSchemaMixin, UUIDSchemaMixin, QuerySetMixin, BaseSchema
from schemas.courses import Course
from schemas.users import User


class GroupBase(BaseSchema):
    teachers: List[UUID]
    students: List[UUID]
    start_at: datetime
    is_archived: bool = False

    class Config:
        validate_assignment = True
        use_enum_values = True
        orm_mode = True


class GroupTeacher(UUIDSchemaMixin, QuerySetMixin, BaseSchema):
    role: enums.TeacherRole
    user: User

    class Config:
        orm_mode = True


class GroupStudent(UUIDSchemaMixin, QuerySetMixin, BaseSchema):
    is_archived: bool
    user: User

    class Config:
        orm_mode = True


class Group(UUIDSchemaMixin, AuditSchemaMixin, QuerySetMixin, GroupBase):
    course: Course
    creator_id: UUID
    teachers: List[GroupTeacher]


class GroupDetail(Group):
    students: List[GroupStudent]


class GroupCreate(GroupBase):
    course_id: UUID


class GroupUpdate(BaseSchema):
    start_at: datetime
    is_archived: bool = False
