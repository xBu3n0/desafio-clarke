from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.application.dto import EstadoSearchDTO


class EstadoSearchRepository(ABC):
    @abstractmethod
    def get_by_sigla(self, sigla: str) -> EstadoSearchDTO | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, estado_id: int) -> EstadoSearchDTO | None:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> Sequence[EstadoSearchDTO]:
        raise NotImplementedError
