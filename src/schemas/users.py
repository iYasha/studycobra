from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel, EmailStr, validator, root_validator

import enums
import schemas
from core.config import settings


class AuthorizationBase(BaseModel):
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

    class Config:
        validate_assignment = True
        use_enum_values = True


class UserInDB(UserBase):
    id: Optional[UUID] = None
    hashed_password: Optional[str] = None


class UserInToken(UserBase):
    pass


class User(schemas.UUIDSchemaMixin, schemas.AuditSchemaMixin, UserBase):
    pass
