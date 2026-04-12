from app import create_app
from app.infrastructure.database import create_engine_from_url, create_schema
from app.infrastructure.seed import run_seed


def test_graphql_health_query_returns_ok(monkeypatch, tmp_path) -> None:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'graphql.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    monkeypatch.setenv("DATABASE_URL", database_url)

    app = create_app()
    client = app.test_client()
    response = client.post(
        "/api/v1/graphql",
        json={"query": "query { health { status } }"},
    )

    assert response.status_code == 200
    assert response.get_json() == {"data": {"health": {"status": "ok"}}}


def test_graphql_can_query_offers_by_state_with_supplier_logo(
    monkeypatch,
    tmp_path,
) -> None:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'graphql.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    run_seed(database_url)
    monkeypatch.setenv("DATABASE_URL", database_url)

    app = create_app()
    client = app.test_client()
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

    assert response.status_code == 200
    payload = response.get_json()
    assert "errors" not in payload
    items = payload["data"]["ofertasPorEstado"]
    assert len(items) == 2
    assert "fornecedor" in items[0]
    assert "logo" in items[0]["fornecedor"]


def test_graphql_can_create_estado_fornecedor_and_oferta(
    monkeypatch,
    tmp_path,
) -> None:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'graphql.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    monkeypatch.setenv("DATABASE_URL", database_url)

    app = create_app()
    client = app.test_client()

    create_estado_response = client.post(
        "/api/v1/graphql",
        json={
            "query": """
                mutation {
                  createEstado(nome: "Bahia", sigla: "BA", tarifaBaseKwh: "0.55") {
                    id
                    nome
                    sigla
                  }
                }
            """
        },
    )
    assert create_estado_response.status_code == 200
    estado_id = create_estado_response.get_json()["data"]["createEstado"]["id"]

    create_fornecedor_response = client.post(
        "/api/v1/graphql",
        json={
            "query": """
                mutation {
                  createFornecedor(
                    nome: "Nova Energia"
                    logoUrl: "https://example.com/nova.png"
                    numeroClientes: 100
                    avaliacaoTotal: 80
                    numeroAvaliacoes: 10
                    avaliacaoMedia: "8.0"
                  ) {
                    id
                    nome
                    logo { id url }
                  }
                }
            """
        },
    )
    assert create_fornecedor_response.status_code == 200
    fornecedor_id = create_fornecedor_response.get_json()["data"]["createFornecedor"][
        "id"
    ]

    create_oferta_response = client.post(
        "/api/v1/graphql",
        json={
            "query": """
                mutation ($estadoId: Int!, $fornecedorId: Int!) {
                  createOferta(
                    estadoId: $estadoId
                    fornecedorId: $fornecedorId
                    solucao: "GD"
                    custoKwh: "0.40"
                  ) {
                    id
                    estadoId
                    fornecedorId
                    solucao
                    fornecedor { nome logo { url } }
                  }
                }
            """,
            "variables": {
                "estadoId": estado_id,
                "fornecedorId": fornecedor_id,
            },
        },
    )

    assert create_oferta_response.status_code == 200
    oferta_payload = create_oferta_response.get_json()["data"]["createOferta"]
    assert oferta_payload["estadoId"] == estado_id
    assert oferta_payload["fornecedorId"] == fornecedor_id
    assert oferta_payload["solucao"] == "GD"


def test_graphql_requires_query_field(monkeypatch, tmp_path) -> None:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'graphql.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    monkeypatch.setenv("DATABASE_URL", database_url)

    app = create_app()
    client = app.test_client()

    response = client.post("/api/v1/graphql", json={})

    assert response.status_code == 400
    assert response.get_json() == {"errors": [{"message": "query is required"}]}


def test_graphql_validates_create_estado_variables_with_value_objects(
    monkeypatch,
    tmp_path,
) -> None:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'graphql.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    monkeypatch.setenv("DATABASE_URL", database_url)

    app = create_app()
    client = app.test_client()
    response = client.post(
        "/api/v1/graphql",
        json={
            "query": """
                mutation {
                  createEstado(nome: "Bahia", sigla: "B", tarifaBaseKwh: "0.55") {
                    id
                  }
                }
            """
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "errors": [{"message": "sigla_estado must contain exactly two letters"}]
    }


def test_graphql_validates_create_oferta_variables_with_value_objects(
    monkeypatch,
    tmp_path,
) -> None:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'graphql.db'}"
    engine = create_engine_from_url(database_url)
    create_schema(engine)
    monkeypatch.setenv("DATABASE_URL", database_url)

    app = create_app()
    client = app.test_client()
    response = client.post(
        "/api/v1/graphql",
        json={
            "query": """
                mutation ($estadoId: Int!, $fornecedorId: Int!) {
                  createOferta(
                    estadoId: $estadoId
                    fornecedorId: $fornecedorId
                    solucao: "GD"
                    custoKwh: "0.40"
                  ) {
                    id
                  }
                }
            """,
            "variables": {
                "estadoId": 0,
                "fornecedorId": 1,
            },
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "errors": [{"message": "estado_id must be greater than 0"}]
    }
