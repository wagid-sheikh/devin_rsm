from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.store import Store
    from app.models.user import User


class UserStoreAccess(Base):
    __tablename__ = "user_store_access"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    store_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, index=True
    )
    scope: Mapped[str] = mapped_column(String(50), nullable=False, default="full")

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )

    user: Mapped[User] = relationship("User", back_populates="store_accesses")
    store: Mapped[Store] = relationship("Store", back_populates="user_accesses")
