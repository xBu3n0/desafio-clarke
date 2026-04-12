from app.domain.base import DomainModel
from app.domain.entities.energy.logo import Logo
from app.domain.value_objects import (
    AvaliacaoMedia,
    AvaliacaoTotal,
    FornecedorId,
    NomeFornecedor,
    NumeroAvaliacoes,
    NumeroClientes,
)


class Fornecedor(DomainModel):
    id: FornecedorId | None
    nome: NomeFornecedor
    logo: Logo
    numero_clientes: NumeroClientes
    avaliacao_total: AvaliacaoTotal
    numero_avaliacoes: NumeroAvaliacoes
    avaliacao_media: AvaliacaoMedia
