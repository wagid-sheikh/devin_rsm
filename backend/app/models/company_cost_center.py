from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.company import Company
    from app.models.cost_center import CostCenter


class CompanyCostCenter(Base):
    """Company-specific cost center assignments."""

    __tablename__ = "company_cost_centers"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("companies.id"), nullable=False, index=True
    )
    cost_center_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("cost_centers.id"), nullable=False, index=True
    )
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )

    company: Mapped["Company"] = relationship("Company", back_populates="cost_centers")
    cost_center: Mapped["CostCenter"] = relationship(
        "CostCenter", back_populates="company_assignments"
    )
