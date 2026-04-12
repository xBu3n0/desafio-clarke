from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.orm.base import Base

if TYPE_CHECKING:
    from app.infrastructure.orm.energy.oferta import OfertaModel


class EstadoModel(Base):
    __tablename__ = "estados"
    __table_args__ = (
        CheckConstraint(
            "tarifa_base_kwh > 0",
            name="ck_estados_tarifa_base_kwh_gt_zero",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    sigla: Mapped[str] = mapped_column(String(2), nullable=False, unique=True)
    tarifa_base_kwh: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    ofertas: Mapped[list[OfertaModel]] = relationship(back_populates="estado")
