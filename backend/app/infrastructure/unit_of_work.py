from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from app.application.ports import UnitOfWork
from app.domain.exceptions import DuplicateEntityError

from .repositories import (
    SqlAlchemyEstadoSearchRepository,
    SqlAlchemyFornecedorSearchRepository,
    SqlAlchemyOfertaSearchRepository,
)


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory
        self._session: Session | None = None

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self._session = self._session_factory()
        self.estados = SqlAlchemyEstadoSearchRepository(self._session)
        self.fornecedores = SqlAlchemyFornecedorSearchRepository(self._session)
        self.ofertas = SqlAlchemyOfertaSearchRepository(self._session)
        return self

    def commit(self) -> None:
        if self._session is None:
            return
        try:
            self._session.commit()
        except IntegrityError as exc:
            self._session.rollback()
            raise DuplicateEntityError(
                "database integrity constraint violated"
            ) from exc

    def rollback(self) -> None:
        if self._session is not None:
            self._session.rollback()

    def close(self) -> None:
        if self._session is not None:
            self._session.close()
            self._session = None
