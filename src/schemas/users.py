from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel, EmailStr, validator, root_validator

import enums
from schemas import UUIDSchemaMixin, AuditSchemaMixin, BaseSchema
from core.config import settings


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

    class Config:
        validate_assignment = True
        use_enum_values = True
        orm_mode = True


class UserInDB(UserBase):
    uuid: Optional[UUID] = None
    hashed_password: Optional[str] = None


class User(UUIDSchemaMixin, AuditSchemaMixin, UserBase):
    pass
