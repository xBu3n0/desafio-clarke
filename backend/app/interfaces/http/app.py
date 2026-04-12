from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from app.domain.exceptions import (
    DomainError,
    DuplicateEntityError,
    EntityNotFoundError,
    ValidationError,
)

from .controller import create_api_blueprint


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(create_api_blueprint())
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
