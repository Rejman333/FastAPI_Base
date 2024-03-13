from datetime import datetime
from typing import Optional

from pydantic import EmailStr, SecretStr, ConfigDict

from app.schemas.schemas_base import BaseSchema


class UserBase(BaseSchema):
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    email: EmailStr
    password: SecretStr


class UserLogin(UserBase):
    email: EmailStr
    password: SecretStr


class UserResponse(UserBase):
    id: int
    email: EmailStr
    is_superuser: Optional[bool]
    is_verified: Optional[bool]


class UserUpdate:
    pass


class UserInDB(UserBase):
    id: int
    hashed_password: SecretStr
    is_superuser: bool
    is_verified: bool
    created_date: datetime
    updated_at: datetime
    deleted_at: datetime | None

    model_config = ConfigDict(from_attributes=True)