from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.value_objects import Solucao
from app.infrastructure.orm.base import Base

if TYPE_CHECKING:
    from app.infrastructure.orm.energy.fornecedor import FornecedorModel
    from app.infrastructure.orm.shared.estado import EstadoModel


class OfertaModel(Base):
    __tablename__ = "ofertas"
    __table_args__ = (
        UniqueConstraint(
            "estado_id",
            "fornecedor_id",
            "solucao",
            name="uq_ofertas_estado_fornecedor_solucao",
        ),
        CheckConstraint(
            "custo_kwh > 0",
            name="ck_ofertas_custo_kwh_gt_zero",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    estado_id: Mapped[int] = mapped_column(
        ForeignKey("estados.id", ondelete="CASCADE"),
        nullable=False,
    )
    fornecedor_id: Mapped[int] = mapped_column(
        ForeignKey("fornecedores.id", ondelete="CASCADE"),
        nullable=False,
    )
    solucao: Mapped[Solucao] = mapped_column(
        Enum(
            Solucao,
            native_enum=False,
            validate_strings=True,
            values_callable=lambda enum_class: [member.value for member in enum_class],
        ),
        nullable=False,
    )
    custo_kwh: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    estado: Mapped[EstadoModel] = relationship(back_populates="ofertas")
    fornecedor: Mapped[FornecedorModel] = relationship(back_populates="ofertas")
