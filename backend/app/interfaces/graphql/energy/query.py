import strawberry

from app.domain.exceptions import EntityNotFoundError

from .common import (
    create_uow,
    list_ofertas_by_estado,
    to_estado_type,
    validate_estado_id,
)
from .types import EstadoType, HealthStatusType, OfertaType


def build_query_type():
    @strawberry.type
    class Query:
        @strawberry.field
        def health(self) -> HealthStatusType:
            return HealthStatusType(status="ok")

        @strawberry.field
        def estados(self) -> list[EstadoType]:
            with create_uow() as uow:
                estados = list(uow.estados.list_all())
            return [to_estado_type(estado) for estado in estados]

        @strawberry.field
        def ofertas_por_estado(
            self,
            estado_id: int,
            page: int = 1,
            per_page: int = 10,
        ) -> list[OfertaType]:
            _, ofertas = list_ofertas_by_estado(
                estado_id=estado_id,
                page=page,
                per_page=per_page,
            )
            return ofertas

        @strawberry.field
        def estado(self, estado_id: int) -> EstadoType:
            validated_estado_id = validate_estado_id(estado_id)
            with create_uow() as uow:
                estado = uow.estados.get_by_id(validated_estado_id)
            if estado is None:
                raise EntityNotFoundError("estado was not found")
            return to_estado_type(estado)

        @strawberry.field
        def fornecedores_count(self) -> int:
            with create_uow() as uow:
                return uow.fornecedores.count()

    return Query
