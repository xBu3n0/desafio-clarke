from decimal import Decimal

from app.domain.entities import Oferta
from app.domain.value_objects import (
    CustoKwh,
    EstadoId,
    FornecedorId,
    OfertaId,
    Solucao,
)


def test_oferta_can_link_a_supplier_to_a_state_solution() -> None:
    oferta = Oferta(
        id=OfertaId.create(7),
        estado_id=EstadoId.create(3),
        fornecedor_id=FornecedorId.create(10),
        solucao=Solucao.create("GD"),
        custo_kwh=CustoKwh.create(Decimal("0.41")),
    )

    assert isinstance(oferta, Oferta)
    assert isinstance(oferta.id, OfertaId)
    assert isinstance(oferta.estado_id, EstadoId)
    assert isinstance(oferta.fornecedor_id, FornecedorId)
    assert isinstance(oferta.solucao, Solucao)
    assert isinstance(oferta.custo_kwh, CustoKwh)
