import { render, screen } from "@testing-library/react";

import { AppNavbar } from "@/components/layout/AppNavbar";
import { PLATFORM_LINKS } from "@/lib/constants/platform-links";

describe("AppNavbar", () => {
  it("renders platform links and the theme toggle button", () => {
    // Arrange
    render(<AppNavbar />);

    // Act
    const links = screen.getAllByRole("link");
    const toggleButton = screen.getByRole("button", { name: "Alternar tema" });

    // Assert
    expect(links).toHaveLength(PLATFORM_LINKS.length);
    expect(toggleButton).toBeInTheDocument();
    expect(screen.getByText("Clarke Energia")).toBeInTheDocument();
  });
});
