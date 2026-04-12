from dataclasses import dataclass

from app.domain.value_objects import ConsumoKwh, SiglaEstado


@dataclass(frozen=True, slots=True)
class BuscarOfertasCommand:
    sigla_estado: SiglaEstado
    consumo_kwh: ConsumoKwh


@dataclass(frozen=True, slots=True)
class ComparacaoFornecedorDTO:
    fornecedor_id: int
    fornecedor_nome: str
    logo_url: str
    custo_kwh: str
    custo_mensal: str
    economia: str
    economia_percentual: str
    numero_clientes: int
    avaliacao_media: str

    def to_dict(self) -> dict[str, object]:
        return {
            "fornecedor_id": self.fornecedor_id,
            "fornecedor_nome": self.fornecedor_nome,
            "logo_url": self.logo_url,
            "custo_kwh": self.custo_kwh,
            "custo_mensal": self.custo_mensal,
            "economia": self.economia,
            "economia_percentual": self.economia_percentual,
            "numero_clientes": self.numero_clientes,
            "avaliacao_media": self.avaliacao_media,
        }


@dataclass(frozen=True, slots=True)
class ResumoSolucaoDTO:
    solucao: str
    fornecedores: list[ComparacaoFornecedorDTO]

    def to_dict(self) -> dict[str, object]:
        return {
            "solucao": self.solucao,
            "fornecedores": [fornecedor.to_dict() for fornecedor in self.fornecedores],
        }


@dataclass(frozen=True, slots=True)
class ResultadoBuscaDTO:
    estado_id: int
    estado_nome: str
    estado_sigla: str
    consumo_kwh: str
    tarifa_base_kwh: str
    custo_base: str
    solucoes: list[ResumoSolucaoDTO]

    def to_dict(self) -> dict[str, object]:
        return {
            "estado_id": self.estado_id,
            "estado_nome": self.estado_nome,
            "estado_sigla": self.estado_sigla,
            "consumo_kwh": self.consumo_kwh,
            "tarifa_base_kwh": self.tarifa_base_kwh,
            "custo_base": self.custo_base,
            "solucoes": [solucao.to_dict() for solucao in self.solucoes],
        }
