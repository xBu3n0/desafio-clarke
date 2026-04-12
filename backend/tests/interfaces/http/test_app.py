from flask import abort

from app import create_app
from app.domain.exceptions import (
    DomainError,
    DuplicateEntityError,
    EntityNotFoundError,
    ValidationError,
)
from app.infrastructure.database import create_engine_from_url, create_schema
from app.infrastructure.seed import run_seed


def test_health_endpoint_confirms_the_api_is_alive() -> None:
    app = create_app()
    client = app.test_client()

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_invalid_requests_are_reported_as_unprocessable_entities() -> None:
    app = create_app()

    @app.get("/validation-error")
    def validation_error():
        raise ValidationError("invalid payload")

    client = app.test_client()
    response = client.get("/validation-error")

    assert response.status_code == 422
    assert response.get_json() == {"error": "invalid payload"}


def test_missing_entities_are_reported_as_not_found() -> None:
    app = create_app()

    @app.get("/entity-not-found")
    def entity_not_found():
        raise EntityNotFoundError("entity not found")

    client = app.test_client()
    response = client.get("/entity-not-found")

    assert response.status_code == 404
    assert response.get_json() == {"error": "entity not found"}


def test_duplicate_entities_are_reported_as_conflicts() -> None:
    app = create_app()

    @app.get("/duplicate-entity")
    def duplicate_entity():
        raise DuplicateEntityError("duplicate entity")

    client = app.test_client()
    response = client.get("/duplicate-entity")

    assert response.status_code == 409
    assert response.get_json() == {"error": "duplicate entity"}


def test_missing_required_fields_are_reported_as_bad_requests() -> None:
    app = create_app()

    @app.get("/missing-field")
    def missing_field():
        raise KeyError("name")

    client = app.test_client()
    response = client.get("/missing-field")

    assert response.status_code == 400
    assert response.get_json() == {"error": "missing required field: name"}


def test_invalid_values_are_reported_as_bad_requests() -> None:
    app = create_app()

    @app.get("/value-error")
    def value_error():
        raise ValueError("invalid value")

    client = app.test_client()
    response = client.get("/value-error")

    assert response.status_code == 400
    assert response.get_json() == {"error": "invalid value"}


def test_domain_failures_are_reported_as_bad_requests() -> None:
    app = create_app()

    @app.get("/domain-error")
    def domain_error():
        raise DomainError("domain failure")

    client = app.test_client()
    response = client.get("/domain-error")

    assert response.status_code == 400
    assert response.get_json() == {"error": "domain failure"}


def test_http_exceptions_keep_their_original_status_code() -> None:
    app = create_app()

    @app.get("/forbidden")
    def forbidden():
        abort(403, description="forbidden")

    client = app.test_client()
    response = client.get("/forbidden")

    assert response.status_code == 403
    assert response.get_json() == {"error": "forbidden"}


def test_unexpected_failures_are_reported_as_internal_server_errors() -> None:
    app = create_app()

    @app.get("/unexpected-error")
    def unexpected_error():
        raise RuntimeError("unexpected failure")

    client = app.test_client()
    response = client.get("/unexpected-error")

    assert response.status_code == 500
    assert response.get_json() == {"error": "unexpected failure"}


def test_estado_endpoint_lists_paginated_offers_with_supplier_and_logo(
    monkeypatch,
    tmp_path,
) -> None:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'http.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    run_seed(database_url)
    monkeypatch.setenv("DATABASE_URL", database_url)

    app = create_app()
    client = app.test_client()

    response = client.get("/api/v1/estados/1?page=1&per_page=2")

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


def test_estado_endpoint_returns_not_found_for_unknown_state(
    monkeypatch,
    tmp_path,
) -> None:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'http.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    monkeypatch.setenv("DATABASE_URL", database_url)

    app = create_app()
    client = app.test_client()

    response = client.get("/api/v1/estados/999")

    assert response.status_code == 404
    assert response.get_json() == {"error": "estado was not found"}


def test_estado_endpoint_rejects_invalid_pagination_params(
    monkeypatch,
    tmp_path,
) -> None:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'http.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    run_seed(database_url)
    monkeypatch.setenv("DATABASE_URL", database_url)

    app = create_app()
    client = app.test_client()

    invalid_page_response = client.get("/api/v1/estados/1?page=0")
    invalid_per_page_response = client.get("/api/v1/estados/1?per_page=abc")

    assert invalid_page_response.status_code == 400
    assert invalid_page_response.get_json() == {"error": "page must be greater than 0"}
    assert invalid_per_page_response.status_code == 400
    assert invalid_per_page_response.get_json() == {
        "error": "per_page must be an integer"
    }
