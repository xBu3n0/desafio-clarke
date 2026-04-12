import strawberry


@strawberry.type(name="HealthStatus")
class HealthStatusType:
    status: str


@strawberry.type(name="Logo")
class LogoType:
    id: int
    url: str


@strawberry.type(name="Fornecedor")
class FornecedorType:
    id: int
    nome: str
    numero_clientes: int
    avaliacao_total: int
    numero_avaliacoes: int
    avaliacao_media: str
    logo: LogoType


@strawberry.type(name="Estado")
class EstadoType:
    id: int
    nome: str
    sigla: str
    tarifa_base_kwh: str


@strawberry.type(name="Oferta")
class OfertaType:
    id: int
    estado_id: int
    fornecedor_id: int
    solucao: str
    custo_kwh: str
    fornecedor: FornecedorType
