from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_accessible_company_ids, get_db
from app.core.rbac import require_role
from app.models.store import Store
from app.models.user import User
from app.schemas.store import StoreCreate, StoreResponse, StoreUpdate

router = APIRouter(prefix="/stores", tags=["stores"])


@router.post("", response_model=StoreResponse, status_code=status.HTTP_201_CREATED)
async def create_store(
    store_data: StoreCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN"))],
) -> StoreResponse:
    store = Store(**store_data.model_dump())
    db.add(store)
    await db.commit()
    await db.refresh(store)
    return StoreResponse.model_validate(store)


@router.get("", response_model=list[StoreResponse])
async def list_stores(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User,
        Depends(
            require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "AREA_MANAGER", "STORE_MANAGER")
        ),
    ],
    accessible_company_ids: Annotated[set[int], Depends(get_accessible_company_ids)],
) -> list[StoreResponse]:
    query = select(Store).where(Store.status == "active")

    user_role_codes = {user_role.role.code for user_role in current_user.roles}
    if "PLATFORM_ADMIN" not in user_role_codes:
        if not accessible_company_ids:
            return []
        query = query.where(Store.company_id.in_(accessible_company_ids))

    result = await db.execute(query)
    stores = result.scalars().all()
    return [StoreResponse.model_validate(store) for store in stores]


@router.get("/{store_id}", response_model=StoreResponse)
async def get_store(
    store_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User,
        Depends(
            require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "AREA_MANAGER", "STORE_MANAGER")
        ),
    ],
    accessible_company_ids: Annotated[set[int], Depends(get_accessible_company_ids)],
) -> StoreResponse:
    result = await db.execute(select(Store).where(Store.id == store_id))
    store = result.scalar_one_or_none()

    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )

    user_role_codes = {user_role.role.code for user_role in current_user.roles}
    if "PLATFORM_ADMIN" not in user_role_codes and store.company_id not in accessible_company_ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this store",
        )

    return StoreResponse.model_validate(store)


@router.patch("/{store_id}", response_model=StoreResponse)
async def update_store(
    store_id: int,
    store_data: StoreUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN"))],
    accessible_company_ids: Annotated[set[int], Depends(get_accessible_company_ids)],
) -> StoreResponse:
    result = await db.execute(select(Store).where(Store.id == store_id))
    store = result.scalar_one_or_none()

    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )

    user_role_codes = {user_role.role.code for user_role in current_user.roles}
    if "PLATFORM_ADMIN" not in user_role_codes and store.company_id not in accessible_company_ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this store",
        )

    update_data = store_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(store, field, value)

    await db.commit()
    await db.refresh(store)
    return StoreResponse.model_validate(store)


@router.delete("/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_store(
    store_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN"))],
    accessible_company_ids: Annotated[set[int], Depends(get_accessible_company_ids)],
) -> None:
    result = await db.execute(select(Store).where(Store.id == store_id))
    store = result.scalar_one_or_none()

    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )

    user_role_codes = {user_role.role.code for user_role in current_user.roles}
    if "PLATFORM_ADMIN" not in user_role_codes and store.company_id not in accessible_company_ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this store",
        )

    store.status = "inactive"
    await db.commit()
