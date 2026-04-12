from app.domain.base import DomainModel
from app.domain.value_objects import (
    CustoKwh,
    EstadoId,
    FornecedorId,
    OfertaId,
    Solucao,
)


class Oferta(DomainModel):
    id: OfertaId | None
    estado_id: EstadoId
    fornecedor_id: FornecedorId
    solucao: Solucao
    custo_kwh: CustoKwh
