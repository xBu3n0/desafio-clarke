from flask import Blueprint, jsonify, request
from strawberry import Schema


def register_graphql_routes(
    blueprint: Blueprint,
    *,
    schema: Schema,
) -> None:
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
