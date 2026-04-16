from flask import Blueprint, jsonify, request

from app.application.services import SearchQueryService
from app.domain.exceptions import EntityNotFoundError
from app.interfaces.shared import format_decimal, parse_positive_int


def register_estado_routes(
    blueprint: Blueprint,
    *,
    search_query_service: SearchQueryService,
) -> None:
    @blueprint.get("/estados")
    def list_estados():
        estados = list(search_query_service.list_estados())

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

        estado = search_query_service.get_estado(estado_id)
        if estado is None:
            raise EntityNotFoundError("estado was not found")

        total, ofertas = search_query_service.list_ofertas_by_estado(
            estado_id=estado_id,
            page=page,
            per_page=per_page,
        )

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
        response.headers["X-Total-Count"] = str(total)
        return response
