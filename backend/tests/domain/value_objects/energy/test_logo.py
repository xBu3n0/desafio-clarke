import pytest

from app.domain.exceptions import ValidationError
from app.domain.value_objects import LogoId, UrlLogo


def test_url_logo_keeps_a_ready_to_use_logo_address() -> None:
    value_object = UrlLogo.create("https://example.com/logo.png")

    assert value_object.value == "https://example.com/logo.png"


def test_logo_id_keeps_a_positive_identifier() -> None:
    value_object = LogoId.create(3)

    assert value_object.value == 3


@pytest.mark.parametrize(
    "raw_value",
    [
        "   ",
        " https://example.com/logo.png ",
    ],
)
def test_url_logo_only_allows_ready_to_use_addresses(raw_value) -> None:
    with pytest.raises(ValidationError):
        UrlLogo.create(raw_value)


def test_logo_id_requires_a_positive_identifier() -> None:
    with pytest.raises(ValidationError):
        LogoId.create(0)
