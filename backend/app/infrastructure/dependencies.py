from __future__ import annotations

from collections.abc import Callable

from sqlalchemy.orm import Session

from app.application.services import SearchQueryService
from app.infrastructure.cache import RedisJsonCache
from app.infrastructure.services import (
    CachedSearchQueryService,
    SqlAlchemySearchQueryService,
)
from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork


def build_search_query_service(
    *,
    session_provider: Callable[[], Session],
) -> SearchQueryService:
    def uow_factory() -> SqlAlchemyUnitOfWork:
        return SqlAlchemyUnitOfWork(session_provider)

    base_service = SqlAlchemySearchQueryService(uow_factory=uow_factory)
    return CachedSearchQueryService(
        delegate=base_service,
        cache=RedisJsonCache(),
    )
