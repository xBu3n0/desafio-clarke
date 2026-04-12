import re

from pydantic import field_validator
from pydantic_core import PydanticCustomError

from app.domain.value_objects.base import ValueObject


class EstadoId(ValueObject):
    value: int

    @field_validator("value")
    @classmethod
    def validate_value(cls, value: int) -> int:
        if value <= 0:
            raise PydanticCustomError(
                "estado_id_gt_zero",
                "estado_id must be greater than 0",
            )
        return value


class NomeEstado(ValueObject):
    value: str

    @field_validator("value")
    @classmethod
    def validate_value(cls, value: str) -> str:
        if not value.strip():
            raise PydanticCustomError(
                "nome_estado_not_blank",
                "nome_estado must not be blank",
            )
        if value != value.strip():
            raise PydanticCustomError(
                "nome_estado_trimmed",
                "nome_estado must be trimmed",
            )
        return value


class SiglaEstado(ValueObject):
    value: str

    @field_validator("value")
    @classmethod
    def validate_value(cls, value: str) -> str:
        if not re.fullmatch(r"[A-Z]{2}", value):
            raise PydanticCustomError(
                "sigla_estado_format",
                "sigla_estado must contain exactly two letters",
            )
        return value
