import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_current_user
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    is_token_revoked,
    revoke_token,
    verify_password,
)
from app.db.session import get_db
from app.models.user import User
from app.models.user_role import UserRole
from app.schemas.auth import (
    LoginRequest,
    LogoutRequest,
    MessageResponse,
    RefreshRequest,
    RefreshResponse,
    TokenResponse,
)
from app.schemas.user import UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: LoginRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenResponse:
    result = await db.execute(select(User).where(User.email == credentials.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is not active",
        )

    access_jti = str(uuid.uuid4())
    refresh_jti = str(uuid.uuid4())

    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "jti": access_jti}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id), "jti": refresh_jti}
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model=RefreshResponse)
async def refresh(
    request: RefreshRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RefreshResponse:
    try:
        payload = decode_token(request.refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        ) from e

    token_type = payload.get("type")
    if token_type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    jti = payload.get("jti")
    if jti and is_token_revoked(jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has been revoked",
        )

    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    try:
        user_int_id = int(user_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format",
        ) from exc

    result = await db.execute(select(User).where(User.id == user_int_id))
    user = result.scalar_one_or_none()

    if not user or user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or not active",
        )

    new_access_jti = str(uuid.uuid4())
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "jti": new_access_jti}
    )

    return RefreshResponse(access_token=access_token)


@router.post("/logout", response_model=MessageResponse)
async def logout(request: LogoutRequest) -> MessageResponse:
    if request.refresh_token:
        try:
            payload = decode_token(request.refresh_token)
            jti = payload.get("jti")
            exp = payload.get("exp")
            if jti and exp:
                try:
                    revoke_token(jti, exp)
                except Exception as e:
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f"Failed to revoke token in Redis: {e}")
        except ValueError:
            pass

    return MessageResponse(message="Successfully logged out")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserResponse:
    result = await db.execute(
        select(User)
        .where(User.id == current_user.id)
        .options(
            selectinload(User.roles).selectinload(UserRole.role),
            selectinload(User.store_accesses)
        )
    )
    user_with_data = result.scalar_one()

    user_dict = {
        "id": user_with_data.id,
        "email": user_with_data.email,
        "phone": user_with_data.phone,
        "first_name": user_with_data.first_name,
        "last_name": user_with_data.last_name,
        "status": user_with_data.status,
        "roles": [user_role.role for user_role in user_with_data.roles],
        "store_accesses": user_with_data.store_accesses,
        "created_at": user_with_data.created_at,
        "updated_at": user_with_data.updated_at,
    }

    return UserResponse.model_validate(user_dict)
