from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.dto import EstadoSearchDTO
from app.application.ports import EstadoSearchRepository
from app.infrastructure.orm import EstadoModel


class SqlAlchemyEstadoSearchRepository(EstadoSearchRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def _to_search_dto(self, model: EstadoModel) -> EstadoSearchDTO:
        return EstadoSearchDTO(
            id=model.id,
            nome=model.nome,
            sigla=model.sigla,
            tarifa_base_kwh=model.tarifa_base_kwh,
        )

    def get_by_sigla(self, sigla: str) -> EstadoSearchDTO | None:
        statement = select(EstadoModel).where(EstadoModel.sigla == sigla)
        model = self._session.scalar(statement)
        return None if model is None else self._to_search_dto(model)

    def get_by_id(self, estado_id: int) -> EstadoSearchDTO | None:
        model = self._session.get(EstadoModel, estado_id)
        return None if model is None else self._to_search_dto(model)

    def list_all(self) -> list[EstadoSearchDTO]:
        statement = select(EstadoModel).order_by(EstadoModel.nome)
        models = self._session.scalars(statement).all()
        return [self._to_search_dto(model) for model in models]
