from decimal import Decimal

from app.domain.entities import Fornecedor, Logo
from app.domain.value_objects import (
    AvaliacaoMedia,
    AvaliacaoTotal,
    FornecedorId,
    LogoId,
    NomeFornecedor,
    NumeroAvaliacoes,
    NumeroClientes,
    UrlLogo,
)


def test_fornecedor_can_be_created_with_a_complete_supplier_profile() -> None:
    fornecedor = Fornecedor(
        id=FornecedorId.create(5),
        nome=NomeFornecedor.create("Clarke Energia"),
        logo=Logo(
            id=LogoId.create(2),
            url=UrlLogo.create("https://example.com/logo.png"),
        ),
        numero_clientes=NumeroClientes.create(1200),
        avaliacao_total=AvaliacaoTotal.create(45),
        numero_avaliacoes=NumeroAvaliacoes.create(5),
        avaliacao_media=AvaliacaoMedia.create(Decimal("9.0")),
    )

    assert isinstance(fornecedor, Fornecedor)
    assert isinstance(fornecedor.id, FornecedorId)
    assert isinstance(fornecedor.nome, NomeFornecedor)
    assert isinstance(fornecedor.logo, Logo)
    assert isinstance(fornecedor.logo.id, LogoId)
    assert isinstance(fornecedor.logo.url, UrlLogo)
    assert isinstance(fornecedor.numero_clientes, NumeroClientes)
    assert isinstance(fornecedor.avaliacao_total, AvaliacaoTotal)
    assert isinstance(fornecedor.numero_avaliacoes, NumeroAvaliacoes)
    assert isinstance(fornecedor.avaliacao_media, AvaliacaoMedia)
