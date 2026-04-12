from .domain_error import DomainError


class ValidationError(DomainError):
    """Raised when a value object or entity violates a business rule."""
