from app import create_app
from app.domain.value_objects import Solucao
from app.infrastructure.database import (
    create_engine_from_url,
    create_schema,
    create_session_factory,
)
from app.infrastructure.orm import EstadoModel, FornecedorModel, LogoModel, OfertaModel


def _seed_estado_offers_data(database_url: str) -> None:
    engine = create_engine_from_url(database_url)
    session_factory = create_session_factory(engine)

    with session_factory() as session:
        session.add(
            EstadoModel(
                id=1,
                nome="Sao Paulo",
                sigla="SP",
                tarifa_base_kwh="0.62",
            )
        )
        session.add_all(
            [
                FornecedorModel(
                    id=1,
                    nome="Fornecedor A",
                    logo=LogoModel(id=1, url="https://example.com/a.png"),
                    numero_clientes=1000,
                    avaliacao_total=50,
                    numero_avaliacoes=10,
                    avaliacao_media="8.5",
                ),
                FornecedorModel(
                    id=2,
                    nome="Fornecedor B",
                    logo=LogoModel(id=2, url="https://example.com/b.png"),
                    numero_clientes=1100,
                    avaliacao_total=60,
                    numero_avaliacoes=12,
                    avaliacao_media="8.7",
                ),
                FornecedorModel(
                    id=3,
                    nome="Fornecedor C",
                    logo=LogoModel(id=3, url="https://example.com/c.png"),
                    numero_clientes=1200,
                    avaliacao_total=70,
                    numero_avaliacoes=14,
                    avaliacao_media="8.9",
                ),
            ]
        )
        session.add_all(
            [
                OfertaModel(
                    id=1,
                    estado_id=1,
                    fornecedor_id=1,
                    solucao=Solucao.GD,
                    custo_kwh="0.46",
                ),
                OfertaModel(
                    id=2,
                    estado_id=1,
                    fornecedor_id=1,
                    solucao=Solucao.MERCADO_LIVRE,
                    custo_kwh="0.44",
                ),
                OfertaModel(
                    id=3,
                    estado_id=1,
                    fornecedor_id=2,
                    solucao=Solucao.GD,
                    custo_kwh="0.47",
                ),
                OfertaModel(
                    id=4,
                    estado_id=1,
                    fornecedor_id=2,
                    solucao=Solucao.MERCADO_LIVRE,
                    custo_kwh="0.45",
                ),
                OfertaModel(
                    id=5,
                    estado_id=1,
                    fornecedor_id=3,
                    solucao=Solucao.MERCADO_LIVRE,
                    custo_kwh="0.43",
                ),
            ]
        )
        session.commit()


def test_estado_endpoint_lists_paginated_offers_with_supplier_and_logo(
    monkeypatch,
    tmp_path,
) -> None:
    # Arrange
    database_url = f"sqlite+pysqlite:///{tmp_path / 'http.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    _seed_estado_offers_data(database_url)
    monkeypatch.setenv("DATABASE_URL", database_url)

    app = create_app()
    client = app.test_client()

    # Act
    response = client.get("/api/v1/estados/1?page=1&per_page=2")

    # Assert
    assert response.status_code == 200
    assert response.headers["X-Estado-Id"] == "1"
    assert response.headers["X-Page"] == "1"
    assert response.headers["X-Per-Page"] == "2"
    assert response.headers["X-Total-Count"] == "5"
    payload = response.get_json()
    assert isinstance(payload, list)
    assert len(payload) == 2

    first_item = payload[0]
    assert first_item["estadoId"] == 1
    assert first_item["solucao"] in {"GD", "Mercado Livre"}
    assert isinstance(first_item["fornecedor"], dict)
    assert isinstance(first_item["fornecedor"]["logo"], dict)
    assert "url" in first_item["fornecedor"]["logo"]


def test_estados_endpoint_lists_all_states_without_pagination(
    monkeypatch,
    tmp_path,
) -> None:
    # Arrange
    database_url = f"sqlite+pysqlite:///{tmp_path / 'http.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    session_factory = create_session_factory(engine)
    with session_factory() as session:
        session.add_all(
            [
                EstadoModel(
                    id=10,
                    nome="Bahia",
                    sigla="BA",
                    tarifa_base_kwh="0.55",
                ),
                EstadoModel(
                    id=11,
                    nome="Acre",
                    sigla="AC",
                    tarifa_base_kwh="0.61",
                ),
                EstadoModel(
                    id=12,
                    nome="Ceara",
                    sigla="CE",
                    tarifa_base_kwh="0.58",
                ),
            ]
        )
        session.commit()
    monkeypatch.setenv("DATABASE_URL", database_url)

    app = create_app()
    client = app.test_client()

    # Act
    response = client.get("/api/v1/estados")

    # Assert
    assert response.status_code == 200
    payload = response.get_json()
    assert isinstance(payload, list)
    assert len(payload) == 3
    assert payload[0] == {
        "id": 11,
        "nome": "Acre",
        "sigla": "AC",
        "tarifaBaseKwh": "0.61",
    }
    assert payload[2] == {
        "id": 12,
        "nome": "Ceara",
        "sigla": "CE",
        "tarifaBaseKwh": "0.58",
    }
