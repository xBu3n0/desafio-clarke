from collections.abc import Callable

from flask import Blueprint, jsonify, request
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.domain.exceptions import EntityNotFoundError
from app.infrastructure.orm import EstadoModel, OfertaModel
from app.infrastructure.orm.energy.fornecedor import FornecedorModel
from app.interfaces.shared import format_decimal, parse_positive_int


def register_estado_routes(
    blueprint: Blueprint,
    *,
    session_provider: Callable[[], Session],
) -> None:
    @blueprint.get("/estados")
    def list_estados():
        with session_provider() as session:
            estados = session.scalars(
                select(EstadoModel).order_by(EstadoModel.nome)
            ).all()

        return jsonify(
            [
                {
                    "id": estado.id,
                    "nome": estado.nome,
                    "sigla": estado.sigla,
                    "tarifaBaseKwh": format_decimal(estado.tarifa_base_kwh, 2),
                }
                for estado in estados
            ]
        )

    @blueprint.get("/estados/<int:estado_id>")
    def list_ofertas_by_estado(estado_id: int):
        page = parse_positive_int(request.args.get("page", "1"), "page")
        per_page = parse_positive_int(request.args.get("per_page", "10"), "per_page")
        offset = (page - 1) * per_page

        with session_provider() as session:
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
                    "estadoId": oferta.estado_id,
                    "fornecedorId": oferta.fornecedor_id,
                    "solucao": oferta.solucao.value,
                    "custoKwh": format_decimal(oferta.custo_kwh, 2),
                    "fornecedor": {
                        "id": fornecedor.id,
                        "nome": fornecedor.nome,
                        "numeroClientes": fornecedor.numero_clientes,
                        "avaliacaoTotal": fornecedor.avaliacao_total,
                        "numeroAvaliacoes": fornecedor.numero_avaliacoes,
                        "avaliacaoMedia": format_decimal(
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
