"""create initial schema

Revision ID: 20260411_000001
Revises:
Create Date: 2026-04-11 00:00:01

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260411_000001"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "estados",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nome", sa.String(length=255), nullable=False),
        sa.Column("sigla", sa.String(length=2), nullable=False),
        sa.Column("tarifa_base_kwh", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.CheckConstraint(
            "tarifa_base_kwh > 0",
            name="ck_estados_tarifa_base_kwh_gt_zero",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sigla"),
    )
    op.create_table(
        "logos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("url", sa.String(length=500), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "fornecedores",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nome", sa.String(length=255), nullable=False),
        sa.Column("logo_id", sa.Integer(), nullable=False),
        sa.Column("numero_clientes", sa.Integer(), nullable=False),
        sa.Column("avaliacao_total", sa.Integer(), nullable=False),
        sa.Column("numero_avaliacoes", sa.Integer(), nullable=False),
        sa.Column("avaliacao_media", sa.Numeric(precision=3, scale=1), nullable=False),
        sa.CheckConstraint(
            "avaliacao_media >= 0 AND avaliacao_media <= 10",
            name="ck_fornecedores_avaliacao_media_range",
        ),
        sa.CheckConstraint(
            "avaliacao_total >= 0",
            name="ck_fornecedores_avaliacao_total_gte_zero",
        ),
        sa.CheckConstraint(
            "numero_avaliacoes >= 0",
            name="ck_fornecedores_numero_avaliacoes_gte_zero",
        ),
        sa.CheckConstraint(
            "numero_clientes >= 0",
            name="ck_fornecedores_numero_clientes_gte_zero",
        ),
        sa.ForeignKeyConstraint(
            ["logo_id"],
            ["logos.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("logo_id"),
    )
    op.create_table(
        "ofertas",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("estado_id", sa.Integer(), nullable=False),
        sa.Column("fornecedor_id", sa.Integer(), nullable=False),
        sa.Column(
            "solucao",
            sa.Enum("GD", "Mercado Livre", name="solucao", native_enum=False),
            nullable=False,
        ),
        sa.Column("custo_kwh", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.CheckConstraint(
            "custo_kwh > 0",
            name="ck_ofertas_custo_kwh_gt_zero",
        ),
        sa.ForeignKeyConstraint(
            ["estado_id"],
            ["estados.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["fornecedor_id"],
            ["fornecedores.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "estado_id",
            "fornecedor_id",
            "solucao",
            name="uq_ofertas_estado_fornecedor_solucao",
        ),
    )


def downgrade() -> None:
    op.drop_table("ofertas")
    op.drop_table("fornecedores")
    op.drop_table("logos")
    op.drop_table("estados")
