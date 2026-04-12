from app import create_app
from app.infrastructure.database import create_engine_from_url, create_schema
from app.infrastructure.seed import run_seed


def test_graphql_health_query_returns_ok(monkeypatch, tmp_path) -> None:
    # Arrange
    database_url = f"sqlite+pysqlite:///{tmp_path / 'graphql.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    monkeypatch.setenv("DATABASE_URL", database_url)

    app = create_app()
    client = app.test_client()

    # Act
    response = client.post(
        "/api/v1/graphql",
        json={"query": "query { health { status } }"},
    )

    # Assert
    assert response.status_code == 200
    assert response.get_json() == {"data": {"health": {"status": "ok"}}}


def test_graphql_can_query_offers_by_state_with_supplier_logo(
    monkeypatch,
    tmp_path,
) -> None:
    # Arrange
    database_url = f"sqlite+pysqlite:///{tmp_path / 'graphql.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    run_seed(database_url)
    monkeypatch.setenv("DATABASE_URL", database_url)

    app = create_app()
    client = app.test_client()

    # Act
    response = client.post(
        "/api/v1/graphql",
        json={
            "query": """
                query ($estadoId: Int!, $page: Int!, $perPage: Int!) {
                  ofertasPorEstado(
                    estadoId: $estadoId
                    page: $page
                    perPage: $perPage
                  ) {
                    id
                    estadoId
                    fornecedorId
                    solucao
                    custoKwh
                    fornecedor {
                      id
                      nome
                      avaliacaoMedia
                      logo {
                        id
                        url
                      }
                    }
                  }
                }
            """,
            "variables": {
                "estadoId": 1,
                "page": 1,
                "perPage": 2,
            },
        },
    )

    # Assert
    assert response.status_code == 200
    payload = response.get_json()
    assert "errors" not in payload
    items = payload["data"]["ofertasPorEstado"]
    assert len(items) == 2
    assert "fornecedor" in items[0]
    assert "logo" in items[0]["fornecedor"]


def test_graphql_mutations_are_not_supported_yet(monkeypatch, tmp_path) -> None:
    # Arrange
    database_url = f"sqlite+pysqlite:///{tmp_path / 'graphql.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    monkeypatch.setenv("DATABASE_URL", database_url)

    app = create_app()
    client = app.test_client()

    # Act
    response = client.post(
        "/api/v1/graphql",
        json={
            "query": """
                mutation {
                  createEstado(nome: "Bahia", sigla: "BA", tarifaBaseKwh: "0.55") {
                    id
                  }
                }
            """
        },
    )

    # Assert
    assert response.status_code == 400
    payload = response.get_json()
    assert "errors" in payload
    assert "mutation" in payload["errors"][0]["message"].lower()


def test_graphql_requires_query_field(monkeypatch, tmp_path) -> None:
    # Arrange
    database_url = f"sqlite+pysqlite:///{tmp_path / 'graphql.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    monkeypatch.setenv("DATABASE_URL", database_url)

    app = create_app()
    client = app.test_client()

    # Act
    response = client.post("/api/v1/graphql", json={})

    # Assert
    assert response.status_code == 400
    assert response.get_json() == {"errors": [{"message": "query is required"}]}
