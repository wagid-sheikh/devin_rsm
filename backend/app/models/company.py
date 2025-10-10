from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, BigInteger, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.company_cost_center import CompanyCostCenter
    from app.models.company_gstin import CompanyGSTIN
    from app.models.store import Store


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    legal_name: Mapped[str] = mapped_column(String(255), nullable=False)
    trade_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    pan: Mapped[str | None] = mapped_column(String(10), unique=True, index=True, nullable=True)
    contacts: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    address: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now(), onupdate=func.now()
    )

    stores: Mapped[list[Store]] = relationship("Store", back_populates="company")
    gstins: Mapped[list[CompanyGSTIN]] = relationship("CompanyGSTIN", back_populates="company")
    cost_centers: Mapped[list[CompanyCostCenter]] = relationship("CompanyCostCenter", back_populates="company")
