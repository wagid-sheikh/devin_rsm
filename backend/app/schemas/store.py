from datetime import datetime

from pydantic import BaseModel


class StoreCreate(BaseModel):
    company_id: int
    name: str
    address: str
    is_franchise: bool = False
    timezone: str = "Asia/Kolkata"
    invoice_series_prefix: str


class StoreUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    is_franchise: bool | None = None
    status: str | None = None
    timezone: str | None = None
    invoice_series_prefix: str | None = None


class StoreResponse(BaseModel):
    id: int
    company_id: int
    name: str
    address: str
    is_franchise: bool
    status: str
    timezone: str
    invoice_series_prefix: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
