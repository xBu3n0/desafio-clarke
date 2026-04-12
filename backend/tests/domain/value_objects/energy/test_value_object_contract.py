from decimal import Decimal

import pytest

from app.domain.value_objects import (
    AvaliacaoMedia,
    AvaliacaoTotal,
    ConsumoKwh,
    CustoKwh,
    EstadoId,
    FornecedorId,
    LogoId,
    NomeEstado,
    NomeFornecedor,
    NumeroAvaliacoes,
    NumeroClientes,
    OfertaId,
    SiglaEstado,
    UrlLogo,
)


@pytest.mark.parametrize(
    ("value_object_class", "raw_value"),
    [
        (EstadoId, 1),
        (NomeEstado, "Sao Paulo"),
        (SiglaEstado, "SP"),
        (FornecedorId, 1),
        (NomeFornecedor, "Clarke Energia"),
        (NumeroClientes, 10),
        (AvaliacaoTotal, 100),
        (NumeroAvaliacoes, 25),
        (AvaliacaoMedia, Decimal("8.5")),
        (LogoId, 1),
        (UrlLogo, "https://example.com/logo.png"),
        (OfertaId, 1),
        (CustoKwh, Decimal("0.52")),
        (ConsumoKwh, Decimal("350.00")),
    ],
)
def test_value_object_keeps_the_same_value_it_receives(
    value_object_class, raw_value
) -> None:
    value_object = value_object_class.create(raw_value)

    assert value_object.value == raw_value
