from pydantic import field_validator
from pydantic_core import PydanticCustomError

from app.domain.value_objects.base import ValueObject


class LogoId(ValueObject):
    value: int

    @field_validator("value")
    @classmethod
    def validate_value(cls, value: int) -> int:
        if value <= 0:
            raise PydanticCustomError(
                "logo_id_gt_zero",
                "logo_id must be greater than 0",
            )
        return value


class UrlLogo(ValueObject):
    value: str

    @field_validator("value")
    @classmethod
    def validate_value(cls, value: str) -> str:
        if not value.strip():
            raise PydanticCustomError(
                "url_logo_not_blank",
                "url_logo must not be blank",
            )
        if value != value.strip():
            raise PydanticCustomError(
                "url_logo_trimmed",
                "url_logo must be trimmed",
            )
        return value
