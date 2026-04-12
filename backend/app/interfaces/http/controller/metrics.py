import os
from time import perf_counter

from flask import Flask, Response, g, request
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    Summary,
    generate_latest,
)

FLASK_APP_NAME = os.getenv("FLASK_METRICS_APP_NAME", "flask-monitoring")

HTTP_REQUESTS_TOTAL = Counter(
    "clarke_http_requests_total",
    "Total number of HTTP requests handled by the backend",
    ("method", "path", "status"),
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "clarke_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ("method", "path"),
)

FLASK_INFO = Gauge(
    "flask_info",
    "Flask application info for Grafana dashboard compatibility",
    ("app_name",),
)

FLASK_REQUEST_STATUS_TOTAL = Counter(
    "flask_request_status_total",
    "Total Flask requests grouped by endpoint, method and status",
    ("app_name", "endpoint", "method", "status"),
)

FLASK_REQUEST_DURATION_SECONDS = Summary(
    "flask_request_duration_seconds",
    "Flask request duration in seconds",
    ("app_name", "endpoint", "method"),
)


def _request_path_label() -> str:
    return getattr(request.url_rule, "rule", request.path)


def register_metrics(app: Flask) -> None:
    FLASK_INFO.labels(app_name=FLASK_APP_NAME).set(1)

    @app.before_request
    def _capture_request_start_time():
        g.request_start_time = perf_counter()

    @app.after_request
    def _record_request_metrics(response: Response):
        duration = perf_counter() - getattr(g, "request_start_time", perf_counter())
        path = _request_path_label()
        method = request.method
        status = str(response.status_code)

        HTTP_REQUESTS_TOTAL.labels(method=method, path=path, status=status).inc()
        HTTP_REQUEST_DURATION_SECONDS.labels(method=method, path=path).observe(duration)
        FLASK_REQUEST_STATUS_TOTAL.labels(
            app_name=FLASK_APP_NAME,
            endpoint=path,
            method=method,
            status=status,
        ).inc()
        FLASK_REQUEST_DURATION_SECONDS.labels(
            app_name=FLASK_APP_NAME,
            endpoint=path,
            method=method,
        ).observe(duration)
        return response


def build_metrics_response() -> Response:
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
