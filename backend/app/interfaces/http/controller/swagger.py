from flask import Blueprint, Response, jsonify


def _build_openapi_spec() -> dict[str, object]:
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "Clarke Energia API",
            "version": "1.0.0",
            "description": "REST and GraphQL endpoints for Clarke Energia challenge.",
        },
        "servers": [{"url": "/api/v1"}],
        "paths": {
            "/health": {
                "get": {
                    "summary": "Health check",
                    "responses": {
                        "200": {
                            "description": "API is alive",
                        }
                    },
                }
            },
            "/estados": {
                "get": {
                    "summary": "List states",
                    "responses": {
                        "200": {
                            "description": "States list",
                        }
                    },
                }
            },
            "/estados/{estado_id}": {
                "get": {
                    "summary": "List offers by state",
                    "parameters": [
                        {
                            "name": "estado_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                        },
                        {
                            "name": "page",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "integer", "minimum": 1, "default": 1},
                        },
                        {
                            "name": "per_page",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "integer", "minimum": 1, "default": 10},
                        },
                    ],
                    "responses": {
                        "200": {"description": "Offers list"},
                        "404": {"description": "State not found"},
                    },
                }
            },
            "/graphql": {
                "post": {
                    "summary": "Execute GraphQL query",
                    "responses": {
                        "200": {"description": "GraphQL query result"},
                        "400": {"description": "GraphQL validation errors"},
                    },
                },
            },
        },
    }


def register_swagger_routes(blueprint: Blueprint) -> None:
    @blueprint.get("/swagger.json")
    def swagger_json():
        return jsonify(_build_openapi_spec())

    @blueprint.get("/swagger")
    def swagger_ui():
        html = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Clarke Energia API Swagger</title>
    <link
      rel="stylesheet"
      href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css"
    />
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
      window.ui = SwaggerUIBundle({
        url: "/api/v1/swagger.json",
        dom_id: "#swagger-ui",
      });
    </script>
  </body>
</html>
        """
        return Response(html, mimetype="text/html")
