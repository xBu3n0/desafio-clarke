from collections.abc import Callable

from flask import Blueprint
from sqlalchemy.orm import Session

from .estado import register_estado_routes
from .graphql import register_graphql_routes
from .health import register_health_routes

API_PREFIX = "/api/v1"


def create_api_blueprint(*, session_provider: Callable[[], Session]) -> Blueprint:
    blueprint = Blueprint("api", __name__, url_prefix=API_PREFIX)
    register_health_routes(blueprint)
    register_graphql_routes(blueprint)
    register_estado_routes(blueprint, session_provider=session_provider)
    return blueprint
