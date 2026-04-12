from decimal import Decimal

from app.infrastructure.database import (
    create_engine_from_url,
    create_schema,
    create_session_factory,
)
from app.infrastructure.orm import FornecedorModel, LogoModel
from app.infrastructure.repositories.search import SqlAlchemyFornecedorSearchRepository


def make_fornecedor(
    *,
    fornecedor_id: int,
    nome: str,
    logo_path: str,
) -> FornecedorModel:
    return FornecedorModel(
        id=fornecedor_id,
        nome=nome,
        logo=LogoModel(
            id=fornecedor_id,
            url=logo_path,
        ),
        numero_clientes=1000 + fornecedor_id,
        avaliacao_total=50 + fornecedor_id,
        numero_avaliacoes=10 + fornecedor_id,
        avaliacao_media=Decimal("8.5"),
    )


def test_fornecedor_repository_lists_only_requested_suppliers(tmp_path) -> None:
    # Arrange
    engine = create_engine_from_url(
        f"sqlite+pysqlite:///{tmp_path / 'repositories.db'}"
    )
    create_schema(engine)
    session_factory = create_session_factory(engine)

    with session_factory() as session:
        session.add_all(
            [
                make_fornecedor(
                    fornecedor_id=1,
                    nome="Fornecedor A",
                    logo_path="https://example.com/a.png",
                ),
                make_fornecedor(
                    fornecedor_id=2,
                    nome="Fornecedor B",
                    logo_path="https://example.com/b.png",
                ),
                make_fornecedor(
                    fornecedor_id=3,
                    nome="Fornecedor C",
                    logo_path="https://example.com/c.png",
                ),
            ]
        )
        session.commit()

        repository = SqlAlchemyFornecedorSearchRepository(session)

        # Act
        fornecedores = repository.list_by_ids(
            [
                1,
                3,
            ]
        )

    # Assert
    assert [fornecedor.id for fornecedor in fornecedores] == [1, 3]
    assert [fornecedor.nome for fornecedor in fornecedores] == [
        "Fornecedor A",
        "Fornecedor C",
    ]
    assert [fornecedor.logo.url for fornecedor in fornecedores] == [
        "https://example.com/a.png",
        "https://example.com/c.png",
    ]


def test_fornecedor_repository_returns_total_count(tmp_path) -> None:
    # Arrange
    engine = create_engine_from_url(
        f"sqlite+pysqlite:///{tmp_path / 'repositories.db'}"
    )
    create_schema(engine)
    session_factory = create_session_factory(engine)

    with session_factory() as session:
        session.add_all(
            [
                make_fornecedor(
                    fornecedor_id=1,
                    nome="Fornecedor A",
                    logo_path="https://example.com/a.png",
                ),
                make_fornecedor(
                    fornecedor_id=2,
                    nome="Fornecedor B",
                    logo_path="https://example.com/b.png",
                ),
            ]
        )
        session.commit()

        repository = SqlAlchemyFornecedorSearchRepository(session)

        # Act
        total = repository.count()

    # Assert
    assert total == 2
