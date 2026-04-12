import {
  Activity,
  BarChart3,
  Boxes,
  Github,
  Linkedin,
  Mail,
  MessageCircle,
  Server,
  type LucideIcon,
} from "lucide-react";

const SERVER_NAME = process.env.NEXT_PUBLIC_SERVER_NAME ?? "localhost";

export const PLATFORM_LINKS: Array<{
  label: string;
  href: string;
  icon: LucideIcon;
  description: string;
}> = [
  {
    label: "API Swagger",
    href: `https://api.${SERVER_NAME}/api/v1/swagger`,
    icon: Server,
    description: "Documentação interativa da API REST.",
  },
  {
    label: "MinIO",
    href: `https://minio.${SERVER_NAME}`,
    icon: Boxes,
    description: "Acesso aos arquivos públicos de mídia.",
  },
  {
    label: "MinIO Console",
    href: `https://minio-console.${SERVER_NAME}`,
    icon: Activity,
    description: "Painel administrativo do armazenamento.",
  },
  {
    label: "Prometheus",
    href: `https://prometheus.${SERVER_NAME}`,
    icon: BarChart3,
    description: "Coleta e consulta de métricas da plataforma.",
  },
  {
    label: "Grafana",
    href: `https://grafana.${SERVER_NAME}`,
    icon: Activity,
    description: "Dashboards de observabilidade e monitoramento.",
  },
];

export const CONTACT = {
  name: "Matheus Bueno",
  email: "matheusbartkev.s@gmail.com",
  github: "https://github.com/xBu3n0",
  linkedin: "https://www.linkedin.com/in/matheus-bueno-178119230/",
  whatsapp: "https://wa.me/5542999343425",
} as const;

export const CONTACT_LINKS: Array<{
  label: string;
  href: string;
  icon: LucideIcon;
}> = [
  { label: CONTACT.email, href: `mailto:${CONTACT.email}`, icon: Mail },
  { label: "GitHub", href: CONTACT.github, icon: Github },
  { label: "LinkedIn", href: CONTACT.linkedin, icon: Linkedin },
  { label: "WhatsApp", href: CONTACT.whatsapp, icon: MessageCircle },
];
