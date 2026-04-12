from app import create_app


def test_swagger_json_exposes_openapi_document() -> None:
    # Arrange
    app = create_app()
    client = app.test_client()

    # Act
    response = client.get("/api/v1/swagger.json")

    # Assert
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["openapi"] == "3.0.3"
    assert payload["info"]["title"] == "Clarke Energia API"
    assert "/health" in payload["paths"]
    assert "/graphql" in payload["paths"]
    assert "get" not in payload["paths"]["/graphql"]
    assert "post" in payload["paths"]["/graphql"]


def test_swagger_endpoint_renders_swagger_ui_html() -> None:
    # Arrange
    app = create_app()
    client = app.test_client()

    # Act
    response = client.get("/api/v1/swagger")

    # Assert
    assert response.status_code == 200
    content_type = response.headers.get("Content-Type", "")
    assert "text/html" in content_type
    body = response.get_data(as_text=True)
    assert "SwaggerUIBundle" in body
    assert "/api/v1/swagger.json" in body
