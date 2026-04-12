from sqlalchemy import inspect

from app.infrastructure.database import (
    create_engine_from_url,
    create_schema,
    create_session_factory,
)


def test_database_schema_creates_expected_tables(tmp_path) -> None:
    engine = create_engine_from_url(f"sqlite+pysqlite:///{tmp_path / 'database.db'}")

    create_schema(engine)

    inspector = inspect(engine)
    assert set(inspector.get_table_names()) == {
        "estados",
        "fornecedores",
        "logos",
        "ofertas",
    }


def test_database_session_factory_creates_working_sessions(tmp_path) -> None:
    engine = create_engine_from_url(f"sqlite+pysqlite:///{tmp_path / 'database.db'}")
    create_schema(engine)
    session_factory = create_session_factory(engine)

    session = session_factory()
    try:
        assert session.is_active
    finally:
        session.close()
