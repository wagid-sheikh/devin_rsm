from datetime import datetime

from pydantic import BaseModel


class ServiceTypeResponse(BaseModel):
    id: int
    code: str
    name: str
    description: str | None
    active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
