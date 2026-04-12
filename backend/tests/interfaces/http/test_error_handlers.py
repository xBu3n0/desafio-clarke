from flask import abort

from app import create_app
from app.domain.exceptions import (
    DomainError,
    DuplicateEntityError,
    EntityNotFoundError,
    ValidationError,
)


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
