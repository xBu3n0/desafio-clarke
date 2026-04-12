from __future__ import annotations

from collections.abc import Callable, Sequence
from decimal import Decimal

from app.application.dto import (
    EstadoSearchDTO,
    FornecedorSearchDTO,
    LogoSearchDTO,
    OfertaComFornecedorSearchDTO,
    OfertaSearchDTO,
)
from app.application.ports import UnitOfWork
from app.application.services import SearchQueryService
from app.domain.exceptions import EntityNotFoundError
from app.domain.value_objects import Solucao
from app.infrastructure.cache import RedisJsonCache

UnitOfWorkFactory = Callable[[], UnitOfWork]


class SqlAlchemySearchQueryService(SearchQueryService):
    def __init__(self, uow_factory: UnitOfWorkFactory) -> None:
        self._uow_factory = uow_factory

    def list_estados(self) -> Sequence[EstadoSearchDTO]:
        with self._uow_factory() as uow:
            return list(uow.estados.list_all())

    def get_estado(self, estado_id: int) -> EstadoSearchDTO | None:
        with self._uow_factory() as uow:
            return uow.estados.get_by_id(estado_id)

    def list_ofertas_by_estado(
        self,
        *,
        estado_id: int,
        page: int,
        per_page: int,
    ) -> tuple[int, Sequence[OfertaComFornecedorSearchDTO]]:
        offset = (page - 1) * per_page

        with self._uow_factory() as uow:
            estado = uow.estados.get_by_id(estado_id)
            if estado is None:
                raise EntityNotFoundError("estado was not found")

            all_ofertas = list(uow.ofertas.list_by_estado_id(estado_id))
            total = len(all_ofertas)
            ofertas = all_ofertas[offset : offset + per_page]

            fornecedor_ids = self._extract_fornecedor_ids(ofertas)
            fornecedores = uow.fornecedores.list_by_ids(fornecedor_ids)
            fornecedores_index = {
                fornecedor.id: fornecedor for fornecedor in fornecedores
            }

        result: list[OfertaComFornecedorSearchDTO] = []
        for oferta in ofertas:
            fornecedor = fornecedores_index.get(oferta.fornecedor_id)
            if fornecedor is None:
                continue

            result.append(
                OfertaComFornecedorSearchDTO(
                    id=oferta.id,
                    estado_id=oferta.estado_id,
                    fornecedor_id=oferta.fornecedor_id,
                    solucao=oferta.solucao,
                    custo_kwh=oferta.custo_kwh,
                    fornecedor=fornecedor,
                )
            )

        return total, result

    def fornecedores_count(self) -> int:
        with self._uow_factory() as uow:
            return uow.fornecedores.count()

    def _extract_fornecedor_ids(self, ofertas: Sequence[OfertaSearchDTO]) -> list[int]:
        seen: set[int] = set()
        fornecedor_ids: list[int] = []
        for oferta in ofertas:
            fornecedor_id = oferta.fornecedor_id
            if fornecedor_id in seen:
                continue
            seen.add(fornecedor_id)
            fornecedor_ids.append(fornecedor_id)
        return fornecedor_ids


