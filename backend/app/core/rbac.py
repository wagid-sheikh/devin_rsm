from collections.abc import Awaitable, Callable
from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.api.deps import get_current_user
from app.models.user import User


def require_role(*required_roles: str) -> Callable[[Annotated[User, Depends(get_current_user)]], Awaitable[User]]:
    async def role_checker(
        current_user: Annotated[User, Depends(get_current_user)]
    ) -> User:
        user_role_codes = {user_role.role.code for user_role in current_user.roles}

        if not any(role in user_role_codes for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role(s): {', '.join(required_roles)}",
            )

        return current_user

    return role_checker


def require_permission(permission_key: str) -> Callable[[Annotated[User, Depends(get_current_user)]], Awaitable[User]]:
    async def permission_checker(
        current_user: Annotated[User, Depends(get_current_user)]
    ) -> User:
        for user_role in current_user.roles:
            role_permissions = user_role.role.permissions or {}
            if role_permissions.get(permission_key) is True:
                return current_user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Required permission: {permission_key}",
        )

    return permission_checker
