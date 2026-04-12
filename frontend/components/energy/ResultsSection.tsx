import Image from "next/image";

import { formatPercent } from "@/lib/energy/comparison";
import { currencyFormatter } from "@/lib/energy/formatters";
import type { SolucaoComparacao } from "@/lib/types/energy";

type ResultsSectionProps = {
  solucoes: SolucaoComparacao[];
};

export function ResultsSection({ solucoes }: ResultsSectionProps) {
  return (
    <section className="grid gap-3">
      {solucoes.map((solucao) => {
        const melhorEconomia = solucao.fornecedores[0]?.economia ?? null;
        return (
          <article
            key={solucao.solucao}
            className="border border-(--line) bg-(--panel) p-4"
          >
            <header className="mb-3 flex flex-wrap justify-between gap-3 border-b border-(--line) pb-3">
              <div>
                <p className="m-0 text-xs tracking-wide text-(--muted) uppercase">
                  Solução
                </p>
                <h2 className="m-0">{solucao.solucao}</h2>
              </div>
              <div className="text-left sm:text-right">
                <p className="m-0 text-xs tracking-wide text-(--muted) uppercase">
                  Melhor economia
                </p>
                <p className="m-0">
                  {melhorEconomia === null
                    ? "Indisponível"
                    : currencyFormatter.format(melhorEconomia)}
                </p>
              </div>
            </header>

            {solucao.fornecedores.length === 0 ? (
              <p className="m-0 text-(--muted)">
                Não há fornecedores para esta solução no estado selecionado.
              </p>
            ) : (
              <div className="grid gap-2.5">
                {solucao.fornecedores.map((fornecedor) => (
                  <article
                    key={fornecedor.id}
                    className={`grid grid-cols-1 gap-4 border p-3 md:grid-cols-2 ${
                      fornecedor.economia >= 0
                        ? "border-(--positive-line) bg-(--positive-bg)"
                        : "border-(--negative-line) bg-(--negative-bg)"
                    }`}
                  >
                    <div className="flex items-center gap-2.5">
                      <Image
                        src={fornecedor.logoUrl}
                        alt={`Logo ${fornecedor.nome}`}
                        className="h-8 w-8 rounded-full border border-(--line) bg-(--panel) object-cover"
                        width={34}
                        height={34}
                      />
                      <div>
                        <h3 className="m-0 text-sm">{fornecedor.nome}</h3>
                        <p className="mt-0.5 mb-0 text-xs text-(--muted)">
                          {fornecedor.numeroClientes} clientes · nota{" "}
                          {fornecedor.avaliacaoMedia.toFixed(1)}
                        </p>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 gap-x-3 gap-y-2 sm:grid-cols-2">
                      <p className="m-0 grid gap-0.5 text-sm">
                        <span className="text-xs tracking-wide text-(--muted) uppercase">
                          Custo/kWh
                        </span>
                        {currencyFormatter.format(fornecedor.custoKwh)}
                      </p>
                      <p className="m-0 grid gap-0.5 text-sm">
                        <span className="text-xs tracking-wide text-(--muted) uppercase">
                          Custo estimado
                        </span>
                        {currencyFormatter.format(fornecedor.custoFornecedor)}
                      </p>
                      <p className="m-0 grid gap-0.5 text-sm">
                        <span className="text-xs tracking-wide text-(--muted) uppercase">
                          Economia
                        </span>
                        <strong
                          className={
                            fornecedor.economia >= 0
                              ? "text-(--positive-text)"
                              : "text-(--negative-text)"
                          }
                        >
                          {currencyFormatter.format(fornecedor.economia)}
                        </strong>
                      </p>
                      <p className="m-0 grid gap-0.5 text-sm">
                        <span className="text-xs tracking-wide text-(--muted) uppercase">
                          Economia %
                        </span>
                        <strong
                          className={
                            fornecedor.economiaPercentual >= 0
                              ? "text-(--positive-text)"
                              : "text-(--negative-text)"
                          }
                        >
                          {formatPercent(fornecedor.economiaPercentual)}
                        </strong>
                      </p>
                    </div>
                  </article>
                ))}
              </div>
            )}
          </article>
        );
      })}
    </section>
  );
}
