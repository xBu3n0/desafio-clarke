import { ExternalLink, type LucideIcon } from "lucide-react";

type PlatformResourceCardProps = {
  label: string;
  href: string;
  description: string;
  icon: LucideIcon;
};

export function PlatformResourceCard({
  label,
  href,
  description,
  icon: Icon,
}: PlatformResourceCardProps) {
  return (
    <article className="border border-(--line) bg-(--panel) p-3">
      <div className="flex items-start gap-2">
        <Icon size={16} className="mt-0.5 text-(--accent)" aria-hidden="true" />
        <div className="grid gap-1">
          <h2 className="m-0 text-sm">{label}</h2>
          <p className="m-0 text-sm text-(--muted)">{description}</p>
        </div>
      </div>
      <a
        href={href}
        target="_blank"
        rel="noreferrer"
        className="mt-3 inline-flex min-h-8 items-center gap-1 border border-(--line) bg-(--bg) px-2 py-1 text-xs text-(--text) no-underline transition hover:border-(--accent) hover:text-(--accent)"
      >
        Acessar
        <ExternalLink size={12} aria-hidden="true" />
      </a>
    </article>
  );
}
