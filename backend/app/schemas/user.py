from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr


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
