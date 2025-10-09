"""Seed default roles for the RBAC system"""
import asyncio

from sqlalchemy import select

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.role import Role

DEFAULT_ROLES = [
    {
        "code": "PLATFORM_ADMIN",
        "name": "Platform Administrator",
        "description": "Full system access across all companies and stores",
        "permissions": {
            "system:manage": True,
            "company:manage": True,
            "store:manage": True,
            "user:manage": True,
            "role:manage": True,
        },
    },
    {
        "code": "COMPANY_ADMIN",
        "name": "Company Administrator",
        "description": "Full access within a company and its stores",
        "permissions": {
            "company:view": True,
            "company:edit": True,
            "store:manage": True,
            "user:manage": True,
            "inventory:manage": True,
            "order:manage": True,
            "customer:manage": True,
        },
    },
    {
        "code": "AREA_MANAGER",
        "name": "Area Manager",
        "description": "Manage multiple stores within an area",
        "permissions": {
            "store:view": True,
            "store:edit": True,
            "inventory:manage": True,
            "order:manage": True,
            "customer:manage": True,
            "report:view": True,
        },
    },
    {
        "code": "STORE_MANAGER",
        "name": "Store Manager",
        "description": "Full access within assigned store(s)",
        "permissions": {
            "store:view": True,
            "inventory:manage": True,
            "order:manage": True,
            "customer:manage": True,
            "staff:manage": True,
            "report:view": True,
        },
    },
    {
        "code": "STAFF",
        "name": "Staff",
        "description": "Basic operational access for store staff",
        "permissions": {
            "order:create": True,
            "order:view": True,
            "customer:view": True,
            "customer:create": True,
            "inventory:view": True,
        },
    },
    {
        "code": "ACCOUNTANT",
        "name": "Accountant",
        "description": "Financial and reporting access",
        "permissions": {
            "report:view": True,
            "invoice:view": True,
            "invoice:manage": True,
            "payment:view": True,
            "payment:manage": True,
        },
    },
    {
        "code": "B2B_SALES",
        "name": "B2B Sales",
        "description": "Business-to-business sales representative",
        "permissions": {
            "customer:view": True,
            "customer:create": True,
            "order:create": True,
            "order:view": True,
            "quote:manage": True,
        },
    },
]


async def seed_roles() -> None:
    async with AsyncSessionLocal() as db:
        for role_data in DEFAULT_ROLES:
            result = await db.execute(select(Role).where(Role.code == role_data["code"]))
            existing_role = result.scalar_one_or_none()

            if not existing_role:
                role = Role(
                    code=role_data["code"],
                    name=role_data["name"],
                    description=role_data["description"],
                    permissions=role_data["permissions"],
                    status="active",
                )
                db.add(role)
                print(f"✓ Created role: {role_data['name']} ({role_data['code']})")
            else:
                print(f"- Role already exists: {role_data['name']} ({role_data['code']})")

        await db.commit()
        print("\n✓ Role seeding completed!")


if __name__ == "__main__":
    print("Seeding default roles...")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Database: {settings.DATABASE_URL}\n")
    asyncio.run(seed_roles())
