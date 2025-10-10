from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field


class RoleResponse(BaseModel):
    id: int
    code: str
    name: str
    description: str | None
    permissions: dict[str, Any]

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    phone: str | None
    first_name: str
    last_name: str
    status: str
    roles: list[RoleResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    phone: str | None = None
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    status: str = Field(default="active")


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    phone: str | None = None
    password: str | None = Field(None, min_length=8)
    first_name: str | None = Field(None, min_length=1, max_length=100)
    last_name: str | None = Field(None, min_length=1, max_length=100)
    status: str | None = None


class UserRoleAssignment(BaseModel):
    role_id: int
