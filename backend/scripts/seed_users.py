import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select

from app.core.security import get_password_hash
from app.db.session import AsyncSessionLocal
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole


async def seed_users() -> None:
    import os

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Role))
        roles = {role.code: role for role in result.scalars().all()}

        if not roles:
            print("No roles found. Please run seed_roles.py first.")
            return

        default_password = os.getenv("SEED_USER_PASSWORD", "ChangeMe@123")

        test_users = [
            {
                "email": "admin@tsv.com",
                "password": default_password,
                "first_name": "Platform",
                "last_name": "Admin",
                "phone": "+1234567890",
                "status": "active",
                "roles": ["PLATFORM_ADMIN"],
            },
            {
                "email": "company.admin@tsv.com",
                "password": default_password,
                "first_name": "Company",
                "last_name": "Admin",
                "phone": "+1234567891",
                "status": "active",
                "roles": ["COMPANY_ADMIN"],
            },
            {
                "email": "store.manager@tsv.com",
                "password": default_password,
                "first_name": "Store",
                "last_name": "Manager",
                "phone": "+1234567892",
                "status": "active",
                "roles": ["STORE_MANAGER"],
            },
            {
                "email": "cashier@tsv.com",
                "password": default_password,
                "first_name": "Store",
                "last_name": "Cashier",
                "phone": "+1234567893",
                "status": "active",
                "roles": ["CASHIER"],
            },
        ]

        if default_password == "ChangeMe@123":
            print(
                "WARNING: Using default insecure password. "
                "Set SEED_USER_PASSWORD environment variable for custom password."
            )

        for user_data in test_users:
            result = await session.execute(
                select(User).where(User.email == user_data["email"])
            )
            existing_user = result.scalar_one_or_none()

            if existing_user:
                print(f"User {user_data['email']} already exists. Skipping.")
                continue

            user = User(
                email=str(user_data["email"]),
                password_hash=get_password_hash(str(user_data["password"])),
                first_name=str(user_data["first_name"]),
                last_name=str(user_data["last_name"]),
                phone=str(user_data["phone"]) if user_data["phone"] else None,
                status=str(user_data["status"]),
            )
            session.add(user)
            await session.flush()

            for role_code in user_data["roles"]:
                if role_code in roles:
                    user_role = UserRole(user_id=user.id, role_id=roles[role_code].id)
                    session.add(user_role)

            print(
                f"Created user: {user_data['email']} with roles: {', '.join(user_data['roles'])}"
            )

        await session.commit()
        print("User seeding completed successfully!")


if __name__ == "__main__":
    asyncio.run(seed_users())
