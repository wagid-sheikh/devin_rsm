import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel


class CompanyCreate(BaseModel):
    legal_name: str
    trade_name: str | None = None
    gstin: str | None = None
    pan: str | None = None
    contacts: dict[str, Any] = {}
    address: dict[str, Any] = {}


class CompanyUpdate(BaseModel):
    legal_name: str | None = None
    trade_name: str | None = None
    gstin: str | None = None
    pan: str | None = None
    contacts: dict[str, Any] | None = None
    address: dict[str, Any] | None = None
    status: str | None = None


class CompanyResponse(BaseModel):
    id: uuid.UUID
    legal_name: str
    trade_name: str | None
    gstin: str | None
    pan: str | None
    contacts: dict[str, Any]
    address: dict[str, Any]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
