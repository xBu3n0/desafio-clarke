from decimal import Decimal

from app.application.dto import OfertaComFornecedorSearchDTO
from app.domain.exceptions import ValidationError
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
from app.interfaces.shared import format_decimal, parse_decimal

from .types import EstadoType, FornecedorType, LogoType, OfertaType


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


def validate_logo_path(value: str) -> str:
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


def to_oferta_type(model: OfertaComFornecedorSearchDTO) -> OfertaType:
    return OfertaType(
        id=model.id,
        estado_id=model.estado_id,
        fornecedor_id=model.fornecedor_id,
        solucao=model.solucao.value,
        custo_kwh=format_decimal(model.custo_kwh, 2),
        fornecedor=to_fornecedor_type(model.fornecedor),
    )
