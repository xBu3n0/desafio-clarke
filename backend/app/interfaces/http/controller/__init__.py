from flask import Blueprint

from .estado import register_estado_routes
from .graphql import register_graphql_routes
from .health import register_health_routes

API_PREFIX = "/api/v1"


def create_api_blueprint() -> Blueprint:
    blueprint = Blueprint("api", __name__, url_prefix=API_PREFIX)
    register_health_routes(blueprint)
    register_graphql_routes(blueprint)
    register_estado_routes(blueprint)
    return blueprint
