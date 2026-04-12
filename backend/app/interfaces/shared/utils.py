from decimal import Decimal, InvalidOperation


def format_decimal(value: Decimal, places: int) -> str:
    return f"{value:.{places}f}"


def parse_positive_int(value: int | str, field_name: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        msg = f"{field_name} must be an integer"
        raise ValueError(msg) from exc

    if parsed <= 0:
        msg = f"{field_name} must be greater than 0"
        raise ValueError(msg)
    return parsed


def parse_decimal(value: str, field_name: str) -> Decimal:
    try:
        return Decimal(value)
    except InvalidOperation as exc:
        msg = f"{field_name} must be a valid decimal"
        raise ValueError(msg) from exc