class CachedSearchQueryService(SearchQueryService):
    def __init__(
        self,
        delegate: SearchQueryService,
        cache: RedisJsonCache,
    ) -> None:
        self._delegate = delegate
        self._cache = cache

    def list_estados(self) -> Sequence[EstadoSearchDTO]:
        cache_key = "graphql:list_estados"
        cached = self._cache.get_json(cache_key)
        if isinstance(cached, list):
            return [self._deserialize_estado(item) for item in cached]

        estados = list(self._delegate.list_estados())
        self._cache.set_json(
            cache_key, [self._serialize_estado(item) for item in estados]
        )
        return estados

    def get_estado(self, estado_id: int) -> EstadoSearchDTO | None:
        cache_key = f"graphql:get_estado:{estado_id}"
        cached = self._cache.get_json(cache_key)
        if isinstance(cached, dict):
            return self._deserialize_estado(cached)

        estado = self._delegate.get_estado(estado_id)
        if estado is None:
            return None
        self._cache.set_json(cache_key, self._serialize_estado(estado))
        return estado

    def list_ofertas_by_estado(
        self,
        *,
        estado_id: int,
        page: int,
        per_page: int,
    ) -> tuple[int, Sequence[OfertaComFornecedorSearchDTO]]:
        cache_key = f"graphql:list_ofertas_by_estado:{estado_id}:{page}:{per_page}"
        cached = self._cache.get_json(cache_key)
        if isinstance(cached, dict):
            total = int(cached.get("total", 0))
            items = cached.get("items", [])
            if isinstance(items, list):
                return total, [self._deserialize_oferta(item) for item in items]

        total, ofertas = self._delegate.list_ofertas_by_estado(
            estado_id=estado_id,
            page=page,
            per_page=per_page,
        )
        self._cache.set_json(
            cache_key,
            {
                "total": total,
                "items": [self._serialize_oferta(item) for item in ofertas],
            },
        )
        return total, ofertas

    def fornecedores_count(self) -> int:
        cache_key = "graphql:fornecedores_count"
        cached = self._cache.get_json(cache_key)
        if isinstance(cached, int):
            return cached
        if isinstance(cached, str) and cached.isdigit():
            return int(cached)

        total = self._delegate.fornecedores_count()
        self._cache.set_json(cache_key, total)
        return total

    def _serialize_estado(self, item: EstadoSearchDTO) -> dict[str, object]:
        return {
            "id": item.id,
            "nome": item.nome,
            "sigla": item.sigla,
            "tarifa_base_kwh": str(item.tarifa_base_kwh),
        }

    def _deserialize_estado(self, payload: dict[str, object]) -> EstadoSearchDTO:
        return EstadoSearchDTO(
            id=int(payload["id"]),
            nome=str(payload["nome"]),
            sigla=str(payload["sigla"]),
            tarifa_base_kwh=Decimal(str(payload["tarifa_base_kwh"])),
        )

    def _serialize_oferta(
        self, item: OfertaComFornecedorSearchDTO
    ) -> dict[str, object]:
        return {
            "id": item.id,
            "estado_id": item.estado_id,
            "fornecedor_id": item.fornecedor_id,
            "solucao": item.solucao.value,
            "custo_kwh": str(item.custo_kwh),
            "fornecedor": self._serialize_fornecedor(item.fornecedor),
        }

    def _deserialize_oferta(
        self,
        payload: dict[str, object],
    ) -> OfertaComFornecedorSearchDTO:
        fornecedor_payload = payload["fornecedor"]
        assert isinstance(fornecedor_payload, dict)
        return OfertaComFornecedorSearchDTO(
            id=int(payload["id"]),
            estado_id=int(payload["estado_id"]),
            fornecedor_id=int(payload["fornecedor_id"]),
            solucao=Solucao.create(str(payload["solucao"])),
            custo_kwh=Decimal(str(payload["custo_kwh"])),
            fornecedor=self._deserialize_fornecedor(fornecedor_payload),
        )

    def _serialize_fornecedor(self, item: FornecedorSearchDTO) -> dict[str, object]:
        return {
            "id": item.id,
            "nome": item.nome,
            "logo": {
                "id": item.logo.id,
                "url": item.logo.url,
            },
            "numero_clientes": item.numero_clientes,
            "avaliacao_total": item.avaliacao_total,
            "numero_avaliacoes": item.numero_avaliacoes,
            "avaliacao_media": str(item.avaliacao_media),
        }

    def _deserialize_fornecedor(
        self,
        payload: dict[str, object],
    ) -> FornecedorSearchDTO:
        logo_payload = payload["logo"]
        assert isinstance(logo_payload, dict)
        return FornecedorSearchDTO(
            id=int(payload["id"]),
            nome=str(payload["nome"]),
            logo=LogoSearchDTO(
                id=int(logo_payload["id"]),
                url=str(logo_payload["url"]),
            ),
            numero_clientes=int(payload["numero_clientes"]),
            avaliacao_total=int(payload["avaliacao_total"]),
            numero_avaliacoes=int(payload["numero_avaliacoes"]),
            avaliacao_media=Decimal(str(payload["avaliacao_media"])),
        )
