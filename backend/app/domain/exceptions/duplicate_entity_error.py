from .domain_error import DomainError


class DuplicateEntityError(DomainError):
    """Raised when a unique business key already exists."""
