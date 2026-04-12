from collections.abc import Sequence
from decimal import Decimal

import pytest

from app.application.dto.search import BuscarOfertasCommand
from app.application.dto.search.read_models import (
    EstadoSearchDTO,
    FornecedorSearchDTO,
    LogoSearchDTO,
    OfertaSearchDTO,
)
from app.application.ports import (
    EstadoSearchRepository,
    FornecedorSearchRepository,
    OfertaSearchRepository,
    UnitOfWork,
)
from app.application.use_cases import BuscarOfertasUseCase
from app.domain.exceptions import EntityNotFoundError, ValidationError
from app.domain.value_objects import ConsumoKwh, SiglaEstado, Solucao


class FakeEstadoSearchRepository(EstadoSearchRepository):
    def __init__(self, estados: Sequence[EstadoSearchDTO]) -> None:
        self._estados = list(estados)

    def get_by_sigla(self, sigla: str) -> EstadoSearchDTO | None:
        for estado in self._estados:
            if estado.sigla == sigla:
                return estado
        return None

    def get_by_id(self, estado_id: int) -> EstadoSearchDTO | None:
        for estado in self._estados:
            if estado.id == estado_id:
                return estado
        return None

    def list_all(self) -> Sequence[EstadoSearchDTO]:
        return self._estados


class FakeFornecedorSearchRepository(FornecedorSearchRepository):
    def __init__(self, fornecedores: Sequence[FornecedorSearchDTO]) -> None:
        self._fornecedores = list(fornecedores)

    def list_by_ids(
        self,
        fornecedor_ids: Sequence[int],
    ) -> Sequence[FornecedorSearchDTO]:
        ids = set(fornecedor_ids)
        return [fornecedor for fornecedor in self._fornecedores if fornecedor.id in ids]

    def count(self) -> int:
        return len(self._fornecedores)


class FakeOfertaSearchRepository(OfertaSearchRepository):
    def __init__(self, ofertas: Sequence[OfertaSearchDTO]) -> None:
        self._ofertas = list(ofertas)

    def list_by_estado_id(self, estado_id: int) -> Sequence[OfertaSearchDTO]:
        return [oferta for oferta in self._ofertas if oferta.estado_id == estado_id]


class FakeUnitOfWork(UnitOfWork):
    def __init__(
        self,
        *,
        estados: Sequence[EstadoSearchDTO],
        fornecedores: Sequence[FornecedorSearchDTO],
        ofertas: Sequence[OfertaSearchDTO],
    ) -> None:
        self.estados = FakeEstadoSearchRepository(estados)
        self.fornecedores = FakeFornecedorSearchRepository(fornecedores)
        self.ofertas = FakeOfertaSearchRepository(ofertas)
        self.commit_called = False
        self.rollback_called = False
        self.close_called = False

    def commit(self) -> None:
        self.commit_called = True

    def rollback(self) -> None:
        self.rollback_called = True

    def close(self) -> None:
        self.close_called = True


def make_estado() -> EstadoSearchDTO:
    return EstadoSearchDTO(
        id=1,
        nome="Sao Paulo",
        sigla="SP",
        tarifa_base_kwh=Decimal("0.50"),
    )


def make_fornecedor(
    fornecedor_id: int,
    nome: str,
    logo_url: str,
    avaliacao_media: str,
) -> FornecedorSearchDTO:
    return FornecedorSearchDTO(
        id=fornecedor_id,
        nome=nome,
        logo=LogoSearchDTO(
            id=fornecedor_id,
            url=logo_url,
        ),
        numero_clientes=1000 + fornecedor_id,
        avaliacao_total=50 + fornecedor_id,
        numero_avaliacoes=10 + fornecedor_id,
        avaliacao_media=Decimal(avaliacao_media),
    )


def make_oferta(
    oferta_id: int,
    fornecedor_id: int,
    solucao: Solucao,
    custo_kwh: str,
) -> OfertaSearchDTO:
    return OfertaSearchDTO(
        id=oferta_id,
        estado_id=1,
        fornecedor_id=fornecedor_id,
        solucao=solucao,
        custo_kwh=Decimal(custo_kwh),
    )


