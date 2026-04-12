import strawberry

from app.domain.entities import Estado, Fornecedor, Logo, Oferta
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
    UrlLogo,
)
from app.infrastructure.database import create_engine_from_url, create_session_factory
from app.infrastructure.orm import EstadoModel, FornecedorModel, OfertaModel
from app.infrastructure.orm.energy.logo import LogoModel
from app.infrastructure.seed import run_seed

from .common import (
    get_database_url,
    to_estado_type,
    to_fornecedor_type,
    to_oferta_type,
    validate_avaliacao_media,
    validate_avaliacao_total,
    validate_custo_kwh,
    validate_estado_id,
    validate_fornecedor_id,
    validate_logo_url,
    validate_nome_estado,
    validate_nome_fornecedor,
    validate_numero_avaliacoes,
    validate_numero_clientes,
    validate_sigla_estado,
    validate_solucao,
    validate_tarifa_base_kwh,
)
from .types import EstadoType, FornecedorType, OfertaType


def build_mutation_type():
    @strawberry.type
    class Mutation:
        @strawberry.mutation
        def create_estado(
            self,
            nome: str,
            sigla: str,
            tarifa_base_kwh: str,
        ) -> EstadoType:
            validated_nome = validate_nome_estado(nome)
            validated_sigla = validate_sigla_estado(sigla)
            validated_tarifa_base_kwh = validate_tarifa_base_kwh(tarifa_base_kwh)
            estado = Estado(
                id=None,
                nome=NomeEstado.create(validated_nome),
                sigla=SiglaEstado.create(validated_sigla),
                tarifa_base_kwh=CustoKwh.create(validated_tarifa_base_kwh),
            )

            engine = create_engine_from_url(get_database_url())
            session_factory = create_session_factory(engine)
            with session_factory() as session:
                estado_model = EstadoModel(
                    nome=estado.nome.value,
                    sigla=estado.sigla.value,
                    tarifa_base_kwh=estado.tarifa_base_kwh.value,
                )
                session.add(estado_model)
                session.commit()
                session.refresh(estado_model)
            return to_estado_type(estado_model)

        @strawberry.mutation
        def create_fornecedor(
            self,
            nome: str,
            logo_url: str,
            numero_clientes: int,
            avaliacao_total: int,
            numero_avaliacoes: int,
            avaliacao_media: str,
        ) -> FornecedorType:
            validated_nome = validate_nome_fornecedor(nome)
            validated_logo_url = validate_logo_url(logo_url)
            validated_numero_clientes = validate_numero_clientes(numero_clientes)
            validated_avaliacao_total = validate_avaliacao_total(avaliacao_total)
            validated_numero_avaliacoes = validate_numero_avaliacoes(numero_avaliacoes)
            validated_avaliacao_media = validate_avaliacao_media(avaliacao_media)
            fornecedor = Fornecedor(
                id=None,
                nome=NomeFornecedor.create(validated_nome),
                logo=Logo(
                    id=None,
                    url=UrlLogo.create(validated_logo_url),
                ),
                numero_clientes=NumeroClientes.create(validated_numero_clientes),
                avaliacao_total=AvaliacaoTotal.create(validated_avaliacao_total),
                numero_avaliacoes=NumeroAvaliacoes.create(validated_numero_avaliacoes),
                avaliacao_media=AvaliacaoMedia.create(validated_avaliacao_media),
            )

            engine = create_engine_from_url(get_database_url())
            session_factory = create_session_factory(engine)
            with session_factory() as session:
                fornecedor_model = FornecedorModel(
                    nome=fornecedor.nome.value,
                    logo=LogoModel(url=fornecedor.logo.url.value),
                    numero_clientes=fornecedor.numero_clientes.value,
                    avaliacao_total=fornecedor.avaliacao_total.value,
                    numero_avaliacoes=fornecedor.numero_avaliacoes.value,
                    avaliacao_media=fornecedor.avaliacao_media.value,
                )
                session.add(fornecedor_model)
                session.commit()
                session.refresh(fornecedor_model)
                _ = fornecedor_model.logo
            return to_fornecedor_type(fornecedor_model)

        @strawberry.mutation
        def create_oferta(
            self,
            estado_id: int,
            fornecedor_id: int,
            solucao: str,
            custo_kwh: str,
        ) -> OfertaType:
            validated_estado_id = validate_estado_id(estado_id)
            validated_fornecedor_id = validate_fornecedor_id(fornecedor_id)
            validated_solucao = validate_solucao(solucao)
            validated_custo_kwh = validate_custo_kwh(custo_kwh)
            oferta = Oferta(
                id=None,
                estado_id=EstadoId.create(validated_estado_id),
                fornecedor_id=FornecedorId.create(validated_fornecedor_id),
                solucao=validated_solucao,
                custo_kwh=CustoKwh.create(validated_custo_kwh),
            )

            engine = create_engine_from_url(get_database_url())
            session_factory = create_session_factory(engine)
            with session_factory() as session:
                oferta_model = OfertaModel(
                    estado_id=oferta.estado_id.value,
                    fornecedor_id=oferta.fornecedor_id.value,
                    solucao=oferta.solucao,
                    custo_kwh=oferta.custo_kwh.value,
                )
                session.add(oferta_model)
                session.commit()
                session.refresh(oferta_model)
                _ = oferta_model.fornecedor.logo
            return to_oferta_type(oferta_model)

        @strawberry.mutation
        def run_seed(self) -> bool:
            run_seed(get_database_url())
            return True

    return Mutation
