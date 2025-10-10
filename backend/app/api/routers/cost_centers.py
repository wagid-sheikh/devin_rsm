from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_db
from app.core.rbac import require_role
from app.models.company import Company
from app.models.company_cost_center import CompanyCostCenter
from app.models.cost_center import CostCenter
from app.models.user import User
from app.schemas.cost_center import (
    CompanyCostCenterCreate,
    CompanyCostCenterResponse,
    CostCenterCreate,
    CostCenterResponse,
    CostCenterUpdate,
)

router = APIRouter(prefix="/cost-centers", tags=["cost-centers"])


@router.post(
    "", response_model=CostCenterResponse, status_code=status.HTTP_201_CREATED
)
async def create_cost_center(
    cost_center_data: CostCenterCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("PLATFORM_ADMIN"))],
) -> CostCenterResponse:
    """Create a new global cost center (PLATFORM_ADMIN only)."""
    result = await db.execute(
        select(CostCenter).where(CostCenter.code == cost_center_data.code)
    )
    existing_cc = result.scalar_one_or_none()
    if existing_cc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cost center with code '{cost_center_data.code}' already exists",
        )

    cost_center = CostCenter(**cost_center_data.model_dump())
    db.add(cost_center)
    await db.commit()
    await db.refresh(cost_center)
    return CostCenterResponse.model_validate(cost_center)


@router.get("", response_model=list[CostCenterResponse])
async def list_cost_centers(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN"))
    ],
    active_only: bool = True,
) -> list[CostCenterResponse]:
    """List all global cost centers."""
    query = select(CostCenter)
    if active_only:
        query = query.where(CostCenter.active)

    result = await db.execute(query.order_by(CostCenter.code))
    cost_centers = result.scalars().all()
    return [CostCenterResponse.model_validate(cc) for cc in cost_centers]


@router.get("/{cost_center_id}", response_model=CostCenterResponse)
async def get_cost_center(
    cost_center_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN"))
    ],
) -> CostCenterResponse:
    """Get a specific cost center by ID."""
    result = await db.execute(
        select(CostCenter).where(CostCenter.id == cost_center_id)
    )
    cost_center = result.scalar_one_or_none()

    if not cost_center:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cost center not found",
        )

    return CostCenterResponse.model_validate(cost_center)


@router.patch("/{cost_center_id}", response_model=CostCenterResponse)
async def update_cost_center(
    cost_center_id: int,
    cost_center_data: CostCenterUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("PLATFORM_ADMIN"))],
) -> CostCenterResponse:
    """Update a cost center (PLATFORM_ADMIN only)."""
    result = await db.execute(
        select(CostCenter).where(CostCenter.id == cost_center_id)
    )
    cost_center = result.scalar_one_or_none()

    if not cost_center:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cost center not found",
        )

    update_data = cost_center_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(cost_center, field, value)

    await db.commit()
    await db.refresh(cost_center)
    return CostCenterResponse.model_validate(cost_center)


@router.delete("/{cost_center_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cost_center(
    cost_center_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("PLATFORM_ADMIN"))],
) -> None:
    """Soft delete a cost center (PLATFORM_ADMIN only)."""
    result = await db.execute(
        select(CostCenter).where(CostCenter.id == cost_center_id)
    )
    cost_center = result.scalar_one_or_none()

    if not cost_center:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cost center not found",
        )

    cost_center.active = False
    await db.commit()


@router.get(
    "/companies/{company_id}/cost-centers",
    response_model=list[CompanyCostCenterResponse],
)
async def list_company_cost_centers(
    company_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN"))
    ],
) -> list[CompanyCostCenterResponse]:
    """List cost centers assigned to a company."""
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    result = await db.execute(
        select(CompanyCostCenter)
        .where(CompanyCostCenter.company_id == company_id)
        .options(selectinload(CompanyCostCenter.cost_center))
    )
    assignments = result.scalars().all()
    return [CompanyCostCenterResponse.model_validate(a) for a in assignments]


@router.post(
    "/companies/{company_id}/cost-centers",
    response_model=CompanyCostCenterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def assign_cost_center_to_company(
    company_id: int,
    assignment_data: CompanyCostCenterCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN"))
    ],
) -> CompanyCostCenterResponse:
    """Assign a cost center to a company."""
    company_result = await db.execute(
        select(Company).where(Company.id == company_id)
    )
    company = company_result.scalar_one_or_none()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    cc_result = await db.execute(
        select(CostCenter).where(CostCenter.id == assignment_data.cost_center_id)
    )
    cost_center = cc_result.scalar_one_or_none()
    if not cost_center:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cost center not found",
        )
    if not cost_center.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot assign inactive cost center",
        )

    result = await db.execute(
        select(CompanyCostCenter).where(
            CompanyCostCenter.company_id == company_id,
            CompanyCostCenter.cost_center_id == assignment_data.cost_center_id,
        )
    )
    existing_assignment = result.scalar_one_or_none()
    if existing_assignment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cost center already assigned to this company",
        )

    if assignment_data.is_default:
        defaults_result = await db.execute(
            select(CompanyCostCenter).where(
                CompanyCostCenter.company_id == company_id,
                CompanyCostCenter.is_default,
            )
        )
        for existing_default in defaults_result.scalars().all():
            existing_default.is_default = False

    assignment = CompanyCostCenter(
        company_id=company_id,
        cost_center_id=assignment_data.cost_center_id,
        is_default=assignment_data.is_default,
    )
    db.add(assignment)
    await db.commit()
    await db.refresh(assignment, ["cost_center"])
    return CompanyCostCenterResponse.model_validate(assignment)


@router.delete(
    "/companies/{company_id}/cost-centers/{assignment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_cost_center_from_company(
    company_id: int,
    assignment_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN"))
    ],
) -> None:
    """Remove a cost center assignment from a company."""
    result = await db.execute(
        select(CompanyCostCenter).where(
            CompanyCostCenter.id == assignment_id,
            CompanyCostCenter.company_id == company_id,
        )
    )
    assignment = result.scalar_one_or_none()

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cost center assignment not found",
        )

    await db.delete(assignment)
    await db.commit()
