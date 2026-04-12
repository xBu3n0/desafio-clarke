from abc import ABC, abstractmethod

from .search import (
    EstadoSearchRepository,
    FornecedorSearchRepository,
    OfertaSearchRepository,
)


class UnitOfWork(ABC):
    estados: EstadoSearchRepository
    fornecedores: FornecedorSearchRepository
    ofertas: OfertaSearchRepository

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is not None:
            self.rollback()
        self.close()

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError
