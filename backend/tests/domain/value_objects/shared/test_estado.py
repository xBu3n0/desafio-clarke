import pytest

from app.domain.exceptions import ValidationError
from app.domain.value_objects import EstadoId, NomeEstado, SiglaEstado


def test_nome_estado_keeps_a_clean_state_name() -> None:
    value_object = NomeEstado.create("Sao Paulo")

    assert value_object.value == "Sao Paulo"


def test_sigla_estado_keeps_the_official_two_letter_code() -> None:
    value_object = SiglaEstado.create("SP")

    assert value_object.value == "SP"


def test_estado_id_keeps_a_positive_identifier() -> None:
    value_object = EstadoId.create(1)

    assert value_object.value == 1


@pytest.mark.parametrize(
    "raw_value",
    [
        "  Sao Paulo  ",
        "   ",
    ],
)
def test_nome_estado_only_allows_clean_names(raw_value) -> None:
    with pytest.raises(ValidationError):
        NomeEstado.create(raw_value)


def test_sigla_estado_requires_the_official_two_letter_code() -> None:
    with pytest.raises(ValidationError):
        SiglaEstado.create("sp")


def test_estado_id_requires_a_positive_identifier() -> None:
    with pytest.raises(ValidationError):
        EstadoId.create(-1)
