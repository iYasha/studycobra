import enums
from schemas import UUIDSchemaMixin, AuditSchemaMixin, BaseSchema


class CreateFile(BaseSchema):
	name: str
	content_type: enums.FileType
	size: float


class File(UUIDSchemaMixin, AuditSchemaMixin, CreateFile):
	pass

