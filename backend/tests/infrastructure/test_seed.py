from decimal import Decimal

from sqlalchemy import func, select

from app.infrastructure.database import (
    create_engine_from_url,
    create_schema,
    create_session_factory,
)
from app.infrastructure.orm import EstadoModel, FornecedorModel, OfertaModel
from app.infrastructure.seed import run_seed


def test_seed_populates_states_suppliers_logos_and_offers(tmp_path) -> None:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'seed.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    session_factory = create_session_factory(engine)

    run_seed(database_url)

    with session_factory() as session:
        estados_count = session.scalar(select(func.count()).select_from(EstadoModel))
        fornecedores_count = session.scalar(
            select(func.count()).select_from(FornecedorModel)
        )
        ofertas_count = session.scalar(select(func.count()).select_from(OfertaModel))

        assert estados_count == 4
        assert fornecedores_count == 4
        assert ofertas_count == 14

        fornecedor = session.get(FornecedorModel, 1)
        assert fornecedor is not None
        assert fornecedor.logo is not None
        assert fornecedor.logo.url == "https://cdn.example.com/logos/lumen.png"


def test_seed_is_idempotent_and_restores_seed_values(tmp_path) -> None:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'seed.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    session_factory = create_session_factory(engine)

    run_seed(database_url)

    with session_factory() as session:
        estado_sp = session.execute(
            select(EstadoModel).where(EstadoModel.sigla == "SP")
        ).scalar_one()
        estado_sp.tarifa_base_kwh = Decimal("0.99")

        fornecedor = session.get(FornecedorModel, 1)
        assert fornecedor is not None
        assert fornecedor.logo is not None
        fornecedor.logo.url = "https://cdn.example.com/logos/changed.png"

        oferta = session.execute(
            select(OfertaModel).where(
                OfertaModel.estado_id == 1,
                OfertaModel.fornecedor_id == 1,
                OfertaModel.solucao == "GD",
            )
        ).scalar_one()
        oferta.custo_kwh = Decimal("0.99")
        session.commit()

    run_seed(database_url)

    with session_factory() as session:
        estados_count = session.scalar(select(func.count()).select_from(EstadoModel))
        fornecedores_count = session.scalar(
            select(func.count()).select_from(FornecedorModel)
        )
        ofertas_count = session.scalar(select(func.count()).select_from(OfertaModel))
        assert estados_count == 4
        assert fornecedores_count == 4
        assert ofertas_count == 14

        estado_sp = session.execute(
            select(EstadoModel).where(EstadoModel.sigla == "SP")
        ).scalar_one()
        assert estado_sp.tarifa_base_kwh == Decimal("0.62")

        fornecedor = session.get(FornecedorModel, 1)
        assert fornecedor is not None
        assert fornecedor.logo is not None
        assert fornecedor.logo.url == "https://cdn.example.com/logos/lumen.png"

        oferta = session.execute(
            select(OfertaModel).where(
                OfertaModel.estado_id == 1,
                OfertaModel.fornecedor_id == 1,
                OfertaModel.solucao == "GD",
            )
        ).scalar_one()
        assert oferta.custo_kwh == Decimal("0.46")
