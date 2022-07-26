from datetime import datetime
from typing import Optional

import enums
from schemas.base import BaseSchema
from schemas.users import UserBase


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
