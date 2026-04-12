from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.application.dto import FornecedorSearchDTO, LogoSearchDTO
from app.application.ports import FornecedorSearchRepository
from app.infrastructure.orm import FornecedorModel


class SqlAlchemyFornecedorSearchRepository(FornecedorSearchRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def _to_search_dto(self, model: FornecedorModel) -> FornecedorSearchDTO:
        return FornecedorSearchDTO(
            id=model.id,
            nome=model.nome,
            logo=LogoSearchDTO(id=model.logo.id, url=model.logo.url),
            numero_clientes=model.numero_clientes,
            avaliacao_total=model.avaliacao_total,
            numero_avaliacoes=model.numero_avaliacoes,
            avaliacao_media=model.avaliacao_media,
        )

    def list_by_ids(
        self,
        fornecedor_ids: list[int],
    ) -> list[FornecedorSearchDTO]:
        if not fornecedor_ids:
            return []

        statement = (
            select(FornecedorModel)
            .where(FornecedorModel.id.in_(fornecedor_ids))
            .options(selectinload(FornecedorModel.logo))
            .order_by(FornecedorModel.id)
        )
        models = self._session.scalars(statement).all()
        return [self._to_search_dto(model) for model in models]

    def count(self) -> int:
        return self._session.query(FornecedorModel).count()
