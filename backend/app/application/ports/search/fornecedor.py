from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.application.dto import FornecedorSearchDTO


class FornecedorSearchRepository(ABC):
    @abstractmethod
    def list_by_ids(
        self,
        fornecedor_ids: Sequence[int],
    ) -> Sequence[FornecedorSearchDTO]:
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError
