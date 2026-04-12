import os
from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy import select

from app.domain.value_objects import Solucao
from app.infrastructure.database import create_engine_from_url, create_session_factory
from app.infrastructure.orm import EstadoModel, FornecedorModel, LogoModel, OfertaModel


@dataclass(frozen=True)
class EstadoSeed:
    id: int
    nome: str
    sigla: str
    tarifa_base_kwh: Decimal


@dataclass(frozen=True)
class FornecedorSeed:
    id: int
    nome: str
    logo_id: int
    logo_path: str
    numero_clientes: int
    avaliacao_total: int
    numero_avaliacoes: int
    avaliacao_media: Decimal


@dataclass(frozen=True)
class OfertaSeed:
    estado_id: int
    fornecedor_id: int
    solucao: Solucao
    custo_kwh: Decimal


ESTADOS: tuple[EstadoSeed, ...] = (
    EstadoSeed(1, "Sao Paulo", "SP", Decimal("0.62")),
    EstadoSeed(2, "Parana", "PR", Decimal("0.58")),
    EstadoSeed(3, "Rio de Janeiro", "RJ", Decimal("0.64")),
    EstadoSeed(4, "Minas Gerais", "MG", Decimal("0.57")),
)

FORNECEDORES: tuple[FornecedorSeed, ...] = (
    FornecedorSeed(
        id=1,
        nome="Lumen Energia",
        logo_id=1,
        logo_path="logos/lumen.svg",
        numero_clientes=14300,
        avaliacao_total=4130,
        numero_avaliacoes=500,
        avaliacao_media=Decimal("8.3"),
    ),
    FornecedorSeed(
        id=2,
        nome="Aurora Power",
        logo_id=2,
        logo_path="logos/aurora.svg",
        numero_clientes=9200,
        avaliacao_total=3720,
        numero_avaliacoes=450,
        avaliacao_media=Decimal("8.8"),
    ),
    FornecedorSeed(
        id=3,
        nome="Brisa Livre",
        logo_id=3,
        logo_path="logos/brisa.svg",
        numero_clientes=7200,
        avaliacao_total=2840,
        numero_avaliacoes=350,
        avaliacao_media=Decimal("8.1"),
    ),
    FornecedorSeed(
        id=4,
        nome="Nexa Solar",
        logo_id=4,
        logo_path="logos/nexa.svg",
        numero_clientes=5100,
        avaliacao_total=2260,
        numero_avaliacoes=280,
        avaliacao_media=Decimal("8.9"),
    ),
)

OFERTAS: tuple[OfertaSeed, ...] = (
    OfertaSeed(1, 1, Solucao.GD, Decimal("0.46")),
    OfertaSeed(1, 1, Solucao.MERCADO_LIVRE, Decimal("0.44")),
    OfertaSeed(1, 2, Solucao.GD, Decimal("0.47")),
    OfertaSeed(1, 3, Solucao.MERCADO_LIVRE, Decimal("0.43")),
    OfertaSeed(1, 4, Solucao.GD, Decimal("0.45")),
    OfertaSeed(2, 1, Solucao.GD, Decimal("0.42")),
    OfertaSeed(2, 2, Solucao.MERCADO_LIVRE, Decimal("0.41")),
    OfertaSeed(2, 4, Solucao.GD, Decimal("0.44")),
    OfertaSeed(3, 2, Solucao.GD, Decimal("0.50")),
    OfertaSeed(3, 2, Solucao.MERCADO_LIVRE, Decimal("0.48")),
    OfertaSeed(3, 3, Solucao.MERCADO_LIVRE, Decimal("0.47")),
    OfertaSeed(4, 1, Solucao.GD, Decimal("0.40")),
    OfertaSeed(4, 3, Solucao.GD, Decimal("0.41")),
    OfertaSeed(4, 4, Solucao.MERCADO_LIVRE, Decimal("0.39")),
)


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        msg = "DATABASE_URL is required to run seeds"
        raise RuntimeError(msg)
    return database_url


