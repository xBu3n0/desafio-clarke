from flask import Blueprint
from strawberry import Schema

from app.application.services import SearchQueryService

from .estado import register_estado_routes
from .graphql import register_graphql_routes
from .health import register_health_routes
from .swagger import register_swagger_routes

API_PREFIX = "/api/v1"


def create_api_blueprint(
    *,
    search_query_service: SearchQueryService,
    graphql_schema: Schema,
) -> Blueprint:
    blueprint = Blueprint("api", __name__, url_prefix=API_PREFIX)
    register_health_routes(blueprint)
    register_swagger_routes(blueprint)
    register_graphql_routes(
        blueprint,
        schema=graphql_schema,
    )
    register_estado_routes(
        blueprint,
        search_query_service=search_query_service,
    )
    return blueprint
