from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.application.dto import OfertaSearchDTO


class OfertaSearchRepository(ABC):
    @abstractmethod
    def list_by_estado_id(self, estado_id: int) -> Sequence[OfertaSearchDTO]:
        raise NotImplementedError
