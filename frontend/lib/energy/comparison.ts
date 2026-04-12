import type { OfertaNormalizada, SolucaoComparacao } from "@/lib/types/energy";

const SOLUCOES: Array<"GD" | "Mercado Livre"> = ["GD", "Mercado Livre"];

export function parseNumber(value: string | number): number {
  return typeof value === "number" ? value : Number(value);
}

export function parseInteger(value: string): number {
  return Number.parseInt(value, 10);
}

export function formatPercent(value: number): string {
  const sign = value >= 0 ? "+" : "";
  return `${sign}${(value * 100).toFixed(2)}%`;
}

export function buildComparacao(
  ofertas: OfertaNormalizada[],
  consumoKwh: number,
  tarifaBaseKwh: number,
): SolucaoComparacao[] {
  const custoBase = consumoKwh * tarifaBaseKwh;

  return SOLUCOES.map((solucao) => {
    const fornecedores = ofertas
      .filter((oferta) => oferta.solucao === solucao)
      .map((oferta) => {
        const custoFornecedor = consumoKwh * oferta.custoKwh;
        const economia = custoBase - custoFornecedor;
        const economiaPercentual = custoBase === 0 ? 0 : economia / custoBase;

        return {
          id: oferta.fornecedor.id,
          nome: oferta.fornecedor.nome,
          numeroClientes: oferta.fornecedor.numeroClientes,
          avaliacaoMedia: oferta.fornecedor.avaliacaoMedia,
          logoUrl: oferta.fornecedor.logoUrl,
          custoKwh: oferta.custoKwh,
          custoFornecedor,
          economia,
          economiaPercentual,
        };
      })
      .sort((a, b) => b.economia - a.economia);

    return { solucao, fornecedores };
  });
}
