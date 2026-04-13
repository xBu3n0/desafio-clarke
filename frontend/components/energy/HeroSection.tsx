import { SearchCheck } from "lucide-react";

import { PLATFORM_LINKS } from "@/lib/constants/platform-links";
import { PlatformResourceCard } from "@/components/energy/PlatformResourceCard";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const APP_COMPONENTS = [
  {
    title: "Frontend",
    description:
      "Interface em Next.js para consulta de estados, comparação de ofertas e visualização de economia.",
  },
  {
    title: "Backend API",
    description:
      "Serviços REST e GraphQL para estados e ofertas, com regras de domínio e integração com banco.",
  },
  {
    title: "Observabilidade",
    description:
      "Métricas expostas para Prometheus e dashboards no Grafana para acompanhar saúde e uso da aplicação.",
  },
  {
    title: "Armazenamento",
    description:
      "MinIO para servir ativos como logos e arquivos auxiliares usados no fluxo da plataforma.",
  },
] as const;

const CREDENTIALS_BY_LABEL: Record<
  string,
  { username: string; password: string } | undefined
> = {
  "MinIO Console": {
    username: "minioadmin",
    password: "minioadmin",
  },
  "Grafana": {
    username: "admin",
    password: "admin",
  },
};

export function HeroSection() {
  return (
    <section className="grid gap-3 border border-(--line) bg-(--panel) p-6">
      <p className="m-0 text-xs tracking-wide text-(--muted) uppercase">
        Clarke Energia
      </p>
      <h1 className="m-0 text-3xl leading-tight md:text-4xl">
        Solução do desafio Clarke Energia
      </h1>
      <div className="grid gap-1 border border-(--line) bg-(--bg) p-3">
        <span className="text-sm font-semibold">Visão geral</span>
        <p className="m-0 max-w-3xl text-(--muted)">
          Aplicação para consulta e comparação de ofertas de energia, com APIs,
          observabilidade e armazenamento integrados em um único ambiente.
        </p>
        <div className="flex items-start gap-2 border border-(--line) bg-(--panel) p-2.5">
          <SearchCheck size={16} className="mt-0.5 text-(--accent)" aria-hidden="true" />
          <p className="m-0 text-sm text-(--muted)">
            Compare fornecedores por estado e avalie custo e economia.
          </p>
        </div>
      </div>

      <Accordion type="single" collapsible className="grid gap-2">

        <AccordionItem value="components" className="bg-(--bg)">
          <AccordionTrigger>
            <span className="text-sm font-semibold">Componentes da aplicação</span>
          </AccordionTrigger>
          <AccordionContent>
            <div className="grid grid-cols-1 gap-2 md:grid-cols-2">
              {APP_COMPONENTS.map((component) => (
                <article
                  key={component.title}
                  className="border border-(--line) bg-(--panel) p-3"
                >
                  <h2 className="m-0 text-sm">{component.title}</h2>
                  <p className="mt-1 mb-0 text-sm text-(--muted)">
                    {component.description}
                  </p>
                </article>
              ))}
            </div>
          </AccordionContent>
        </AccordionItem>

        <AccordionItem value="explore" className="bg-(--bg)">
          <AccordionTrigger>
            <span className="text-sm font-semibold">Explorar a plataforma</span>
          </AccordionTrigger>
          <AccordionContent>
            <div className="grid grid-cols-1 gap-2 md:grid-cols-2">
              {PLATFORM_LINKS.map((link) => (
                <PlatformResourceCard
                  key={link.label}
                  label={link.label}
                  href={link.href}
                  description={link.description}
                  icon={link.icon}
                  credentials={CREDENTIALS_BY_LABEL[link.label]}
                />
              ))}
            </div>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </section>
  );
}
