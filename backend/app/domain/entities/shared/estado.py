from app.domain.base import DomainModel
from app.domain.value_objects import CustoKwh, EstadoId, NomeEstado, SiglaEstado


class Estado(DomainModel):
    id: EstadoId | None
    nome: NomeEstado
    sigla: SiglaEstado
    tarifa_base_kwh: CustoKwh
