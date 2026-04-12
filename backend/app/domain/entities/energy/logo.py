from app.domain.base import DomainModel
from app.domain.value_objects import LogoId, UrlLogo


class Logo(DomainModel):
    id: LogoId | None
    url: UrlLogo
