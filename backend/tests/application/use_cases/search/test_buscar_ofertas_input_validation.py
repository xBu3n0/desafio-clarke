from decimal import Decimal

import pytest

from app.application.dto.search import BuscarOfertasCommand
from app.domain.exceptions import ValidationError
from app.domain.value_objects import ConsumoKwh, SiglaEstado


def make_command(
    *,
    sigla_estado: str = "SP",
    consumo_kwh: str = "1000",
) -> BuscarOfertasCommand:
    return BuscarOfertasCommand(
        sigla_estado=SiglaEstado.create(sigla_estado),
        consumo_kwh=ConsumoKwh.create(Decimal(consumo_kwh)),
    )


def test_search_requires_a_valid_state_code() -> None:
    # Arrange
    # Act
    with pytest.raises(ValidationError):
        make_command(sigla_estado="sp")

    # Assert


def test_search_requires_a_positive_consumption() -> None:
    # Arrange
    # Act
    with pytest.raises(ValidationError):
        make_command(consumo_kwh="0")

    # Assert
