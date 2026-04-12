import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { HeroSection } from "@/components/energy/HeroSection";

describe("HeroSection", () => {
  it("renders overview and toggles accordion sections", async () => {
    // Arrange
    const user = userEvent.setup();
    render(<HeroSection />);

    // Act
    const componentsButton = screen.getByRole("button", {
      name: "Componentes da aplicação",
    });
    await user.click(componentsButton);

    // Assert
    expect(screen.getByText("Solução do desafio Clarke Energia")).toBeInTheDocument();
    expect(
      screen.getByText("Compare fornecedores por estado e avalie custo e economia."),
    ).toBeInTheDocument();
    expect(componentsButton).toHaveAttribute("aria-expanded", "true");
    expect(screen.getByText("Backend API")).toBeInTheDocument();
  });
});
