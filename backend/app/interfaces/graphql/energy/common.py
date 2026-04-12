import os
from decimal import Decimal

from app.domain.exceptions import EntityNotFoundError, ValidationError
from app.domain.value_objects import (
    AvaliacaoMedia,
    AvaliacaoTotal,
    CustoKwh,
    EstadoId,
    FornecedorId,
    NomeEstado,
    NomeFornecedor,
    NumeroAvaliacoes,
    NumeroClientes,
    SiglaEstado,
    Solucao,
    UrlLogo,
)
from app.infrastructure.database import create_engine_from_url, create_session_factory
from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from app.interfaces.shared import format_decimal, parse_decimal, parse_positive_int

from .types import EstadoType, FornecedorType, LogoType, OfertaType


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        msg = "DATABASE_URL is required"
        raise RuntimeError(msg)
    return database_url


def resolve_solucao(value: str) -> Solucao:
    try:
        return Solucao.create(value)
    except ValidationError:
        msg = "solucao must be 'GD' or 'Mercado Livre'"
        raise ValueError(msg) from None


def validate_estado_id(value: int) -> int:
    return EstadoId.create(value).value


def validate_fornecedor_id(value: int) -> int:
    return FornecedorId.create(value).value


def validate_nome_estado(value: str) -> str:
    return NomeEstado.create(value).value


def validate_sigla_estado(value: str) -> str:
    return SiglaEstado.create(value).value


def validate_tarifa_base_kwh(value: str) -> Decimal:
    return CustoKwh.create(parse_decimal(value, "tarifa_base_kwh")).value


def validate_nome_fornecedor(value: str) -> str:
    return NomeFornecedor.create(value).value


def validate_logo_url(value: str) -> str:
    return UrlLogo.create(value).value


def validate_numero_clientes(value: int) -> int:
    return NumeroClientes.create(value).value


def validate_avaliacao_total(value: int) -> int:
    return AvaliacaoTotal.create(value).value


def validate_numero_avaliacoes(value: int) -> int:
    return NumeroAvaliacoes.create(value).value


def validate_avaliacao_media(value: str) -> Decimal:
    return AvaliacaoMedia.create(parse_decimal(value, "avaliacao_media")).value


def validate_custo_kwh(value: str) -> Decimal:
    return CustoKwh.create(parse_decimal(value, "custo_kwh")).value


def validate_solucao(value: str) -> Solucao:
    return resolve_solucao(value)


def create_uow() -> SqlAlchemyUnitOfWork:
    engine = create_engine_from_url(get_database_url())
    session_factory = create_session_factory(engine)
    return SqlAlchemyUnitOfWork(session_factory)


def to_logo_type(model) -> LogoType:
    return LogoType(id=model.id, url=model.url)


def to_fornecedor_type(model) -> FornecedorType:
    return FornecedorType(
        id=model.id,
        nome=model.nome,
        numero_clientes=model.numero_clientes,
        avaliacao_total=model.avaliacao_total,
        numero_avaliacoes=model.numero_avaliacoes,
        avaliacao_media=format_decimal(model.avaliacao_media, 1),
        logo=to_logo_type(model.logo),
    )


def to_estado_type(model) -> EstadoType:
    return EstadoType(
        id=model.id,
        nome=model.nome,
        sigla=model.sigla,
        tarifa_base_kwh=format_decimal(model.tarifa_base_kwh, 2),
    )


def to_oferta_type(model, fornecedor=None) -> OfertaType:
    resolved_fornecedor = fornecedor if fornecedor is not None else model.fornecedor
    return OfertaType(
        id=model.id,
        estado_id=model.estado_id,
        fornecedor_id=model.fornecedor_id,
        solucao=model.solucao.value,
        custo_kwh=format_decimal(model.custo_kwh, 2),
        fornecedor=to_fornecedor_type(resolved_fornecedor),
    )


def list_ofertas_by_estado(
    *,
    estado_id: int,
    page: int,
    per_page: int,
) -> tuple[int, list[OfertaType]]:
    validated_estado_id = validate_estado_id(estado_id)
    validated_page = parse_positive_int(page, "page")
    validated_per_page = parse_positive_int(per_page, "per_page")
    offset = (validated_page - 1) * validated_per_page

    with create_uow() as uow:
        estado = uow.estados.get_by_id(validated_estado_id)
        if estado is None:
            raise EntityNotFoundError("estado was not found")

        all_ofertas = list(uow.ofertas.list_by_estado_id(validated_estado_id))
        total = len(all_ofertas)
        ofertas = all_ofertas[offset : offset + validated_per_page]
        fornecedor_ids = []
        seen_ids = set()
        for oferta in ofertas:
            if oferta.fornecedor_id not in seen_ids:
                fornecedor_ids.append(oferta.fornecedor_id)
                seen_ids.add(oferta.fornecedor_id)

        fornecedores = uow.fornecedores.list_by_ids(fornecedor_ids)
        fornecedores_index = {fornecedor.id: fornecedor for fornecedor in fornecedores}

    return (
        total,
        [
            to_oferta_type(oferta, fornecedores_index[oferta.fornecedor_id])
            for oferta in ofertas
            if oferta.fornecedor_id in fornecedores_index
        ],
    )
