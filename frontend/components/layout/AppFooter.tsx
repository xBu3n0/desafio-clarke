import { ExternalLink } from "lucide-react";

import { CONTACT, CONTACT_LINKS } from "@/lib/constants/platform-links";

export function AppFooter() {
  return (
    <footer className="mt-auto border-t border-(--line) bg-(--panel)">
      <div className="mx-auto flex w-full max-w-6xl flex-wrap items-end justify-between gap-4 px-4 py-5 sm:items-start">
        <div>
          <p className="m-0 text-xs tracking-wide text-(--muted) uppercase">
            Desenvolvido por
          </p>
          <p className="mt-1 mb-0">{CONTACT.name}</p>
        </div>
        <div className="flex flex-col gap-2 md:flex-row">
          {CONTACT_LINKS.map((link) => (
            <a
              key={link.label}
              href={link.href}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1 border border-transparent px-2 py-1 text-(--text) no-underline hover:border-(--accent) hover:bg-(--accent-soft) hover:text-(--accent)"
            >
              <link.icon size={14} aria-hidden="true" />
              <span>{link.label}</span>
              <ExternalLink size={12} aria-hidden="true" />
            </a>
          ))}
        </div>
      </div>
    </footer>
  );
}
