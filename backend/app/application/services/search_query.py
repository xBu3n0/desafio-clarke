from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.application.dto import EstadoSearchDTO, OfertaComFornecedorSearchDTO


class SearchQueryService(ABC):
    @abstractmethod
    def list_estados(self) -> Sequence[EstadoSearchDTO]:
        raise NotImplementedError

    @abstractmethod
    def get_estado(self, estado_id: int) -> EstadoSearchDTO | None:
        raise NotImplementedError

    @abstractmethod
    def list_ofertas_by_estado(
        self,
        *,
        estado_id: int,
        page: int,
        per_page: int,
    ) -> tuple[int, Sequence[OfertaComFornecedorSearchDTO]]:
        raise NotImplementedError

    @abstractmethod
    def fornecedores_count(self) -> int:
        raise NotImplementedError
