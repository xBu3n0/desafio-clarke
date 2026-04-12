from app import create_app
from app.infrastructure.database import create_engine_from_url, create_schema


def test_health_endpoint_confirms_the_api_is_alive() -> None:
    # Arrange
    app = create_app()
    client = app.test_client()

    # Act
    response = client.get("/api/v1/health")

    # Assert
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_metrics_endpoint_exposes_prometheus_metrics() -> None:
    # Arrange
    app = create_app()
    client = app.test_client()

    # Act
    response = client.get("/metrics")

    # Assert
    assert response.status_code == 200
    content_type = response.headers.get("Content-Type", "")
    assert "text/plain" in content_type
    payload = response.get_data(as_text=True)
    assert "# HELP" in payload
    assert "# TYPE" in payload
    assert "flask_info" in payload
    assert "flask_request_status_total" in payload
    assert "flask_request_duration_seconds_sum" in payload


def test_metrics_endpoint_includes_estado_route_requests(monkeypatch, tmp_path) -> None:
    # Arrange
    database_url = f"sqlite+pysqlite:///{tmp_path / 'http.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    monkeypatch.setenv("DATABASE_URL", database_url)
    app = create_app()
    client = app.test_client()

    # Act
    estado_response = client.get("/api/v1/estados")

    # Act
    metrics_response = client.get("/metrics")

    # Assert
    assert estado_response.status_code == 200
    assert metrics_response.status_code == 200
    payload = metrics_response.get_data(as_text=True)
    assert "clarke_http_requests_total" in payload
    assert 'path="/api/v1/estados"' in payload
    assert 'app_name="flask-monitoring"' in payload
    assert 'endpoint="/api/v1/estados"' in payload
