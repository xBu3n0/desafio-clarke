from strawberry import Schema
from strawberry.schema.config import StrawberryConfig

from .energy.mutation import build_mutation_type
from .energy.query import build_query_type


def build_schema() -> Schema:
    return Schema(
        query=build_query_type(),
        mutation=build_mutation_type(),
        config=StrawberryConfig(auto_camel_case=True),
    )
