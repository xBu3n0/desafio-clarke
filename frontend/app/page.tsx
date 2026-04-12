"use client";

import { HeroSection } from "@/components/energy/HeroSection";
import { ResultsSection } from "@/components/energy/ResultsSection";
import { SearchPanel } from "@/components/energy/SearchPanel";
import { useEnergyComparison } from "@/lib/hooks/use-energy-comparison";

export default function Home() {
  const {
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
    onEstadoChange,
    onConsumoChange,
    onFonteChange,
  } = useEnergyComparison();

  return (
    <main className="mx-auto grid w-full max-w-6xl flex-1 gap-5 px-4 py-7 md:py-12">
      <HeroSection />

      <SearchPanel
        estados={estados}
        estadoId={estadoId}
        consumoKwh={consumoKwh}
        fonte={fonte}
        loading={loading}
        loadingEstados={loadingEstados}
        requestError={requestError}
        custoBase={custoBase}
        estadoSelecionado={estadoSelecionado}
        onCompare={compareOfertas}
        onEstadoChange={onEstadoChange}
        onConsumoChange={onConsumoChange}
        onFonteChange={onFonteChange}
      />

      <ResultsSection solucoes={solucoes} />
    </main>
  );
}
