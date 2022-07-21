import enums
from schemas import UUIDSchemaMixin, AuditSchemaMixin, BaseSchema, QuerySetMixin


class CreateFile(BaseSchema):
	name: str
	content_type: enums.FileType
	size: float


class File(UUIDSchemaMixin, QuerySetMixin, AuditSchemaMixin, CreateFile):
	pass

