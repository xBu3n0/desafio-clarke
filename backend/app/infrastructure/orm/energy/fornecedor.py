from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.orm.base import Base

if TYPE_CHECKING:
    from app.infrastructure.orm.energy.logo import LogoModel
    from app.infrastructure.orm.energy.oferta import OfertaModel


class FornecedorModel(Base):
    __tablename__ = "fornecedores"
    __table_args__ = (
        CheckConstraint(
            "numero_clientes >= 0",
            name="ck_fornecedores_numero_clientes_gte_zero",
        ),
        CheckConstraint(
            "avaliacao_total >= 0",
            name="ck_fornecedores_avaliacao_total_gte_zero",
        ),
        CheckConstraint(
            "numero_avaliacoes >= 0",
            name="ck_fornecedores_numero_avaliacoes_gte_zero",
        ),
        CheckConstraint(
            "avaliacao_media >= 0 AND avaliacao_media <= 10",
            name="ck_fornecedores_avaliacao_media_range",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    logo_id: Mapped[int] = mapped_column(
        ForeignKey("logos.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    numero_clientes: Mapped[int] = mapped_column(nullable=False)
    avaliacao_total: Mapped[int] = mapped_column(nullable=False)
    numero_avaliacoes: Mapped[int] = mapped_column(nullable=False)
    avaliacao_media: Mapped[Decimal] = mapped_column(Numeric(3, 1), nullable=False)

    logo: Mapped[LogoModel] = relationship(
        back_populates="fornecedor",
        single_parent=True,
        cascade="all, delete-orphan",
    )
    ofertas: Mapped[list[OfertaModel]] = relationship(back_populates="fornecedor")
