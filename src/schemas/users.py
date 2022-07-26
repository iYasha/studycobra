from typing import Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel, EmailStr, validator

import enums
from core.config import settings
from schemas import UUIDSchemaMixin, AuditSchemaMixin, BaseSchema


class AuthorizationBase(BaseSchema):
    password: str
    platform: enums.PlatformType


class SignUp(AuthorizationBase):
    platform: enums.PlatformType
    name: str
    email: Optional[EmailStr] = None


class LogIn(AuthorizationBase):
    email: Optional[EmailStr] = None


class UserBase(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    role: enums.UserRole
    avatar_id: Optional[UUID] = None
    avatar: Optional[str] = None

    @validator('avatar', pre=True)
    def assemble_avatar_full_path(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Optional[str]:
        if isinstance(v, str):
            return v

        avatar_id = values.get('avatar_id')
        if avatar_id is None:
            return None

        return settings.FULL_DOMAIN + settings.API_V1_STR + '/files/' + str(avatar_id)

    class Config:
        validate_assignment = True
        use_enum_values = True
        orm_mode = True


class UserInDB(UserBase):
    uuid: Optional[UUID] = None
    hashed_password: Optional[str] = None


class User(UUIDSchemaMixin, AuditSchemaMixin, UserBase):
    pass
