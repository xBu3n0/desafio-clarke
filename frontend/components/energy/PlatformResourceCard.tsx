import { ExternalLink, type LucideIcon } from "lucide-react";

type PlatformResourceCardProps = {
  label: string;
  href: string;
  description: string;
  icon: LucideIcon;
  credentials?: {
    username: string;
    password: string;
  };
};

export function PlatformResourceCard({
  label,
  href,
  description,
  icon: Icon,
  credentials,
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
      {credentials ? (
        <div className="mt-2 flex flex-wrap items-center gap-1.5 text-xs text-(--muted)">
          <span>Credenciais:</span>
          <span className="border border-(--line) bg-(--bg) px-1.5 py-0.5">
            Usuário: <strong>{credentials.username}</strong>
          </span>
          <span className="border border-(--line) bg-(--bg) px-1.5 py-0.5">
            Senha: <strong>{credentials.password}</strong>
          </span>
        </div>
      ) : null}
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
