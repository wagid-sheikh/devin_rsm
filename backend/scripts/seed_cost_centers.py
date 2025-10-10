"""Seed default cost centers"""

import asyncio

from sqlalchemy import select

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.cost_center import CostCenter

DEFAULT_COST_CENTERS = [
    {
        "code": "UN3668",
        "name": "UN3668 Cost Center",
        "active": True,
    },
    {
        "code": "KN3817",
        "name": "KN3817 Cost Center",
        "active": True,
    },
    {
        "code": "SC3567",
        "name": "SC3567 Cost Center",
        "active": True,
    },
    {
        "code": "SL1610",
        "name": "SL1610 Cost Center",
        "active": True,
    },
    {
        "code": "TSV001",
        "name": "TSV001 Cost Center",
        "active": True,
    },
]


async def seed_cost_centers() -> None:
    async with AsyncSessionLocal() as db:
        for cc_data in DEFAULT_COST_CENTERS:
            result = await db.execute(
                select(CostCenter).where(CostCenter.code == cc_data["code"])
            )
            existing_cc = result.scalar_one_or_none()

            if not existing_cc:
                cost_center = CostCenter(
                    code=cc_data["code"],
                    name=cc_data["name"],
                    active=cc_data["active"],
                )
                db.add(cost_center)
                print(
                    f"✓ Created cost center: {cc_data['name']} ({cc_data['code']})"
                )
            else:
                print(
                    f"- Cost center already exists: {cc_data['name']} ({cc_data['code']})"
                )

        await db.commit()
        print("\n✓ Cost center seeding completed!")


if __name__ == "__main__":
    print("Seeding default cost centers...")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Database: {settings.DATABASE_URL}\n")
    asyncio.run(seed_cost_centers())