def make_command(
    *,
    sigla_estado: str = "SP",
    consumo_kwh: str = "1000",
) -> BuscarOfertasCommand:
    return BuscarOfertasCommand(
        sigla_estado=SiglaEstado.create(sigla_estado),
        consumo_kwh=ConsumoKwh.create(Decimal(consumo_kwh)),
    )


def test_search_builds_ranked_results_grouped_by_solution() -> None:
    estado = make_estado()
    fornecedor_a = make_fornecedor(
        fornecedor_id=1,
        nome="Fornecedor A",
        logo_url="https://example.com/a.png",
        avaliacao_media="8.5",
    )
    fornecedor_b = make_fornecedor(
        fornecedor_id=2,
        nome="Fornecedor B",
        logo_url="https://example.com/b.png",
        avaliacao_media="9.0",
    )
    fornecedor_c = make_fornecedor(
        fornecedor_id=3,
        nome="Fornecedor C",
        logo_url="https://example.com/c.png",
        avaliacao_media="7.5",
    )
    ofertas = [
        make_oferta(1, 1, Solucao.GD, "0.40"),
        make_oferta(2, 2, Solucao.GD, "0.35"),
        make_oferta(3, 3, Solucao.MERCADO_LIVRE, "0.45"),
    ]
    uow = FakeUnitOfWork(
        estados=[estado],
        fornecedores=[fornecedor_a, fornecedor_b, fornecedor_c],
        ofertas=ofertas,
    )
    use_case = BuscarOfertasUseCase(lambda: uow)

    result = use_case.execute(make_command())

    assert result.estado_sigla == "SP"
    assert result.custo_base == "500.00"
    assert [solucao.solucao for solucao in result.solucoes] == ["GD", "Mercado Livre"]

    gd = result.solucoes[0]
    assert [fornecedor.fornecedor_nome for fornecedor in gd.fornecedores] == [
        "Fornecedor B",
        "Fornecedor A",
    ]
    assert gd.fornecedores[0].custo_mensal == "350.00"
    assert gd.fornecedores[0].economia == "150.00"

    mercado_livre = result.solucoes[1]
    assert [
        fornecedor.fornecedor_nome for fornecedor in mercado_livre.fornecedores
    ] == ["Fornecedor C"]
    assert uow.commit_called is False
    assert uow.close_called is True


def test_search_marks_a_solution_as_unavailable_when_it_has_no_offer() -> None:
    estado = make_estado()
    fornecedor = make_fornecedor(
        fornecedor_id=1,
        nome="Fornecedor A",
        logo_url="https://example.com/a.png",
        avaliacao_media="8.5",
    )
    uow = FakeUnitOfWork(
        estados=[estado],
        fornecedores=[fornecedor],
        ofertas=[make_oferta(1, 1, Solucao.GD, "0.40")],
    )
    use_case = BuscarOfertasUseCase(lambda: uow)

    result = use_case.execute(make_command())

    mercado_livre = result.solucoes[1]
    assert mercado_livre.solucao == "Mercado Livre"
    assert mercado_livre.fornecedores == []


def test_search_keeps_negative_savings_when_an_offer_is_more_expensive() -> None:
    estado = make_estado()
    fornecedor = make_fornecedor(
        fornecedor_id=1,
        nome="Fornecedor A",
        logo_url="https://example.com/a.png",
        avaliacao_media="8.5",
    )
    uow = FakeUnitOfWork(
        estados=[estado],
        fornecedores=[fornecedor],
        ofertas=[make_oferta(1, 1, Solucao.GD, "0.55")],
    )
    use_case = BuscarOfertasUseCase(lambda: uow)

    result = use_case.execute(make_command())

    gd = result.solucoes[0]
    assert gd.fornecedores[0].economia == "-50.00"


def test_search_requires_an_existing_state() -> None:
    uow = FakeUnitOfWork(estados=[], fornecedores=[], ofertas=[])
    use_case = BuscarOfertasUseCase(lambda: uow)

    with pytest.raises(EntityNotFoundError):
        use_case.execute(make_command())

    assert uow.rollback_called is True
    assert uow.close_called is True


def test_search_requires_a_valid_state_code() -> None:
    with pytest.raises(ValidationError):
        make_command(sigla_estado="sp")


def test_search_requires_a_positive_consumption() -> None:
    with pytest.raises(ValidationError):
        make_command(consumo_kwh="0")
