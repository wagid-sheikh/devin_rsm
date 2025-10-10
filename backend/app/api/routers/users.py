from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_db
from app.core.rbac import require_role
from app.core.security import get_password_hash
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserRoleAssignment,
    UserUpdate,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("PLATFORM_ADMIN"))],
) -> UserResponse:
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email '{user_data.email}' already exists",
        )

    user = User(
        email=user_data.email,
        phone=user_data.phone,
        password_hash=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        status=user_data.status,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user, ["roles"])

    result = await db.execute(
        select(User)
        .where(User.id == user.id)
        .options(selectinload(User.roles).selectinload(UserRole.role))
    )
    user_with_roles = result.scalar_one()

    user_dict = {
        "id": user_with_roles.id,
        "email": user_with_roles.email,
        "phone": user_with_roles.phone,
        "first_name": user_with_roles.first_name,
        "last_name": user_with_roles.last_name,
        "status": user_with_roles.status,
        "roles": [user_role.role for user_role in user_with_roles.roles],
        "created_at": user_with_roles.created_at,
        "updated_at": user_with_roles.updated_at,
    }

    return UserResponse.model_validate(user_dict)


@router.get("", response_model=list[UserResponse])
async def list_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN"))
    ],
    search: str | None = Query(None, description="Search by name or email"),
    status_filter: str | None = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> list[UserResponse]:
    query = select(User).options(selectinload(User.roles).selectinload(UserRole.role))

    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                User.email.ilike(search_pattern),
                User.first_name.ilike(search_pattern),
                User.last_name.ilike(search_pattern),
            )
        )

    if status_filter:
        query = query.where(User.status == status_filter)

    query = query.offset(skip).limit(limit).order_by(User.created_at.desc())

    result = await db.execute(query)
    users = result.scalars().all()

    return [
        UserResponse.model_validate(
            {
                "id": user.id,
                "email": user.email,
                "phone": user.phone,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "status": user.status,
                "roles": [user_role.role for user_role in user.roles],
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
        )
        for user in users
    ]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        User, Depends(require_role("PLATFORM_ADMIN", "COMPANY_ADMIN"))
    ],
) -> UserResponse:
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.roles).selectinload(UserRole.role))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user_dict = {
        "id": user.id,
        "email": user.email,
        "phone": user.phone,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "status": user.status,
        "roles": [user_role.role for user_role in user.roles],
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }

    return UserResponse.model_validate(user_dict)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("PLATFORM_ADMIN"))],
) -> UserResponse:
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.roles).selectinload(UserRole.role))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    update_data = user_data.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))

    if "email" in update_data and update_data["email"] != user.email:
        email_check = await db.execute(
            select(User).where(User.email == update_data["email"])
        )
        if email_check.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email '{update_data['email']}' already exists",
            )

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    result = await db.execute(
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.roles).selectinload(UserRole.role))
    )
    updated_user = result.scalar_one()

    user_dict = {
        "id": updated_user.id,
        "email": updated_user.email,
        "phone": updated_user.phone,
        "first_name": updated_user.first_name,
        "last_name": updated_user.last_name,
        "status": updated_user.status,
        "roles": [user_role.role for user_role in updated_user.roles],
        "created_at": updated_user.created_at,
        "updated_at": updated_user.updated_at,
    }

    return UserResponse.model_validate(user_dict)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("PLATFORM_ADMIN"))],
) -> None:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.status = "inactive"
    await db.commit()


@router.post(
    "/{user_id}/roles",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def assign_role_to_user(
    user_id: int,
    role_assignment: UserRoleAssignment,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("PLATFORM_ADMIN"))],
) -> UserResponse:
    user_result = await db.execute(
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.roles).selectinload(UserRole.role))
    )
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    role_result = await db.execute(
        select(Role).where(Role.id == role_assignment.role_id)
    )
    role = role_result.scalar_one_or_none()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    existing_assignment = await db.execute(
        select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role_assignment.role_id,
        )
    )
    if existing_assignment.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has this role",
        )

    user_role = UserRole(user_id=user_id, role_id=role_assignment.role_id)
    db.add(user_role)
    await db.commit()

    result = await db.execute(
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.roles).selectinload(UserRole.role))
    )
    updated_user = result.scalar_one()

    user_dict = {
        "id": updated_user.id,
        "email": updated_user.email,
        "phone": updated_user.phone,
        "first_name": updated_user.first_name,
        "last_name": updated_user.last_name,
        "status": updated_user.status,
        "roles": [user_role.role for user_role in updated_user.roles],
        "created_at": updated_user.created_at,
        "updated_at": updated_user.updated_at,
    }

    return UserResponse.model_validate(user_dict)


@router.delete("/{user_id}/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_role_from_user(
    user_id: int,
    role_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("PLATFORM_ADMIN"))],
) -> None:
    result = await db.execute(
        select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id,
        )
    )
    user_role = result.scalar_one_or_none()

    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role assignment not found",
        )

    await db.delete(user_role)
    await db.commit()
