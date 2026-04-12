from decimal import Decimal

from app.domain.entities import Estado
from app.domain.value_objects import CustoKwh, EstadoId, NomeEstado, SiglaEstado


def test_estado_can_be_created_with_a_valid_state_profile() -> None:
    # Arrange
    # Act
    estado = Estado(
        id=EstadoId.create(1),
        nome=NomeEstado.create("Sao Paulo"),
        sigla=SiglaEstado.create("SP"),
        tarifa_base_kwh=CustoKwh.create(Decimal("0.52")),
    )

    # Assert
    assert isinstance(estado, Estado)
