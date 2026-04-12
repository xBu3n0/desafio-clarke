from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from decimal import ROUND_HALF_UP, Decimal

from app.application.dto import (
    BuscarOfertasCommand,
    ComparacaoFornecedorDTO,
    FornecedorSearchDTO,
    OfertaSearchDTO,
    ResultadoBuscaDTO,
    ResumoSolucaoDTO,
)
from app.application.ports import UnitOfWork
from app.domain.exceptions import EntityNotFoundError
from app.domain.value_objects import Solucao

UnitOfWorkFactory = Callable[[], UnitOfWork]

_TWO_DECIMALS = Decimal("0.01")
_ONE_DECIMAL = Decimal("0.1")


class BuscarOfertasUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory) -> None:
        self._uow_factory = uow_factory

    def execute(self, command: BuscarOfertasCommand) -> ResultadoBuscaDTO:
        sigla_estado = command.sigla_estado
        consumo_kwh = command.consumo_kwh

        with self._uow_factory() as uow:
            estado = uow.estados.get_by_sigla(sigla_estado.value)
            if estado is None:
                raise EntityNotFoundError("estado was not found")

            ofertas = list(uow.ofertas.list_by_estado_id(estado.id))
            fornecedores = self._build_fornecedores_index(
                uow=uow,
                ofertas=ofertas,
            )
            custo_base = consumo_kwh.value * estado.tarifa_base_kwh
            solucoes = self._build_solucoes(
                ofertas=ofertas,
                fornecedores=fornecedores,
                consumo_kwh=consumo_kwh.value,
                custo_base=custo_base,
            )

            return ResultadoBuscaDTO(
                estado_id=estado.id,
                estado_nome=estado.nome,
                estado_sigla=estado.sigla,
                consumo_kwh=self._format_decimal(consumo_kwh.value),
                tarifa_base_kwh=self._format_decimal(estado.tarifa_base_kwh),
                custo_base=self._format_decimal(custo_base),
                solucoes=solucoes,
            )

    def _build_fornecedores_index(
        self,
        *,
        uow: UnitOfWork,
        ofertas: list[OfertaSearchDTO],
    ) -> dict[int, FornecedorSearchDTO]:
        fornecedor_ids: list[int] = []
        seen_ids: set[int] = set()

        for oferta in ofertas:
            fornecedor_id = oferta.fornecedor_id
            if fornecedor_id not in seen_ids:
                fornecedor_ids.append(fornecedor_id)
                seen_ids.add(fornecedor_id)

        fornecedores = uow.fornecedores.list_by_ids(fornecedor_ids)
        return {fornecedor.id: fornecedor for fornecedor in fornecedores}

    def _build_solucoes(
        self,
        *,
        ofertas: list[OfertaSearchDTO],
        fornecedores: dict[int, FornecedorSearchDTO],
        consumo_kwh: Decimal,
        custo_base: Decimal,
    ) -> list[ResumoSolucaoDTO]:
        ofertas_por_solucao: dict[Solucao, list[OfertaSearchDTO]] = defaultdict(list)

        for oferta in ofertas:
            solucao = (
                oferta.solucao
                if isinstance(oferta.solucao, Solucao)
                else Solucao.create(str(oferta.solucao))
            )
            ofertas_por_solucao[solucao].append(oferta)

        solucoes: list[ResumoSolucaoDTO] = []
        for solucao in Solucao:
            ofertas_da_solucao = ofertas_por_solucao.get(solucao, [])
            comparacoes = self._build_comparacoes(
                ofertas=ofertas_da_solucao,
                fornecedores=fornecedores,
                consumo_kwh=consumo_kwh,
                custo_base=custo_base,
            )

            if not comparacoes:
                solucoes.append(
                    ResumoSolucaoDTO(
                        solucao=solucao.value,
                        fornecedores=[],
                    )
                )
                continue

            solucoes.append(
                ResumoSolucaoDTO(
                    solucao=solucao.value,
                    fornecedores=comparacoes,
                )
            )

        return solucoes

    def _build_comparacoes(
        self,
        *,
        ofertas: list[OfertaSearchDTO],
        fornecedores: dict[int, FornecedorSearchDTO],
        consumo_kwh: Decimal,
        custo_base: Decimal,
    ) -> list[ComparacaoFornecedorDTO]:
        comparacoes: list[tuple[Decimal, ComparacaoFornecedorDTO]] = []

        for oferta in ofertas:
            fornecedor = fornecedores.get(oferta.fornecedor_id)
            if fornecedor is None:
                raise EntityNotFoundError("fornecedor was not found")

            custo_mensal = consumo_kwh * oferta.custo_kwh
            economia = custo_base - custo_mensal
            economia_percentual = economia / custo_base
            comparacoes.append(
                (
                    economia,
                    ComparacaoFornecedorDTO(
                        fornecedor_id=fornecedor.id,
                        fornecedor_nome=fornecedor.nome,
                        logo_path=fornecedor.logo.url,
                        custo_kwh=self._format_decimal(oferta.custo_kwh),
                        custo_mensal=self._format_decimal(custo_mensal),
                        economia=self._format_decimal(economia),
                        economia_percentual=self._format_decimal(economia_percentual),
                        numero_clientes=fornecedor.numero_clientes,
                        avaliacao_media=self._format_rating(fornecedor.avaliacao_media),
                    ),
                )
            )

        comparacoes.sort(
            key=lambda item: (item[0], item[1].fornecedor_nome),
            reverse=True,
        )
        return [comparacao for _, comparacao in comparacoes]

    def _format_decimal(self, value: Decimal) -> str:
        return str(value.quantize(_TWO_DECIMALS, rounding=ROUND_HALF_UP))

    def _format_rating(self, value: Decimal) -> str:
        return str(value.quantize(_ONE_DECIMAL, rounding=ROUND_HALF_UP))
