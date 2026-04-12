from pydantic import (
    BaseModel,
    ConfigDict,
)
from pydantic import (
    ValidationError as PydanticValidationError,
)

from .exceptions import ValidationError


class DomainModel(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)

    def __init__(self, **data):
        try:
            super().__init__(**data)
        except PydanticValidationError as exc:
            message = exc.errors()[0]["msg"]
            raise ValidationError(message) from exc
