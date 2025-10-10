from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_db
from app.core.rbac import require_role
from app.models.customer import Customer
from app.models.customer_address import CustomerAddress
from app.models.customer_contact import CustomerContact
from app.models.user import User
from app.schemas.customer import (
    CustomerAddressCreate,
    CustomerAddressResponse,
    CustomerAddressUpdate,
    CustomerContactCreate,
    CustomerContactResponse,
    CustomerContactUpdate,
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
)

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


@router.post("/{customer_id}/contacts", response_model=CustomerContactResponse, status_code=status.HTTP_201_CREATED)
async def create_customer_contact(
    customer_id: int,
    contact_data: CustomerContactCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "STORE_MANAGER"))
    ],
) -> CustomerContactResponse:
    """Create a new contact for a customer."""
    if not current_user.store_accesses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have store access to manage customer contacts",
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

    if contact_data.is_primary:
        existing_primary = (await db.execute(
            select(CustomerContact)
            .where(CustomerContact.customer_id == customer_id, CustomerContact.is_primary)
        )).scalar_one_or_none()
        if existing_primary:
            existing_primary.is_primary = False

    contact = CustomerContact(
        customer_id=customer_id,
        **contact_data.model_dump()
    )
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return CustomerContactResponse.model_validate(contact)


@router.get("/{customer_id}/contacts", response_model=list[CustomerContactResponse])
async def list_customer_contacts(
    customer_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "STORE_MANAGER"))
    ],
) -> list[CustomerContactResponse]:
    """List all contacts for a customer."""
    if not current_user.store_accesses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have store access to view customer contacts",
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

    result = await db.execute(
        select(CustomerContact)
        .where(CustomerContact.customer_id == customer_id)
        .order_by(CustomerContact.is_primary.desc(), CustomerContact.contact_person)
    )
    contacts = result.scalars().all()
    return [CustomerContactResponse.model_validate(contact) for contact in contacts]


@router.patch("/{customer_id}/contacts/{contact_id}", response_model=CustomerContactResponse)
async def update_customer_contact(
    customer_id: int,
    contact_id: int,
    contact_data: CustomerContactUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "STORE_MANAGER"))
    ],
) -> CustomerContactResponse:
    """Update a customer contact."""
    if not current_user.store_accesses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have store access to update customer contacts",
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

    result = await db.execute(
        select(CustomerContact).where(
            CustomerContact.id == contact_id,
            CustomerContact.customer_id == customer_id
        )
    )
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )

    update_data = contact_data.model_dump(exclude_unset=True)
    if update_data.get("is_primary") is True:
        existing_primary = (await db.execute(
            select(CustomerContact)
            .where(
                CustomerContact.customer_id == customer_id,
                CustomerContact.is_primary,
                CustomerContact.id != contact_id
            )
        )).scalar_one_or_none()
        if existing_primary:
            existing_primary.is_primary = False

    for field, value in update_data.items():
        setattr(contact, field, value)

    await db.commit()
    await db.refresh(contact)
    return CustomerContactResponse.model_validate(contact)


@router.delete("/{customer_id}/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_contact(
    customer_id: int,
    contact_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "STORE_MANAGER"))
    ],
) -> None:
    """Delete a customer contact."""
    if not current_user.store_accesses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have store access to delete customer contacts",
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

    result = await db.execute(
        select(CustomerContact).where(
            CustomerContact.id == contact_id,
            CustomerContact.customer_id == customer_id
        )
    )
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )

    await db.delete(contact)
    await db.commit()


@router.post("/{customer_id}/addresses", response_model=CustomerAddressResponse, status_code=status.HTTP_201_CREATED)
async def create_customer_address(
    customer_id: int,
    address_data: CustomerAddressCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "STORE_MANAGER"))
    ],
) -> CustomerAddressResponse:
    """Create a new address for a customer."""
    if not current_user.store_accesses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have store access to manage customer addresses",
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

    if address_data.is_pickup_default:
        existing_default = (await db.execute(
            select(CustomerAddress)
            .where(CustomerAddress.customer_id == customer_id, CustomerAddress.is_pickup_default)
        )).scalar_one_or_none()
        if existing_default:
            existing_default.is_pickup_default = False

    if address_data.is_delivery_default:
        existing_default = (await db.execute(
            select(CustomerAddress)
            .where(CustomerAddress.customer_id == customer_id, CustomerAddress.is_delivery_default)
        )).scalar_one_or_none()
        if existing_default:
            existing_default.is_delivery_default = False

    address = CustomerAddress(
        customer_id=customer_id,
        **address_data.model_dump()
    )
    db.add(address)
    await db.commit()
    await db.refresh(address)
    return CustomerAddressResponse.model_validate(address)


@router.get("/{customer_id}/addresses", response_model=list[CustomerAddressResponse])
async def list_customer_addresses(
    customer_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "STORE_MANAGER"))
    ],
) -> list[CustomerAddressResponse]:
    """List all addresses for a customer."""
    if not current_user.store_accesses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have store access to view customer addresses",
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

    result = await db.execute(
        select(CustomerAddress)
        .where(CustomerAddress.customer_id == customer_id)
        .order_by(CustomerAddress.is_pickup_default.desc(), CustomerAddress.type)
    )
    addresses = result.scalars().all()
    return [CustomerAddressResponse.model_validate(address) for address in addresses]


@router.patch("/{customer_id}/addresses/{address_id}", response_model=CustomerAddressResponse)
async def update_customer_address(
    customer_id: int,
    address_id: int,
    address_data: CustomerAddressUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "STORE_MANAGER"))
    ],
) -> CustomerAddressResponse:
    """Update a customer address."""
    if not current_user.store_accesses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have store access to update customer addresses",
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

    result = await db.execute(
        select(CustomerAddress).where(
            CustomerAddress.id == address_id,
            CustomerAddress.customer_id == customer_id
        )
    )
    address = result.scalar_one_or_none()
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )

    update_data = address_data.model_dump(exclude_unset=True)

    if update_data.get("is_pickup_default") is True:
        existing_default = (await db.execute(
            select(CustomerAddress)
            .where(
                CustomerAddress.customer_id == customer_id,
                CustomerAddress.is_pickup_default,
                CustomerAddress.id != address_id
            )
        )).scalar_one_or_none()
        if existing_default:
            existing_default.is_pickup_default = False

    if update_data.get("is_delivery_default") is True:
        existing_default = (await db.execute(
            select(CustomerAddress)
            .where(
                CustomerAddress.customer_id == customer_id,
                CustomerAddress.is_delivery_default,
                CustomerAddress.id != address_id
            )
        )).scalar_one_or_none()
        if existing_default:
            existing_default.is_delivery_default = False

    for field, value in update_data.items():
        setattr(address, field, value)

    await db.commit()
    await db.refresh(address)
    return CustomerAddressResponse.model_validate(address)


@router.delete("/{customer_id}/addresses/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_address(
    customer_id: int,
    address_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN", "STORE_MANAGER"))
    ],
) -> None:
    """Delete a customer address."""
    if not current_user.store_accesses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have store access to delete customer addresses",
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

    result = await db.execute(
        select(CustomerAddress).where(
            CustomerAddress.id == address_id,
            CustomerAddress.customer_id == customer_id
        )
    )
    address = result.scalar_one_or_none()
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found",
        )

    await db.delete(address)
    await db.commit()
