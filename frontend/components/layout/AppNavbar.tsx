"use client";

import { Zap } from "lucide-react";

import { PLATFORM_LINKS } from "@/lib/constants/platform-links";
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
} from "@/components/ui/navigation-menu";
import { ThemeToggleButton } from "@/components/ui/theme-toggle-button";

export function AppNavbar() {
  return (
    <header className="sticky top-0 z-20 border-b border-(--line) bg-(--panel) py-3">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between gap-2 overflow-hidden px-4 whitespace-nowrap">
        <div className="flex shrink-0 items-center gap-2">
          <div
            className="inline-flex h-7 w-7 items-center justify-center border border-(--accent) bg-(--accent-soft) text-(--accent)"
            aria-hidden="true"
          >
            <Zap size={16} />
          </div>
          <div>
            <p className="m-0 text-xs tracking-wide text-(--muted) uppercase">
              Navegação
            </p>
            <p className="m-0 text-sm font-semibold">Clarke Energia</p>
          </div>
        </div>
        <div className="ml-auto flex items-center gap-2 overflow-hidden">
          <NavigationMenu aria-label="Acessos rapidos">
            <NavigationMenuList className="flex-nowrap overflow-x-auto overflow-y-hidden">
              {PLATFORM_LINKS.map((link) => (
                <NavigationMenuItem key={link.label}>
                  <NavigationMenuLink href={link.href} target="_blank" rel="noreferrer">
                    <link.icon size={14} aria-hidden="true" />
                    <span className="font-medium">{link.label}</span>
                  </NavigationMenuLink>
                </NavigationMenuItem>
              ))}
            </NavigationMenuList>
          </NavigationMenu>
          <ThemeToggleButton />
        </div>
      </div>
    </header>
  );
}
