from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

import enums
from schemas.users import UserBase
from schemas.base import BaseSchema


class BaseToken(BaseSchema):
	iat: datetime
	exp: datetime
	sub: str
	token_type: enums.TokenType

	class Config:
		validate_assignment = True
		use_enum_values = True


class AccessToken(BaseToken):
	token_type: enums.TokenType = enums.TokenType.ACCESS
	token: Optional[str] = None
	user: UserBase
	session_id: Optional[str] = None


class RefreshToken(BaseToken):
	token_type: enums.TokenType = enums.TokenType.REFRESH
	token: Optional[str] = None
