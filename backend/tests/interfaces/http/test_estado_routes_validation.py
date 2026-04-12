from app import create_app
from app.infrastructure.database import create_engine_from_url, create_schema


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
