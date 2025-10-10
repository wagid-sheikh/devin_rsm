from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class UserStoreAccessCreate(BaseModel):
    store_id: int
    scope: Literal["view", "edit", "approve"] = Field(default="view")


class UserStoreAccessUpdate(BaseModel):
    scope: Literal["view", "edit", "approve"]


class StoreAccessInfo(BaseModel):
    id: int
    name: str
    company_id: int

    class Config:
        from_attributes = True


class UserStoreAccessResponse(BaseModel):
    id: int
    user_id: int
    store_id: int
    scope: str
    store: StoreAccessInfo
    created_at: datetime

    class Config:
        from_attributes = True
