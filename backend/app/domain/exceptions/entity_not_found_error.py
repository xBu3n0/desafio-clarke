from .domain_error import DomainError


class EntityNotFoundError(DomainError):
    """Raised when an entity required by a use case does not exist."""
