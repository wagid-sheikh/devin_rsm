from datetime import datetime

from pydantic import BaseModel, Field


class CostCenterBase(BaseModel):
    code: str = Field(
        ..., min_length=1, max_length=50, description="Unique cost center code"
    )
    name: str = Field(..., min_length=1, max_length=255, description="Cost center name")
    active: bool = True


class CostCenterCreate(CostCenterBase):
    pass


class CostCenterUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    active: bool | None = None


class CostCenterResponse(CostCenterBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CompanyCostCenterCreate(BaseModel):
    cost_center_id: int
    is_default: bool = False


class CompanyCostCenterResponse(BaseModel):
    id: int
    company_id: int
    cost_center_id: int
    is_default: bool
    cost_center: CostCenterResponse
    created_at: datetime

    class Config:
        from_attributes = True
