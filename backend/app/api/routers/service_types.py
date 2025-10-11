from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.rbac import require_role
from app.models.service_type import ServiceType
from app.models.user import User
from app.schemas.service_type import ServiceTypeResponse

router = APIRouter(prefix="/service-types", tags=["service-types"])


@router.get("", response_model=list[ServiceTypeResponse])
async def list_service_types(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "STORE_MANAGER", "STAFF"))
    ],
) -> list[ServiceTypeResponse]:
    query = select(ServiceType).where(ServiceType.active).order_by(ServiceType.name)
    result = await db.execute(query)
    service_types = result.scalars().all()
    return [ServiceTypeResponse.model_validate(st) for st in service_types]