def get_public_assets_base_url() -> str:
    public_assets_base_url = os.getenv("PUBLIC_ASSETS_BASE_URL")
    if public_assets_base_url:
        return public_assets_base_url.rstrip("/")

    minio_public_endpoint = os.getenv("MINIO_PUBLIC_ENDPOINT")
    minio_bucket_name = os.getenv("MINIO_BUCKET_NAME", "public")
    if minio_public_endpoint:
        return f"{minio_public_endpoint.rstrip('/')}/{minio_bucket_name}"

    return "https://cdn.example.com"


def build_logo_path(base_url: str, logo_path: str) -> str:
    return f"{base_url}/{logo_path.lstrip('/')}"


def seed_states(session) -> None:
    for estado_seed in ESTADOS:
        estado = session.execute(
            select(EstadoModel).where(EstadoModel.sigla == estado_seed.sigla)
        ).scalar_one_or_none()
        if estado is None:
            session.add(
                EstadoModel(
                    id=estado_seed.id,
                    nome=estado_seed.nome,
                    sigla=estado_seed.sigla,
                    tarifa_base_kwh=estado_seed.tarifa_base_kwh,
                )
            )
            continue

        estado.nome = estado_seed.nome
        estado.tarifa_base_kwh = estado_seed.tarifa_base_kwh


def seed_suppliers(session) -> None:
    public_assets_base_url = get_public_assets_base_url()
    for fornecedor_seed in FORNECEDORES:
        logo_path = build_logo_path(public_assets_base_url, fornecedor_seed.logo_path)
        fornecedor = session.get(FornecedorModel, fornecedor_seed.id)
        if fornecedor is None:
            session.add(
                FornecedorModel(
                    id=fornecedor_seed.id,
                    nome=fornecedor_seed.nome,
                    logo=LogoModel(
                        id=fornecedor_seed.logo_id,
                        url=logo_path,
                    ),
                    numero_clientes=fornecedor_seed.numero_clientes,
                    avaliacao_total=fornecedor_seed.avaliacao_total,
                    numero_avaliacoes=fornecedor_seed.numero_avaliacoes,
                    avaliacao_media=fornecedor_seed.avaliacao_media,
                )
            )
            continue

        fornecedor.nome = fornecedor_seed.nome
        fornecedor.numero_clientes = fornecedor_seed.numero_clientes
        fornecedor.avaliacao_total = fornecedor_seed.avaliacao_total
        fornecedor.numero_avaliacoes = fornecedor_seed.numero_avaliacoes
        fornecedor.avaliacao_media = fornecedor_seed.avaliacao_media

        if fornecedor.logo is None:
            fornecedor.logo = LogoModel(
                id=fornecedor_seed.logo_id,
                url=logo_path,
            )
        else:
            fornecedor.logo.url = logo_path


def seed_offers(session) -> None:
    for oferta_seed in OFERTAS:
        oferta = session.execute(
            select(OfertaModel).where(
                OfertaModel.estado_id == oferta_seed.estado_id,
                OfertaModel.fornecedor_id == oferta_seed.fornecedor_id,
                OfertaModel.solucao == oferta_seed.solucao,
            )
        ).scalar_one_or_none()
        if oferta is None:
            session.add(
                OfertaModel(
                    estado_id=oferta_seed.estado_id,
                    fornecedor_id=oferta_seed.fornecedor_id,
                    solucao=oferta_seed.solucao,
                    custo_kwh=oferta_seed.custo_kwh,
                )
            )
            continue

        oferta.custo_kwh = oferta_seed.custo_kwh


def run_seed(database_url: str) -> None:
    engine = create_engine_from_url(database_url)
    session_factory = create_session_factory(engine)

    with session_factory() as session:
        seed_states(session)
        seed_suppliers(session)
        session.flush()
        seed_offers(session)
        session.commit()


def main() -> None:
    run_seed(get_database_url())


if __name__ == "__main__":
    main()
