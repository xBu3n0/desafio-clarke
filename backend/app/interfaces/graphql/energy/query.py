import strawberry

from app.application.services import SearchQueryService
from app.domain.exceptions import EntityNotFoundError
from app.interfaces.shared import parse_positive_int

from .common import (
    to_estado_type,
    to_oferta_type,
    validate_estado_id,
)
from .types import EstadoType, HealthStatusType, OfertaType


def build_query_type(search_query_service: SearchQueryService):
    @strawberry.type
    class Query:
        @strawberry.field
        def health(self) -> HealthStatusType:
            return HealthStatusType(status="ok")

        @strawberry.field
        def estados(self) -> list[EstadoType]:
            estados = list(search_query_service.list_estados())
            return [to_estado_type(estado) for estado in estados]

        @strawberry.field
        def ofertas_por_estado(
            self,
            estado_id: int,
            page: int = 1,
            per_page: int = 10,
        ) -> list[OfertaType]:
            validated_estado_id = validate_estado_id(estado_id)
            validated_page = parse_positive_int(page, "page")
            validated_per_page = parse_positive_int(per_page, "per_page")

            _, ofertas = search_query_service.list_ofertas_by_estado(
                estado_id=validated_estado_id,
                page=validated_page,
                per_page=validated_per_page,
            )
            return [to_oferta_type(oferta) for oferta in ofertas]

        @strawberry.field
        def estado(self, estado_id: int) -> EstadoType:
            validated_estado_id = validate_estado_id(estado_id)
            estado = search_query_service.get_estado(validated_estado_id)
            if estado is None:
                raise EntityNotFoundError("estado was not found")
            return to_estado_type(estado)

        @strawberry.field
        def fornecedores_count(self) -> int:
            return search_query_service.fornecedores_count()

    return Query
