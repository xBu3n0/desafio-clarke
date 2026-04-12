from flask import abort

from app import create_app
from app.domain.exceptions import (
    DomainError,
    DuplicateEntityError,
    EntityNotFoundError,
    ValidationError,
)
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


def test_health_endpoint_confirms_the_api_is_alive() -> None:
    # Arrange
    app = create_app()
    client = app.test_client()

    # Act
    response = client.get("/api/v1/health")

    # Assert
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_invalid_requests_are_reported_as_unprocessable_entities() -> None:
    # Arrange
    app = create_app()

    @app.get("/validation-error")
    def validation_error():
        raise ValidationError("invalid payload")

    client = app.test_client()

    # Act
    response = client.get("/validation-error")

    # Assert
    assert response.status_code == 422
    assert response.get_json() == {"error": "invalid payload"}


def test_missing_entities_are_reported_as_not_found() -> None:
    # Arrange
    app = create_app()

    @app.get("/entity-not-found")
    def entity_not_found():
        raise EntityNotFoundError("entity not found")

    client = app.test_client()

    # Act
    response = client.get("/entity-not-found")

    # Assert
    assert response.status_code == 404
    assert response.get_json() == {"error": "entity not found"}


def test_duplicate_entities_are_reported_as_conflicts() -> None:
    # Arrange
    app = create_app()

    @app.get("/duplicate-entity")
    def duplicate_entity():
        raise DuplicateEntityError("duplicate entity")

    client = app.test_client()

    # Act
    response = client.get("/duplicate-entity")

    # Assert
    assert response.status_code == 409
    assert response.get_json() == {"error": "duplicate entity"}


def test_missing_required_fields_are_reported_as_bad_requests() -> None:
    # Arrange
    app = create_app()

    @app.get("/missing-field")
    def missing_field():
        raise KeyError("name")

    client = app.test_client()

    # Act
    response = client.get("/missing-field")

    # Assert
    assert response.status_code == 400
    assert response.get_json() == {"error": "missing required field: name"}


def test_invalid_values_are_reported_as_bad_requests() -> None:
    # Arrange
    app = create_app()

    @app.get("/value-error")
    def value_error():
        raise ValueError("invalid value")

    client = app.test_client()

    # Act
    response = client.get("/value-error")

    # Assert
    assert response.status_code == 400
    assert response.get_json() == {"error": "invalid value"}


def test_domain_failures_are_reported_as_bad_requests() -> None:
    # Arrange
    app = create_app()

    @app.get("/domain-error")
    def domain_error():
        raise DomainError("domain failure")

    client = app.test_client()

    # Act
    response = client.get("/domain-error")

    # Assert
    assert response.status_code == 400
    assert response.get_json() == {"error": "domain failure"}


def test_http_exceptions_keep_their_original_status_code() -> None:
    # Arrange
    app = create_app()

    @app.get("/forbidden")
    def forbidden():
        abort(403, description="forbidden")

    client = app.test_client()

    # Act
    response = client.get("/forbidden")

    # Assert
    assert response.status_code == 403
    assert response.get_json() == {"error": "forbidden"}


def test_unexpected_failures_are_reported_as_internal_server_errors() -> None:
    # Arrange
    app = create_app()

    @app.get("/unexpected-error")
    def unexpected_error():
        raise RuntimeError("unexpected failure")

    client = app.test_client()

    # Act
    response = client.get("/unexpected-error")

    # Assert
    assert response.status_code == 500
    assert response.get_json() == {"error": "unexpected failure"}


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
    assert first_item["estado_id"] == 1
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
        "tarifa_base_kwh": "0.61",
    }
    assert payload[2] == {
        "id": 12,
        "nome": "Ceara",
        "sigla": "CE",
        "tarifa_base_kwh": "0.58",
    }


def test_estado_endpoint_returns_not_found_for_unknown_state(
    monkeypatch,
    tmp_path,
) -> None:
    # Arrange
    database_url = f"sqlite+pysqlite:///{tmp_path / 'http.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    monkeypatch.setenv("DATABASE_URL", database_url)

    app = create_app()
    client = app.test_client()

    # Act
    response = client.get("/api/v1/estados/999")

    # Assert
    assert response.status_code == 404
    assert response.get_json() == {"error": "estado was not found"}


def test_estado_endpoint_rejects_invalid_pagination_params(
    monkeypatch,
    tmp_path,
) -> None:
    # Arrange
    database_url = f"sqlite+pysqlite:///{tmp_path / 'http.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    monkeypatch.setenv("DATABASE_URL", database_url)

    app = create_app()
    client = app.test_client()

    # Act
    invalid_page_response = client.get("/api/v1/estados/1?page=0")

    # Act
    invalid_per_page_response = client.get("/api/v1/estados/1?per_page=abc")

    # Assert
    assert invalid_page_response.status_code == 400
    assert invalid_page_response.get_json() == {"error": "page must be greater than 0"}
    assert invalid_per_page_response.status_code == 400
    assert invalid_per_page_response.get_json() == {
        "error": "per_page must be an integer"
    }
