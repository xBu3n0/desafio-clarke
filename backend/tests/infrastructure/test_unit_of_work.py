import pytest

from app.domain.exceptions import DuplicateEntityError
from app.infrastructure.database import (
    create_engine_from_url,
    create_schema,
    create_session_factory,
)
from app.infrastructure.orm import EstadoModel, FornecedorModel, LogoModel, OfertaModel
from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork


def test_unit_of_work_exposes_search_repositories(tmp_path) -> None:
    # Arrange
    engine = create_engine_from_url(f"sqlite+pysqlite:///{tmp_path / 'uow.db'}")
    create_schema(engine)
    session_factory = create_session_factory(engine)

    # Act
    with SqlAlchemyUnitOfWork(session_factory) as uow:
        # Assert
        assert uow.estados is not None
        assert uow.fornecedores is not None
        assert uow.ofertas is not None


def test_unit_of_work_translates_integrity_errors_to_domain_errors(tmp_path) -> None:
    # Arrange
    engine = create_engine_from_url(f"sqlite+pysqlite:///{tmp_path / 'uow.db'}")
    create_schema(engine)
    session_factory = create_session_factory(engine)

    with session_factory() as session:
        session.add(
            EstadoModel(
                id=1,
                nome="Sao Paulo",
                sigla="SP",
                tarifa_base_kwh="0.52",
            )
        )
        session.add(
            FornecedorModel(
                id=1,
                nome="Fornecedor A",
                logo=LogoModel(id=1, url="https://example.com/a.png"),
                numero_clientes=1000,
                avaliacao_total=50,
                numero_avaliacoes=10,
                avaliacao_media="8.5",
            )
        )
        session.commit()

    # Act
    with pytest.raises(
        DuplicateEntityError,
        match="database integrity constraint violated",
    ):
        with SqlAlchemyUnitOfWork(session_factory) as uow:
            uow._session.add(
                OfertaModel(
                    id=1,
                    estado_id=1,
                    fornecedor_id=1,
                    solucao="GD",
                    custo_kwh="0.40",
                )
            )
            uow.commit()

            # Assert

            uow._session.add(
                OfertaModel(
                    id=2,
                    estado_id=1,
                    fornecedor_id=1,
                    solucao="GD",
                    custo_kwh="0.41",
                )
            )
            uow.commit()
