from flask import Blueprint, jsonify


def register_health_routes(blueprint: Blueprint) -> None:
    @blueprint.get("/health")
    def health():
        return jsonify({"status": "ok"})
