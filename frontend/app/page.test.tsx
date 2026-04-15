import { render, screen } from "@testing-library/react";

import Home from "@/app/page";
import { useEnergyComparison } from "@/lib/hooks/use-energy-comparison";

jest.mock("@/lib/hooks/use-energy-comparison");

const mockUseEnergyComparison = useEnergyComparison as jest.MockedFunction<
  typeof useEnergyComparison
>;

describe("Home page", () => {
  it("renders the main sections using hook data", () => {
    // Arrange
    mockUseEnergyComparison.mockReturnValue({
      estados: [{ id: 1, nome: "Sao Paulo", sigla: "SP", tarifaBaseKwh: "0.89" }],
      estadoId: 1,
      consumoKwh: "",
      fonte: "graphql",
      loading: false,
      loadingEstados: false,
      requestError: null,
      custoBase: 0,
      estadoSelecionado: {
        id: 1,
        nome: "Sao Paulo",
        sigla: "SP",
        tarifaBaseKwh: "0.89",
      },
      solucoes: [
        { solucao: "GD", fornecedores: [] },
        { solucao: "Mercado Livre", fornecedores: [] },
      ],
      compareOfertas: jest.fn().mockResolvedValue(undefined),
      onEstadoChange: jest.fn(),
      onConsumoChange: jest.fn(),
      onFonteChange: jest.fn(),
    });

    // Act
    render(<Home />);

    // Assert
    expect(screen.getByText("Solução do desafio Clarke Energia")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Comparar ofertas" })).toBeInTheDocument();
    expect(screen.getByText("GD")).toBeInTheDocument();
  });
});
