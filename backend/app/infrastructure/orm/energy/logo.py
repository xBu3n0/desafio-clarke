from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.orm.base import Base

if TYPE_CHECKING:
    from app.infrastructure.orm.energy.fornecedor import FornecedorModel


class LogoModel(Base):
    __tablename__ = "logos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(500), nullable=False)

    fornecedor: Mapped[FornecedorModel] = relationship(
        back_populates="logo",
        uselist=False,
    )
