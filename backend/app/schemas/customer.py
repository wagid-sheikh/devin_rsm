from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class CustomerCreate(BaseModel):
    code: str | None = Field(None, max_length=50)
    name: str = Field(..., min_length=1, max_length=255)
    phone_primary: str = Field(
        ..., pattern=r"^\+?[1-9]\d{1,14}$", description="Phone number in E.164 format"
    )
    email: EmailStr | None = None
    notes: str | None = None


class CustomerUpdate(BaseModel):
    code: str | None = Field(None, max_length=50)
    name: str | None = Field(None, min_length=1, max_length=255)
    phone_primary: str | None = Field(
        None, pattern=r"^\+?[1-9]\d{1,14}$", description="Phone number in E.164 format"
    )
    email: EmailStr | None = None
    notes: str | None = None
    status: str | None = None


class CustomerContactResponse(BaseModel):
    id: int
    customer_id: int
    contact_person: str
    phone: str
    email: str | None
    is_primary: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CustomerAddressResponse(BaseModel):
    id: int
    customer_id: int
    type: str
    address: str
    is_pickup_default: bool
    is_delivery_default: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CustomerResponse(BaseModel):
    id: int
    company_id: int
    code: str | None
    name: str
    phone_primary: str
    email: str | None
    notes: str | None
    status: str
    contacts: list[CustomerContactResponse]
    addresses: list[CustomerAddressResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
