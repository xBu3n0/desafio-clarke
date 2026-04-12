from enum import Enum

from pydantic import field_validator
from pydantic_core import PydanticCustomError

from app.domain.exceptions import ValidationError
from app.domain.value_objects.base import ValueObject


class OfertaId(ValueObject):
    value: int

    @field_validator("value")
    @classmethod
    def validate_value(cls, value: int) -> int:
        if value <= 0:
            raise PydanticCustomError(
                "oferta_id_gt_zero",
                "oferta_id must be greater than 0",
            )
        return value


class Solucao(str, Enum):
    GD = "GD"
    MERCADO_LIVRE = "Mercado Livre"

    @classmethod
    def create(cls, value: str) -> "Solucao":
        return cls.from_value(value)

    @classmethod
    def from_value(cls, value: str) -> "Solucao":
        for member in cls:
            if member.value == value:
                return member
        raise ValidationError("solucao must be 'GD' or 'Mercado Livre'")
