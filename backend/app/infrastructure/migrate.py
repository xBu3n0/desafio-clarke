import os
from pathlib import Path

from alembic import command
from alembic.config import Config


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        msg = "DATABASE_URL is required to run migrations"
        raise RuntimeError(msg)
    return database_url


def get_alembic_config(database_url: str) -> Config:
    backend_root = Path(__file__).resolve().parents[2]
    config = Config(str(backend_root / "alembic.ini"))
    config.set_main_option("script_location", str(backend_root / "alembic"))
    config.set_main_option("sqlalchemy.url", database_url)
    return config


def run_migrations(database_url: str, revision: str = "head") -> None:
    command.upgrade(get_alembic_config(database_url), revision)


def main() -> None:
    run_migrations(get_database_url())


if __name__ == "__main__":
    main()
