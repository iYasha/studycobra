from datetime import datetime
from typing import Optional, List
from uuid import UUID

import enums
from schemas.base import TrackingSchemaMixin, AuditSchemaMixin, UUIDSchemaMixin, BaseSchema
from schemas.users import User


class CourseBase(BaseSchema):
    name: str

    class Config:
        validate_assignment = True
        use_enum_values = True


class Course(UUIDSchemaMixin, AuditSchemaMixin, CourseBase):
    pass
