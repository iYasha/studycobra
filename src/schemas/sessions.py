from typing import Optional
from uuid import UUID

from pydantic import BaseModel

import enums
from schemas.base import TrackingSchemaMixin, AuditSchemaMixin
from schemas.users import User


class SessionBase(TrackingSchemaMixin, BaseModel):
	user_id: UUID
	access_token: Optional[str] = None
	refresh_token: Optional[str] = None
	platform: enums.PlatformType = enums.PlatformType.WEB

	class Config:
		validate_assignment = True
		use_enum_values = True


class SessionInDBBase(SessionBase):
	id: Optional[UUID] = None

	class Config(SessionBase.Config):
		orm_mode = True


class SessionCreate(SessionBase):
	pass


class SessionUpdate(SessionBase):
	access_token: str
	refresh_token: str


class Session(AuditSchemaMixin, SessionInDBBase):
	pass


class SessionWithUser(SessionInDBBase):
	user: User


class SessionOut(BaseModel):
	access_token: str
	refresh_token: str
	token_type: str = 'bearer'
	expires_in: int
