from dataclasses import dataclass
from decimal import Decimal

from app.domain.value_objects import Solucao


@dataclass(frozen=True, slots=True)
class LogoSearchDTO:
    id: int
    url: str


@dataclass(frozen=True, slots=True)
class FornecedorSearchDTO:
    id: int
    nome: str
    logo: LogoSearchDTO
    numero_clientes: int
    avaliacao_total: int
    numero_avaliacoes: int
    avaliacao_media: Decimal


@dataclass(frozen=True, slots=True)
class EstadoSearchDTO:
    id: int
    nome: str
    sigla: str
    tarifa_base_kwh: Decimal


@dataclass(frozen=True, slots=True)
class OfertaSearchDTO:
    id: int
    estado_id: int
    fornecedor_id: int
    solucao: Solucao
    custo_kwh: Decimal
