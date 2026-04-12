from app.domain.entities import Logo
from app.domain.value_objects import LogoId, UrlLogo


def test_logo_can_be_created_with_a_valid_logo_reference() -> None:
    # Arrange
    # Act
    logo = Logo(id=LogoId.create(3), url=UrlLogo.create("https://example.com/logo.svg"))

    # Assert
    assert isinstance(logo, Logo)
