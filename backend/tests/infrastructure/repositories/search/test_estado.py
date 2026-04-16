from app.infrastructure.database import (
    create_engine_from_url,
    create_schema,
    create_session_factory,
)
from app.infrastructure.orm import EstadoModel
from app.infrastructure.repositories.search import SqlAlchemyEstadoSearchRepository


def test_estado_repository_finds_a_state_by_code(tmp_path) -> None:
    # Arrange
    engine = create_engine_from_url(
        f"sqlite+pysqlite:///{tmp_path / 'repositories.db'}"
    )
    create_schema(engine)
    session_factory = create_session_factory(engine)

    with session_factory() as session:
        session.add_all(
            [
                EstadoModel(
                    id=1,
                    nome="Sao Paulo",
                    sigla="SP",
                    tarifa_base_kwh="0.52",
                ),
                EstadoModel(
                    id=2,
                    nome="Parana",
                    sigla="PR",
                    tarifa_base_kwh="0.49",
                ),
            ]
        )
        session.commit()

        repository = SqlAlchemyEstadoSearchRepository(session)

        # Act
        estado = repository.get_by_sigla("SP")

    # Assert
    assert estado is not None
    assert estado.sigla == "SP"
    assert estado.nome == "Sao Paulo"


def test_estado_repository_can_get_by_id_and_list_all(tmp_path) -> None:
    # Arrange
    engine = create_engine_from_url(
        f"sqlite+pysqlite:///{tmp_path / 'repositories.db'}"
    )
    create_schema(engine)
    session_factory = create_session_factory(engine)

    with session_factory() as session:
        session.add_all(
            [
                EstadoModel(
                    id=1,
                    nome="Sao Paulo",
                    sigla="SP",
                    tarifa_base_kwh="0.52",
                ),
                EstadoModel(
                    id=2,
                    nome="Parana",
                    sigla="PR",
                    tarifa_base_kwh="0.49",
                ),
            ]
        )
        session.commit()

        repository = SqlAlchemyEstadoSearchRepository(session)

        # Act
        estado = repository.get_by_id(2)

        # Act
        estados = repository.list_all()

    # Assert
    assert estado is not None
    assert estado.nome == "Parana"
    assert [item.nome for item in estados] == ["Parana", "Sao Paulo"]
