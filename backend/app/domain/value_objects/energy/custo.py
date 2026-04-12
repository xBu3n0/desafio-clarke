from decimal import Decimal

from pydantic import field_validator
from pydantic_core import PydanticCustomError

from app.domain.value_objects.base import ValueObject


class CustoKwh(ValueObject):
    value: Decimal

    @field_validator("value")
    @classmethod
    def validate_value(cls, value: Decimal):
        if value <= Decimal("0.00"):
            raise PydanticCustomError(
                "custo_kwh_gt_zero",
                "custo_kwh must be greater than 0.0",
            )
        return value


class ConsumoKwh(ValueObject):
    value: Decimal

    @field_validator("value")
    @classmethod
    def validate_value(cls, value: Decimal):
        if value <= Decimal("0.00"):
            raise PydanticCustomError(
                "consumo_kwh_gt_zero",
                "consumo_kwh must be greater than 0.0",
            )
        return value
