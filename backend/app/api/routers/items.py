from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.rbac import require_role
from app.models.item import Item
from app.models.user import User
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_data: ItemCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "STORE_MANAGER"))
    ],
) -> ItemResponse:
    if not current_user.store_accesses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have store access to create items",
        )

    company_id = current_user.store_accesses[0].store.company_id

    result = await db.execute(
        select(Item).where(
            Item.company_id == company_id,
            Item.sku == item_data.sku,
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Item with SKU '{item_data.sku}' already exists",
        )

    item = Item(
        company_id=company_id,
        **item_data.model_dump()
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return ItemResponse.model_validate(item)


@router.get("", response_model=list[ItemResponse])
async def list_items(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "STORE_MANAGER", "STAFF"))
    ],
    search: str | None = Query(None, description="Search by SKU or name"),
    status_filter: str | None = Query(None, description="Filter by status (active/inactive)"),
    type_filter: str | None = Query(None, description="Filter by type (service/product)"),
) -> list[ItemResponse]:
    if not current_user.store_accesses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have store access to view items",
        )

    company_id = current_user.store_accesses[0].store.company_id

    query = select(Item).where(Item.company_id == company_id)

    query = query.where(Item.status == status_filter) if status_filter else query.where(Item.status == "active")

    if type_filter:
        query = query.where(Item.type == type_filter)

    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                Item.sku.ilike(search_pattern),
                Item.name.ilike(search_pattern),
            )
        )

    query = query.order_by(Item.name)
    result = await db.execute(query)
    items = result.scalars().all()
    return [ItemResponse.model_validate(item) for item in items]


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "STORE_MANAGER", "STAFF"))
    ],
) -> ItemResponse:
    if not current_user.store_accesses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have store access to view items",
        )

    company_id = current_user.store_accesses[0].store.company_id

    result = await db.execute(
        select(Item).where(Item.id == item_id, Item.company_id == company_id)
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    return ItemResponse.model_validate(item)


@router.patch("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item_data: ItemUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "STORE_MANAGER"))
    ],
) -> ItemResponse:
    if not current_user.store_accesses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have store access to update items",
        )

    company_id = current_user.store_accesses[0].store.company_id

    result = await db.execute(
        select(Item).where(Item.id == item_id, Item.company_id == company_id)
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    if item_data.sku and item_data.sku != item.sku:
        result = await db.execute(
            select(Item).where(
                Item.company_id == company_id,
                Item.sku == item_data.sku,
                Item.id != item_id,
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Item with SKU '{item_data.sku}' already exists",
            )

    update_data = item_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return ItemResponse.model_validate(item)
