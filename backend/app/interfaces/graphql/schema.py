from strawberry import Schema
from strawberry.schema.config import StrawberryConfig

from app.application.services import SearchQueryService

from .energy.mutation import build_mutation_type
from .energy.query import build_query_type


def build_schema(search_query_service: SearchQueryService) -> Schema:
    return Schema(
        query=build_query_type(search_query_service),
        mutation=build_mutation_type(),
        config=StrawberryConfig(auto_camel_case=True),
    )
