from flask import Blueprint, jsonify, request

from app.interfaces.graphql import build_schema


def register_graphql_routes(blueprint: Blueprint) -> None:
    schema = build_schema()

    @blueprint.get("/graphql")
    def graphql_info():
        return jsonify(
            {
                "message": "Send a POST request with a GraphQL query to this endpoint.",
                "path": "/api/v1/graphql",
            },
        )

    @blueprint.post("/graphql")
    def graphql_endpoint():
        payload = request.get_json(force=True, silent=False) or {}
        query = payload.get("query")
        variables = payload.get("variables")
        operation_name = payload.get("operationName")

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
