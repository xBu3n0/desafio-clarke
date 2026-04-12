import logging
import os
from collections.abc import Sequence

from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)

_TELEMETRY_BOOTSTRAPPED = False
_INSTRUMENTED_ENGINES: set[int] = set()


def _telemetry_enabled() -> bool:
    # Follow OpenTelemetry's standard disable switch first.
    if os.getenv("OTEL_SDK_DISABLED", "").lower() == "true":
        return False
    return os.getenv("APP_OTEL_ENABLED", "true").lower() != "false"


def bootstrap_telemetry(service_name: str = "clarke-energy-backend") -> None:
    global _TELEMETRY_BOOTSTRAPPED
    if _TELEMETRY_BOOTSTRAPPED or not _telemetry_enabled():
        return

    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except ImportError:
        logger.info("OpenTelemetry packages are not installed; telemetry is disabled")
        return

    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)

    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if endpoint:
        provider.add_span_processor(
            BatchSpanProcessor(
                OTLPSpanExporter(
                    endpoint=endpoint,
                    headers=dict(
                        parse_otel_headers(os.getenv("OTEL_EXPORTER_OTLP_HEADERS"))
                    ),
                )
            )
        )
    else:
        logger.info(
            "OTEL_EXPORTER_OTLP_ENDPOINT is not set; traces will not be exported"
        )

    trace.set_tracer_provider(provider)
    _TELEMETRY_BOOTSTRAPPED = True


def instrument_flask_app(app) -> None:
    if not _telemetry_enabled():
        return

    bootstrap_telemetry()
    if not _TELEMETRY_BOOTSTRAPPED:
        return

    try:
        from opentelemetry.instrumentation.flask import FlaskInstrumentor
    except ImportError:
        return

    FlaskInstrumentor().instrument_app(app)


def instrument_sqlalchemy_engine(engine: Engine) -> None:
    if not _telemetry_enabled():
        return

    bootstrap_telemetry()
    if not _TELEMETRY_BOOTSTRAPPED:
        return

    engine_id = id(engine)
    if engine_id in _INSTRUMENTED_ENGINES:
        return

    try:
        from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
    except ImportError:
        return

    SQLAlchemyInstrumentor().instrument(engine=engine)
    _INSTRUMENTED_ENGINES.add(engine_id)


def parse_otel_headers(raw_headers: str | None) -> Sequence[tuple[str, str]]:
    if not raw_headers:
        return ()
    pairs = []
    for item in raw_headers.split(","):
        key, separator, value = item.partition("=")
        if separator and key and value:
            pairs.append((key.strip(), value.strip()))
    return tuple(pairs)
