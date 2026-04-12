import pytest

from app.domain.exceptions import ValidationError
from app.domain.value_objects import OfertaId, Solucao


def test_solucao_accepts_a_supported_market_model() -> None:
    solucao = Solucao.create("Mercado Livre")

    assert solucao is Solucao.MERCADO_LIVRE


def test_oferta_id_keeps_a_positive_identifier() -> None:
    value_object = OfertaId.create(7)

    assert value_object.value == 7


def test_solucao_rejects_unknown_or_normalized_labels() -> None:
    with pytest.raises(ValidationError):
        Solucao.create(" gd ")


def test_oferta_id_requires_a_positive_identifier() -> None:
    with pytest.raises(ValidationError):
        OfertaId.create(0)
