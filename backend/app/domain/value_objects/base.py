from app.domain.base import DomainModel


class ValueObject(DomainModel):
    @classmethod
    def create(cls, value):
        return cls(value=value)
