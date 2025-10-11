"""Seed default service types"""

import asyncio

from sqlalchemy import select

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.service_type import ServiceType

DEFAULT_SERVICE_TYPES = [
    {
        "code": "WASH_FOLD",
        "name": "Wash & Fold",
        "description": "Basic washing and folding service",
        "active": True,
    },
    {
        "code": "PREMIUM_WASH",
        "name": "Premium Wash",
        "description": "Premium washing service",
        "active": True,
    },
    {
        "code": "PREMIUM_WASH_IRON",
        "name": "Premium Wash & Iron",
        "description": "Premium washing and ironing service",
        "active": True,
    },
    {
        "code": "IRON",
        "name": "Iron",
        "description": "Ironing service only",
        "active": True,
    },
    {
        "code": "DRY_CLEANING",
        "name": "Dry Cleaning",
        "description": "Professional dry cleaning service",
        "active": True,
    },
]


async def seed_service_types() -> None:
    async with AsyncSessionLocal() as db:
        for st_data in DEFAULT_SERVICE_TYPES:
            result = await db.execute(
                select(ServiceType).where(ServiceType.code == st_data["code"])
            )
            existing_st = result.scalar_one_or_none()

            if not existing_st:
                service_type = ServiceType(
                    code=st_data["code"],
                    name=st_data["name"],
                    description=st_data["description"],
                    active=st_data["active"],
                )
                db.add(service_type)
                print(
                    f"✓ Created service type: {st_data['name']} ({st_data['code']})"
                )
            else:
                print(
                    f"- Service type already exists: {st_data['name']} ({st_data['code']})"
                )

        await db.commit()
        print("\n✓ Service type seeding completed!")


if __name__ == "__main__":
    print("Seeding default service types...")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Database: {settings.DATABASE_URL}\n")
    asyncio.run(seed_service_types())
