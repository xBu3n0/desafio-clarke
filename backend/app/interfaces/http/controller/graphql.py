from flask import Blueprint, jsonify, request

from app.application.services import SearchQueryService
from app.interfaces.graphql import build_schema


def register_graphql_routes(
    blueprint: Blueprint,
    *,
    search_query_service: SearchQueryService,
) -> None:
    schema = build_schema(search_query_service)

    def _execute_graphql(
        query: str | None,
        variables: dict[str, object] | None,
        operation_name: str | None,
    ):
        if not query:
            return jsonify({"errors": [{"message": "query is required"}]}), 400

        result = schema.execute_sync(
            query,
            variable_values=variables,
            operation_name=operation_name,
        )

        response: dict[str, object] = {}
        if result.data is not None:
            response["data"] = result.data
        if result.errors:
            response["errors"] = [{"message": error.message} for error in result.errors]

        return jsonify(response), 200 if not result.errors else 400

    @blueprint.post("/graphql")
    def graphql_post_endpoint():
        payload = request.get_json(force=True, silent=False) or {}
        query = payload.get("query")
        variables = payload.get("variables")
        operation_name = payload.get("operationName")

        return _execute_graphql(query, variables, operation_name)
