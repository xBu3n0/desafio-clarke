import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { SearchPanel } from "@/components/energy/SearchPanel";

const baseEstado = {
  id: 1,
  nome: "Sao Paulo",
  sigla: "SP",
  tarifaBaseKwh: "0.89",
};

describe("SearchPanel", () => {
  it("shows validation when consumo is invalid and does not call compare", async () => {
    // Arrange
    const onCompare = jest.fn().mockResolvedValue(undefined);
    const user = userEvent.setup();

    render(
      <SearchPanel
        estados={[baseEstado]}
        estadoId={1}
        consumoKwh=""
        fonte="graphql"
        loading={false}
        loadingEstados={false}
        requestError={null}
        custoBase={0}
        estadoSelecionado={baseEstado}
        onCompare={onCompare}
        onEstadoChange={jest.fn()}
        onConsumoChange={jest.fn()}
        onFonteChange={jest.fn()}
      />,
    );

    // Act
    await user.click(screen.getByRole("button", { name: "Comparar ofertas" }));

    // Assert
    expect(
      screen.getByText("Consumo mensal deve ser maior que zero."),
    ).toBeInTheDocument();
    expect(onCompare).not.toHaveBeenCalled();
  });

  it("calls compare with parsed values when form is valid", async () => {
    // Arrange
    const onCompare = jest.fn().mockResolvedValue(undefined);
    const user = userEvent.setup();

    render(
      <SearchPanel
        estados={[baseEstado]}
        estadoId={1}
        consumoKwh="30000"
        fonte="graphql"
        loading={false}
        loadingEstados={false}
        requestError={null}
        custoBase={0}
        estadoSelecionado={baseEstado}
        onCompare={onCompare}
        onEstadoChange={jest.fn()}
        onConsumoChange={jest.fn()}
        onFonteChange={jest.fn()}
      />,
    );

    // Act
    await user.click(screen.getByRole("button", { name: "Comparar ofertas" }));

    // Assert
    expect(onCompare).toHaveBeenCalledWith(1, 30000);
  });
});
