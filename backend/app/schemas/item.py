from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    sku: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=255)
    type: str = Field(..., pattern="^(service|product)$")
    hsn_sac: str | None = Field(None, max_length=20)
    uom: str = Field(..., pattern="^(piece|kg)$")
    tax_rate: Decimal = Field(..., ge=0, le=100)


class ItemUpdate(BaseModel):
    sku: str | None = Field(None, min_length=1, max_length=100)
    name: str | None = Field(None, min_length=1, max_length=255)
    type: str | None = Field(None, pattern="^(service|product)$")
    hsn_sac: str | None = Field(None, max_length=20)
    uom: str | None = Field(None, pattern="^(piece|kg)$")
    tax_rate: Decimal | None = Field(None, ge=0, le=100)
    status: str | None = None


class ItemResponse(BaseModel):
    id: int
    company_id: int
    sku: str
    name: str
    type: str
    hsn_sac: str | None
    uom: str
    tax_rate: Decimal
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
