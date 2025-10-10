from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_db
from app.core.rbac import require_role
from app.models.customer import Customer
from app.models.user import User
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_data: CustomerCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "STORE_MANAGER"))
    ],
) -> CustomerResponse:
    """Create a new customer."""
    if not current_user.store_accesses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have store access to create customers",
        )

    company_id = current_user.store_accesses[0].store.company_id

    if customer_data.code:
        result = await db.execute(
            select(Customer).where(
                Customer.company_id == company_id,
                Customer.code == customer_data.code,
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Customer with code '{customer_data.code}' already exists",
            )

    customer = Customer(
        company_id=company_id,
        **customer_data.model_dump()
    )
    db.add(customer)
    await db.commit()
    await db.refresh(customer, ["contacts", "addresses"])
    return CustomerResponse.model_validate(customer)


@router.get("", response_model=list[CustomerResponse])
async def list_customers(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "STORE_MANAGER"))
    ],
    search: str | None = Query(None, description="Search by name, phone, or email"),
    status_filter: str | None = Query(None, description="Filter by status (active/inactive)"),
) -> list[CustomerResponse]:
    """List all customers for the user's company with optional search."""
    if not current_user.store_accesses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have store access to view customers",
        )

    company_id = current_user.store_accesses[0].store.company_id

    query = select(Customer).where(Customer.company_id == company_id)

    query = query.where(Customer.status == status_filter) if status_filter else query.where(Customer.status == "active")

    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                Customer.name.ilike(search_pattern),
                Customer.phone_primary.ilike(search_pattern),
                Customer.email.ilike(search_pattern),
                Customer.code.ilike(search_pattern),
            )
        )

    query = query.options(
        selectinload(Customer.contacts),
        selectinload(Customer.addresses)
    ).order_by(Customer.name)

    result = await db.execute(query)
    customers = result.scalars().all()
    return [CustomerResponse.model_validate(customer) for customer in customers]


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "STORE_MANAGER"))
    ],
) -> CustomerResponse:
    """Get a specific customer by ID."""
    if not current_user.store_accesses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have store access to view customers",
        )

    company_id = current_user.store_accesses[0].store.company_id

    result = await db.execute(
        select(Customer)
        .where(Customer.id == customer_id, Customer.company_id == company_id)
        .options(
            selectinload(Customer.contacts),
            selectinload(Customer.addresses)
        )
    )
    customer = result.scalar_one_or_none()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return CustomerResponse.model_validate(customer)


@router.patch("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "STORE_MANAGER"))
    ],
) -> CustomerResponse:
    """Update a customer."""
    if not current_user.store_accesses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have store access to update customers",
        )

    company_id = current_user.store_accesses[0].store.company_id

    result = await db.execute(
        select(Customer)
        .where(Customer.id == customer_id, Customer.company_id == company_id)
        .options(
            selectinload(Customer.contacts),
            selectinload(Customer.addresses)
        )
    )
    customer = result.scalar_one_or_none()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    update_data = customer_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(customer, field, value)

    await db.commit()
    await db.refresh(customer, ["contacts", "addresses"])
    return CustomerResponse.model_validate(customer)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "STORE_MANAGER"))
    ],
) -> None:
    """Soft delete a customer by setting status to inactive."""
    if not current_user.store_accesses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have store access to delete customers",
        )

    company_id = current_user.store_accesses[0].store.company_id

    result = await db.execute(
        select(Customer).where(Customer.id == customer_id, Customer.company_id == company_id)
    )
    customer = result.scalar_one_or_none()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    customer.status = "inactive"
    await db.commit()
