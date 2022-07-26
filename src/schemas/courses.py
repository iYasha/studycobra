from schemas.base import AuditSchemaMixin, UUIDSchemaMixin, BaseSchema


class CourseBase(BaseSchema):
    name: str

    class Config:
        validate_assignment = True
        use_enum_values = True


class Course(UUIDSchemaMixin, AuditSchemaMixin, CourseBase):
    pass
