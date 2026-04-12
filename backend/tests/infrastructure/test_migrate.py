from sqlalchemy import inspect

from app.infrastructure.database import create_engine_from_url
from app.infrastructure.migrate import main


def test_migration_creates_schema_from_database_url(tmp_path, monkeypatch) -> None:
    # Arrange
    database_path = tmp_path / "migration.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+pysqlite:///{database_path}")

    # Act
    main()

    # Assert
    engine = create_engine_from_url(f"sqlite+pysqlite:///{database_path}")
    inspector = inspect(engine)
    assert set(inspector.get_table_names()) == {
        "alembic_version",
        "estados",
        "fornecedores",
        "logos",
        "ofertas",
    }
