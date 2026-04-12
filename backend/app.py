from flask import Flask, Blueprint, jsonify

app = Flask(__name__)

bp = Blueprint('search', __name__, url_prefix="/api/v1")

@bp.get("health")
def health():
    return jsonify({"status": "ok"})

app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
