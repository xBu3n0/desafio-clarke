from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.dto import OfertaSearchDTO
from app.application.ports import OfertaSearchRepository
from app.infrastructure.orm import OfertaModel


class SqlAlchemyOfertaSearchRepository(OfertaSearchRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def _to_search_dto(self, model: OfertaModel) -> OfertaSearchDTO:
        return OfertaSearchDTO(
            id=model.id,
            estado_id=model.estado_id,
            fornecedor_id=model.fornecedor_id,
            solucao=model.solucao,
            custo_kwh=model.custo_kwh,
        )

    def list_by_estado_id(self, estado_id: int) -> list[OfertaSearchDTO]:
        statement = (
            select(OfertaModel)
            .where(OfertaModel.estado_id == estado_id)
            .order_by(OfertaModel.id)
        )
        models = self._session.scalars(statement).all()
        return [self._to_search_dto(model) for model in models]
