from decimal import Decimal

from pydantic import field_validator
from pydantic_core import PydanticCustomError

from app.domain.value_objects.base import ValueObject


class FornecedorId(ValueObject):
    value: int

    @field_validator("value")
    @classmethod
    def validate_value(cls, value: int) -> int:
        if value <= 0:
            raise PydanticCustomError(
                "fornecedor_id_gt_zero",
                "fornecedor_id must be greater than 0",
            )
        return value


class NomeFornecedor(ValueObject):
    value: str

    @field_validator("value")
    @classmethod
    def validate_value(cls, value: str) -> str:
        if not value.strip():
            raise PydanticCustomError(
                "nome_fornecedor_not_blank",
                "nome_fornecedor must not be blank",
            )
        if value != value.strip():
            raise PydanticCustomError(
                "nome_fornecedor_trimmed",
                "nome_fornecedor must be trimmed",
            )
        return value


class NumeroClientes(ValueObject):
    value: int

    @field_validator("value")
    @classmethod
    def validate_value(cls, value: int) -> int:
        if value < 0:
            raise PydanticCustomError(
                "numero_clientes_min",
                "numero_clientes must be greater than or equal to 0",
            )
        return value


class AvaliacaoTotal(ValueObject):
    value: int

    @field_validator("value")
    @classmethod
    def validate_value(cls, value: int) -> int:
        if value < 0:
            raise PydanticCustomError(
                "avaliacao_total_min",
                "avaliacao_total must be greater than or equal to 0",
            )
        return value


class NumeroAvaliacoes(ValueObject):
    value: int

    @field_validator("value")
    @classmethod
    def validate_value(cls, value: int) -> int:
        if value < 0:
            raise PydanticCustomError(
                "numero_avaliacoes_min",
                "numero_avaliacoes must be greater than or equal to 0",
            )
        return value


class AvaliacaoMedia(ValueObject):
    value: Decimal

    @field_validator("value")
    @classmethod
    def validate_value(cls, value: Decimal):
        if value < Decimal("0.0") or value > Decimal("10.0"):
            raise PydanticCustomError(
                "avaliacao_media_range",
                "avaliacao_media must be between 0.0 and 10.0",
            )
        return value
