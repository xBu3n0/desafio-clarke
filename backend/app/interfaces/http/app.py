import os
from collections.abc import Callable

from flask import Flask, jsonify
from sqlalchemy.orm import Session
from werkzeug.exceptions import HTTPException

from app.domain.exceptions import (
    DomainError,
    DuplicateEntityError,
    EntityNotFoundError,
    ValidationError,
)
from app.infrastructure.database import create_engine_from_url, create_session_factory
from app.infrastructure.dependencies import build_search_query_service
from app.infrastructure.telemetry import bootstrap_telemetry, instrument_flask_app

from .controller import create_api_blueprint
from .controller.metrics import build_metrics_response, register_metrics


def _build_session_provider() -> Callable[[], Session]:
    session_factory = None

    def session_provider() -> Session:
        nonlocal session_factory
        if session_factory is None:
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                msg = "DATABASE_URL is required"
                raise RuntimeError(msg)
            engine = create_engine_from_url(database_url)
            session_factory = create_session_factory(engine)
        return session_factory()

    return session_provider


def create_app(session_provider: Callable[[], Session] | None = None) -> Flask:
    bootstrap_telemetry()
    app = Flask(__name__)
    instrument_flask_app(app)
    register_metrics(app)

    @app.get("/metrics")
    def metrics():
        return build_metrics_response()

    resolved_session_provider = session_provider or _build_session_provider()
    search_query_service = build_search_query_service(
        session_provider=resolved_session_provider
    )
    app.register_blueprint(
        create_api_blueprint(
            session_provider=resolved_session_provider,
            search_query_service=search_query_service,
        )
    )
    register_error_handlers(app)
    return app


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):
        return jsonify({"error": str(error)}), 422

    @app.errorhandler(EntityNotFoundError)
    def handle_not_found(error: EntityNotFoundError):
        return jsonify({"error": str(error)}), 404

    @app.errorhandler(DuplicateEntityError)
    def handle_conflict(error: DuplicateEntityError):
        return jsonify({"error": str(error)}), 409

    @app.errorhandler(KeyError)
    def handle_missing_field(error: KeyError):
        return jsonify({"error": f"missing required field: {error.args[0]}"}), 400

    @app.errorhandler(ValueError)
    def handle_value_error(error: ValueError):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(DomainError)
    def handle_domain_error(error: DomainError):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):
        return jsonify({"error": error.description}), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        return jsonify({"error": str(error)}), 500
