from dataclasses import dataclass
from decimal import Decimal

from app.domain.value_objects import Solucao

from .read_models import FornecedorSearchDTO


@dataclass(frozen=True, slots=True)
class OfertaComFornecedorSearchDTO:
    id: int
    estado_id: int
    fornecedor_id: int
    solucao: Solucao
    custo_kwh: Decimal
    fornecedor: FornecedorSearchDTO
