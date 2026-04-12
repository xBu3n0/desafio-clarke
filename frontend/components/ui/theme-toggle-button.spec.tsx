import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { ThemeToggleButton } from "./theme-toggle-button";

describe("ThemeToggleButton", () => {
  beforeEach(() => {
    window.localStorage.clear();
    document.cookie = "clarke_theme=; max-age=0; path=/";
    document.documentElement.className = "theme-light h-full antialiased";
    document.documentElement.setAttribute("data-theme", "light");
  });

  it("toggles the document theme and persists the choice", async () => {
    const user = userEvent.setup();

    render(<ThemeToggleButton />);

    const button = screen.getByRole("button", { name: "Alternar tema" });
    expect(button).toBeInTheDocument();

    await user.click(button);

    expect(window.localStorage.getItem("clarke:theme")).toBe("dark");
    expect(document.documentElement).toHaveClass("theme-dark");
    expect(document.documentElement).toHaveAttribute("data-theme", "dark");
    expect(document.cookie).toContain("clarke_theme=dark");
  });
});
