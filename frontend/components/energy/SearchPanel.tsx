import { useState, type SyntheticEvent } from "react";
import { z } from "zod";

import { Field } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { currencyFormatter } from "@/lib/energy/formatters";
import type { DataSource, Estado, FormErrors } from "@/lib/types/energy";

type SearchPanelProps = {
  estados: Estado[];
  estadoId: number | null;
  consumoKwh: string;
  fonte: DataSource;
  loading: boolean;
  loadingEstados: boolean;
  requestError: string | null;
  custoBase: number;
  estadoSelecionado: Estado | null;
  onCompare: (estadoId: number, consumoKwh: number) => Promise<void>;
  onEstadoChange: (estadoId: number) => void;
  onConsumoChange: (consumo: string) => void;
  onFonteChange: (fonte: DataSource) => void;
};

const searchFormSchema = z.object({
  estadoId: z.preprocess(
    (value) => (typeof value === "number" ? value : 0),
    z.number().int().positive("Selecione um estado."),
  ),
  consumoKwh: z.coerce
    .number()
    .int("Consumo mensal deve ser um número inteiro.")
    .positive("Consumo mensal deve ser maior que zero."),
});

export function SearchPanel({
  estados,
  estadoId,
  consumoKwh,
  fonte,
  loading,
  loadingEstados,
  requestError,
  custoBase,
  estadoSelecionado,
  onCompare,
  onEstadoChange,
  onConsumoChange,
  onFonteChange,
}: SearchPanelProps) {
  const [formErrors, setFormErrors] = useState<FormErrors>({});
  const hasConsumoInformado = consumoKwh.trim() !== "" && Number.isFinite(custoBase);

  const handleSubmit = async (event: SyntheticEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFormErrors({});

    const parsedForm = searchFormSchema.safeParse({
      estadoId,
      consumoKwh,
    });

    if (!parsedForm.success) {
      const nextFormErrors: FormErrors = {};

      for (const issue of parsedForm.error.issues) {
        const field = issue.path[0];
        if (field === "estadoId" || field === "consumoKwh") {
          nextFormErrors[field] = issue.message;
        }
      }

      setFormErrors(nextFormErrors);
      return;
    }

    await onCompare(parsedForm.data.estadoId, parsedForm.data.consumoKwh);
  };

  return (
    <section className="border border-(--line) bg-(--panel) p-4">
      <form
        onSubmit={handleSubmit}
        className="grid grid-cols-1 items-end gap-3 md:grid-cols-2 lg:grid-cols-4"
      >
        <Field label="Estado" error={formErrors.estadoId}>
          <Select
            hasError={Boolean(formErrors.estadoId)}
            value={estadoId ?? ""}
            onChange={(event) => {
              onEstadoChange(Number(event.target.value));
            }}
            disabled={loadingEstados}
          >
            {estados.map((estado) => (
              <option key={estado.id} value={estado.id}>
                {estado.sigla} - {estado.nome}
              </option>
            ))}
          </Select>
        </Field>

        <Field label="Consumo mensal (kWh)" error={formErrors.consumoKwh}>
          <Input
            hasError={Boolean(formErrors.consumoKwh)}
            type="number"
            min="1"
            step="1"
            value={consumoKwh}
            onChange={(event) => {
              onConsumoChange(event.target.value);
            }}
            placeholder="30000"
          />
        </Field>

        <Field label="Fonte de dados">
          <Select
            value={fonte}
            onChange={(event) => onFonteChange(event.target.value as DataSource)}
          >
            <option value="rest">REST</option>
            <option value="graphql">GraphQL</option>
          </Select>
        </Field>

        <div className="grid gap-1.5">
          <span className="invisible text-xs tracking-wide uppercase">&nbsp;</span>
          <button
            type="submit"
            className="min-h-11 cursor-pointer border border-(--accent) bg-(--accent) px-4 py-2 text-(--accent-contrast) disabled:cursor-not-allowed disabled:opacity-60"
            disabled={loading}
          >
            {loading ? "Consultando..." : "Comparar ofertas"}
          </button>
          <p className="invisible mt-1 mb-0 min-h-4 text-xs">&nbsp;</p>
        </div>
      </form>

      {estadoSelecionado && (
        <div className="mt-4 flex flex-wrap gap-6 border-t border-(--line) pt-4">
          <div>
            <p className="m-0 text-xs tracking-wide text-(--muted) uppercase">
              Tarifa base
            </p>
            <p className="mt-1 mb-0">
              {currencyFormatter.format(Number(estadoSelecionado.tarifaBaseKwh))}/kWh
            </p>
          </div>
          <div>
            <p className="m-0 text-xs tracking-wide text-(--muted) uppercase">
              Custo base estimado
            </p>
            {hasConsumoInformado ? (
              <p className="mt-1 mb-0">{currencyFormatter.format(custoBase)}</p>
            ) : (
              <p className="mt-1 mb-0">
                Informe o consumo mensal para calcular.
              </p>
            )}
          </div>
        </div>
      )}

      {requestError && <p className="mt-4 mb-0 text-(--danger)">{requestError}</p>}
    </section>
  );
}
