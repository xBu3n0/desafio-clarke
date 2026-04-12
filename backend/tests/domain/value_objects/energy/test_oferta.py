import pytest

from app.domain.exceptions import ValidationError
from app.domain.value_objects import OfertaId, Solucao


def test_solucao_accepts_a_supported_market_model() -> None:
    # Arrange
    # Act
    solucao = Solucao.create("Mercado Livre")

    # Assert
    assert solucao is Solucao.MERCADO_LIVRE


def test_oferta_id_keeps_a_positive_identifier() -> None:
    # Arrange
    # Act
    value_object = OfertaId.create(7)

    # Assert
    assert value_object.value == 7


def test_solucao_rejects_unknown_or_normalized_labels() -> None:
    # Arrange
    # Act
    with pytest.raises(ValidationError):
        Solucao.create(" gd ")

    # Assert


def test_oferta_id_requires_a_positive_identifier() -> None:
    # Arrange
    # Act
    with pytest.raises(ValidationError):
        OfertaId.create(0)

    # Assert
