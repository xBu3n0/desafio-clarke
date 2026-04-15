import { useEffect, useMemo, useState } from "react";

import {
  fetchEstadosBySource,
  fetchOfertasBySource,
} from "@/lib/clients/energy-client";
import {
  buildComparacao,
  parseInteger,
  parseNumber,
} from "@/lib/energy/comparison";
import type {
  DataSource,
  Estado,
  SolucaoComparacao,
} from "@/lib/types/energy";

const DATA_SOURCE_STORAGE_KEY = "clarke:data-source";

export function useEnergyComparison() {
  const [estados, setEstados] = useState<Estado[]>([]);
  const [estadoId, setEstadoId] = useState<number | null>(null);
  const [consumoKwh, setConsumoKwh] = useState("");
  const [fonte, setFonte] = useState<DataSource>(() => {
    if (typeof window === "undefined") {
      return "graphql";
    }

    const savedFonte = window.localStorage.getItem(DATA_SOURCE_STORAGE_KEY);
    return savedFonte === "rest" ? "rest" : "graphql";
  });
  const [loading, setLoading] = useState(false);
  const [loadingEstados, setLoadingEstados] = useState(true);
  const [requestError, setRequestError] = useState<string | null>(null);
  const [solucoes, setSolucoes] = useState<SolucaoComparacao[]>([]);

  useEffect(() => {
    const loadEstados = async () => {
      setLoadingEstados(true);

      try {
        const data = await fetchEstadosBySource(fonte);
        setRequestError(null);
        setEstados(data);
        setEstadoId((currentEstadoId) => {
          if (currentEstadoId === null) {
            return data[0]?.id ?? null;
          }

          return data.some((estado) => estado.id === currentEstadoId)
            ? currentEstadoId
            : (data[0]?.id ?? null);
        });
      } catch {
        setRequestError("Não foi possível carregar os estados.");
      } finally {
        setLoadingEstados(false);
      }
    };

    loadEstados();
  }, [fonte]);

  useEffect(() => {
    window.localStorage.setItem(DATA_SOURCE_STORAGE_KEY, fonte);
  }, [fonte]);

  const estadoSelecionado = useMemo(
    () => estados.find((estado) => estado.id === estadoId) ?? null,
    [estados, estadoId],
  );

  const custoBase = useMemo(() => {
    if (!estadoSelecionado) return 0;
    const tarifa = parseNumber(estadoSelecionado.tarifaBaseKwh);
    const consumo = parseInteger(consumoKwh);
    return consumo * tarifa;
  }, [estadoSelecionado, consumoKwh]);

  const compareOfertas = async (estadoIdParaConsulta: number, consumoKwh: number) => {
    setRequestError(null);

    setLoading(true);
    try {
      const ofertas = await fetchOfertasBySource(fonte, estadoIdParaConsulta);
      const estadoBase =
        estados.find((estado) => estado.id === estadoIdParaConsulta) ?? null;
      const comparacao = buildComparacao(
        ofertas,
        consumoKwh,
        parseNumber(estadoBase?.tarifaBaseKwh ?? 0),
      );
      setSolucoes(comparacao);
    } catch {
      setRequestError("Não foi possível buscar as ofertas.");
      setSolucoes([]);
    } finally {
      setLoading(false);
    }
  };

  return {
    estados,
    estadoId,
    consumoKwh,
    fonte,
    loading,
    loadingEstados,
    requestError,
    custoBase,
    estadoSelecionado,
    solucoes,
    compareOfertas,
    onEstadoChange: (nextEstadoId: number) => {
      setEstadoId(nextEstadoId);
    },
    onConsumoChange: (nextConsumoKwh: string) => {
      setConsumoKwh(nextConsumoKwh);
    },
    onFonteChange: (nextFonte: DataSource) => {
      setFonte(nextFonte);
    },
  };
}
