"use client";

import { Moon, Sun } from "lucide-react";
import { useEffect, useReducer, useSyncExternalStore } from "react";

type Theme = "light" | "dark";

const THEME_STORAGE_KEY = "clarke:theme";
const THEME_COOKIE_KEY = "clarke_theme";

function resolveInitialTheme(): Theme {
  if (typeof window === "undefined") {
    return "light";
  }

  if (document.documentElement.classList.contains("theme-dark")) {
    return "dark";
  }

  if (document.documentElement.classList.contains("theme-light")) {
    return "light";
  }

  const savedTheme = window.localStorage.getItem(THEME_STORAGE_KEY);
  if (savedTheme === "dark" || savedTheme === "light") {
    return savedTheme;
  }

  if (typeof window.matchMedia === "function") {
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  return "light";
}

function applyTheme(theme: Theme): void {
  const root = document.documentElement;
  root.classList.remove("theme-light", "theme-dark");
  root.classList.add(theme === "dark" ? "theme-dark" : "theme-light");
  root.setAttribute("data-theme", theme);
}

export function ThemeToggleButton() {
  const isClient = useSyncExternalStore(
    () => () => {},
    () => true,
    () => false,
  );
  const [, forceRender] = useReducer((value: number) => value + 1, 0);

  useEffect(() => {
    if (isClient) {
      applyTheme(resolveInitialTheme());
      forceRender();
    }
  }, [isClient]);

  const theme: Theme | null = isClient
    ? (document.documentElement.classList.contains("theme-dark") ? "dark" : "light")
    : null;

  const toggleTheme = () => {
    const currentTheme: Theme =
      theme === null
        ? document.documentElement.classList.contains("theme-dark")
          ? "dark"
          : "light"
        : theme;
    const nextTheme: Theme = currentTheme === "dark" ? "light" : "dark";
    window.localStorage.setItem(THEME_STORAGE_KEY, nextTheme);
    document.cookie = `${THEME_COOKIE_KEY}=${nextTheme}; path=/; max-age=31536000; samesite=lax`;
    applyTheme(nextTheme);
    forceRender();
  };

  return (
    <button
      type="button"
      onClick={toggleTheme}
      className="inline-flex min-h-7 items-center border border-(--line) bg-(--bg) px-2 py-1 text-xs text-(--text) transition hover:border-(--accent) hover:text-(--accent)"
      aria-label="Alternar tema"
      title="Alternar tema"
    >
      {theme === null ? (
        <span className="inline-block h-[14px] w-[14px]" aria-hidden="true" />
      ) : theme === "light" ? (
        <Sun size={14} />
      ) : (
        <Moon size={14} />
      )}
    </button>
  );
}
