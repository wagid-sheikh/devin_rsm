import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class CompanyContacts(BaseModel):
    email: EmailStr
    phone: str = Field(
        ..., pattern=r"^\+?[1-9]\d{1,14}$", description="Phone number in E.164 format"
    )
    alternate_phone: str | None = Field(
        None, pattern=r"^\+?[1-9]\d{1,14}$", description="Alternate phone in E.164 format"
    )
    website: str | None = None
    contact_person_name: str | None = None
    contact_person_designation: str | None = None

    @field_validator("phone", "alternate_phone")
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if not v.replace("+", "").replace("-", "").replace(" ", "").isdigit():
            raise ValueError("Phone number must contain only digits, spaces, hyphens, and optional leading +")
        return v


class CompanyAddress(BaseModel):
    address_line1: str = Field(..., min_length=1, max_length=200)
    address_line2: str | None = Field(None, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100, description="Indian state name")
    pincode: str = Field(..., pattern=r"^\d{6}$", description="6-digit Indian postal code")
    country: str = Field(default="India", max_length=100)
    landmark: str | None = Field(None, max_length=200)


class CompanyCreate(BaseModel):
    legal_name: str
    trade_name: str | None = None
    gstin: str | None = None
    pan: str | None = None
    contacts: CompanyContacts
    address: CompanyAddress


class CompanyUpdate(BaseModel):
    legal_name: str | None = None
    trade_name: str | None = None
    gstin: str | None = None
    pan: str | None = None
    contacts: CompanyContacts | None = None
    address: CompanyAddress | None = None
    status: str | None = None


class CompanyResponse(BaseModel):
    id: uuid.UUID
    legal_name: str
    trade_name: str | None
    gstin: str | None
    pan: str | None
    contacts: CompanyContacts
    address: CompanyAddress
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
