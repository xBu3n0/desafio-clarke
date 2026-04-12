from decimal import Decimal

import pytest

from app.domain.exceptions import ValidationError
from app.domain.value_objects import ConsumoKwh, CustoKwh


def test_custo_kwh_represents_a_valid_energy_price() -> None:
    value_object = CustoKwh.create(Decimal("0.52"))

    assert value_object.value == Decimal("0.52")


def test_consumo_kwh_represents_a_valid_consumption_amount() -> None:
    value_object = ConsumoKwh.create(Decimal("350.00"))

    assert value_object.value == Decimal("350.00")


@pytest.mark.parametrize(
    "raw_value",
    [
        Decimal("0.00"),
        Decimal("-0.01"),
    ],
)
def test_custo_kwh_does_not_allow_free_or_negative_prices(raw_value) -> None:
    with pytest.raises(ValidationError):
        CustoKwh.create(raw_value)


@pytest.mark.parametrize(
    "raw_value",
    [
        Decimal("0"),
        Decimal("-1"),
    ],
)
def test_consumo_kwh_does_not_allow_zero_or_negative_consumption(raw_value) -> None:
    with pytest.raises(ValidationError):
        ConsumoKwh.create(raw_value)
