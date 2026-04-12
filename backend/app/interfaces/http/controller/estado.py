import os
from decimal import Decimal

from flask import Blueprint, jsonify, request
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.domain.exceptions import EntityNotFoundError
from app.infrastructure.database import create_engine_from_url, create_session_factory
from app.infrastructure.orm import EstadoModel, OfertaModel
from app.infrastructure.orm.energy.fornecedor import FornecedorModel


def _format_decimal(value: Decimal, places: int) -> str:
    return f"{value:.{places}f}"


def _parse_positive_int(value: str, field_name: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        msg = f"{field_name} must be an integer"
        raise ValueError(msg) from exc
    if parsed <= 0:
        msg = f"{field_name} must be greater than 0"
        raise ValueError(msg)
    return parsed


def _get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        msg = "DATABASE_URL is required"
        raise RuntimeError(msg)
    return database_url


def register_estado_routes(blueprint: Blueprint) -> None:
    @blueprint.get("/estados/<int:estado_id>")
    def list_ofertas_by_estado(estado_id: int):
        page = _parse_positive_int(request.args.get("page", "1"), "page")
        per_page = _parse_positive_int(request.args.get("per_page", "10"), "per_page")
        offset = (page - 1) * per_page

        engine = create_engine_from_url(_get_database_url())
        session_factory = create_session_factory(engine)

        with session_factory() as session:
            estado = session.get(EstadoModel, estado_id)
            if estado is None:
                raise EntityNotFoundError("estado was not found")

            total = session.scalar(
                select(func.count())
                .select_from(OfertaModel)
                .where(OfertaModel.estado_id == estado_id)
            )
            ofertas = session.scalars(
                select(OfertaModel)
                .where(OfertaModel.estado_id == estado_id)
                .options(
                    selectinload(OfertaModel.fornecedor).selectinload(
                        FornecedorModel.logo
                    ),
                )
                .order_by(OfertaModel.id)
                .offset(offset)
                .limit(per_page)
            ).all()

        items = []
        for oferta in ofertas:
            fornecedor = oferta.fornecedor
            items.append(
                {
                    "id": oferta.id,
                    "estado_id": oferta.estado_id,
                    "fornecedor_id": oferta.fornecedor_id,
                    "solucao": oferta.solucao.value,
                    "custo_kwh": _format_decimal(oferta.custo_kwh, 2),
                    "fornecedor": {
                        "id": fornecedor.id,
                        "nome": fornecedor.nome,
                        "numero_clientes": fornecedor.numero_clientes,
                        "avaliacao_total": fornecedor.avaliacao_total,
                        "numero_avaliacoes": fornecedor.numero_avaliacoes,
                        "avaliacao_media": _format_decimal(
                            fornecedor.avaliacao_media,
                            1,
                        ),
                        "logo": {
                            "id": fornecedor.logo.id,
                            "url": fornecedor.logo.url,
                        },
                    },
                }
            )

        response = jsonify(items)
        response.headers["X-Estado-Id"] = str(estado_id)
        response.headers["X-Page"] = str(page)
        response.headers["X-Per-Page"] = str(per_page)
        response.headers["X-Total-Count"] = str(total or 0)
        return response
