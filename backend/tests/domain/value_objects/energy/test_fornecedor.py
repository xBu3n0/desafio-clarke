from decimal import Decimal

import pytest

from app.domain.exceptions import ValidationError
from app.domain.value_objects import (
    AvaliacaoMedia,
    AvaliacaoTotal,
    FornecedorId,
    NomeFornecedor,
    NumeroAvaliacoes,
    NumeroClientes,
)


def test_nome_fornecedor_keeps_a_clean_supplier_name() -> None:
    value_object = NomeFornecedor.create("Clarke Energia")

    assert value_object.value == "Clarke Energia"


def test_fornecedor_id_keeps_a_positive_identifier() -> None:
    value_object = FornecedorId.create(1)

    assert value_object.value == 1


def test_numero_clientes_keeps_a_non_negative_total() -> None:
    value_object = NumeroClientes.create(1200)

    assert value_object.value == 1200


def test_avaliacao_total_keeps_a_non_negative_total() -> None:
    value_object = AvaliacaoTotal.create(45)

    assert value_object.value == 45


def test_numero_avaliacoes_keeps_a_non_negative_total() -> None:
    value_object = NumeroAvaliacoes.create(5)

    assert value_object.value == 5


def test_avaliacao_media_keeps_a_valid_score() -> None:
    value_object = AvaliacaoMedia.create(Decimal("9.0"))

    assert value_object.value == Decimal("9.0")


@pytest.mark.parametrize(
    "raw_value",
    [
        "  Clarke Energia  ",
        "   ",
    ],
)
def test_nome_fornecedor_only_allows_clean_names(raw_value) -> None:
    with pytest.raises(ValidationError):
        NomeFornecedor.create(raw_value)


def test_fornecedor_id_requires_a_positive_identifier() -> None:
    with pytest.raises(ValidationError):
        FornecedorId.create(0)


@pytest.mark.parametrize(
    "raw_value",
    [
        -1,
        -10,
    ],
)
def test_numero_clientes_cannot_be_negative(raw_value) -> None:
    with pytest.raises(ValidationError):
        NumeroClientes.create(raw_value)


@pytest.mark.parametrize(
    "raw_value",
    [
        -1,
        -10,
    ],
)
def test_avaliacao_total_cannot_be_negative(raw_value) -> None:
    with pytest.raises(ValidationError):
        AvaliacaoTotal.create(raw_value)


@pytest.mark.parametrize(
    "raw_value",
    [
        -1,
        -10,
    ],
)
def test_numero_avaliacoes_cannot_be_negative(raw_value) -> None:
    with pytest.raises(ValidationError):
        NumeroAvaliacoes.create(raw_value)


@pytest.mark.parametrize(
    "raw_value",
    [
        Decimal("-0.1"),
        Decimal("10.5"),
    ],
)
def test_avaliacao_media_must_stay_within_the_score_scale(raw_value) -> None:
    with pytest.raises(ValidationError):
        AvaliacaoMedia.create(raw_value)
