from decimal import Decimal

from app.domain.value_objects import Solucao
from app.infrastructure.database import (
    create_engine_from_url,
    create_schema,
    create_session_factory,
)
from app.infrastructure.orm import OfertaModel
from app.infrastructure.repositories.search import SqlAlchemyOfertaSearchRepository


def make_oferta(
    *,
    oferta_id: int,
    estado_id: int,
    fornecedor_id: int,
    solucao: Solucao,
    custo_kwh: str,
) -> OfertaModel:
    return OfertaModel(
        id=oferta_id,
        estado_id=estado_id,
        fornecedor_id=fornecedor_id,
        solucao=solucao,
        custo_kwh=Decimal(custo_kwh),
    )


def test_oferta_repository_lists_offers_for_a_state(tmp_path) -> None:
    engine = create_engine_from_url(
        f"sqlite+pysqlite:///{tmp_path / 'repositories.db'}"
    )
    create_schema(engine)
    session_factory = create_session_factory(engine)

    with session_factory() as session:
        session.add_all(
            [
                make_oferta(
                    oferta_id=1,
                    estado_id=1,
                    fornecedor_id=1,
                    solucao=Solucao.GD,
                    custo_kwh="0.40",
                ),
                make_oferta(
                    oferta_id=2,
                    estado_id=1,
                    fornecedor_id=2,
                    solucao=Solucao.MERCADO_LIVRE,
                    custo_kwh="0.45",
                ),
                make_oferta(
                    oferta_id=3,
                    estado_id=2,
                    fornecedor_id=3,
                    solucao=Solucao.GD,
                    custo_kwh="0.39",
                ),
            ]
        )
        session.commit()

        repository = SqlAlchemyOfertaSearchRepository(session)
        ofertas = repository.list_by_estado_id(1)

    assert [oferta.id for oferta in ofertas] == [1, 2]
    assert [oferta.solucao.value for oferta in ofertas] == ["GD", "Mercado Livre"]
