import enum


class TokenType(str, enum.Enum):
	ACCESS = 'ACCESS'
	REFRESH = 'REFRESH'
