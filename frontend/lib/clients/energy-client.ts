import axios from "axios";

import { parseNumber } from "@/lib/energy/comparison";
import type {
  DataSource,
  Estado,
  OfertaNormalizada,
} from "@/lib/types/energy";

type OfertaRest = {
  id: number;
  solucao: "GD" | "Mercado Livre";
  custo_kwh: string;
  fornecedor: {
    id: number;
    nome: string;
    numero_clientes: number;
    avaliacao_media: string;
    logo: {
      url?: string;
      path?: string;
    };
  };
};

type OfertaGraphql = {
  id: number;
  solucao: "GD" | "Mercado Livre";
  custoKwh: string;
  fornecedor: {
    id: number;
    nome: string;
    numeroClientes: number;
    avaliacaoMedia: string;
    logo: {
      url?: string;
      path?: string;
    };
  };
};

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "https://api.localhost/api/v1";
const IMAGE_SERVER_PREFIX =
  process.env.NEXT_PUBLIC_IMAGE_SERVER_PREFIX ?? "https://minio.localhost/public";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

function normalizeLogoUrl(value: string | undefined): string {
  const normalizedPrefix = IMAGE_SERVER_PREFIX.replace(/\/+$/, "");

  if (!value) {
    return normalizedPrefix;
  }

  if (value.startsWith("http://") || value.startsWith("https://")) {
    return value;
  }

  const normalizedPath = value.replace(/^\/+/, "");
  return `${normalizedPrefix}/${normalizedPath}`;
}

function normalizeFromRest(ofertas: OfertaRest[]): OfertaNormalizada[] {
  return ofertas.map((oferta) => ({
    solucao: oferta.solucao,
    custoKwh: parseNumber(oferta.custo_kwh),
    fornecedor: {
      id: oferta.fornecedor.id,
      nome: oferta.fornecedor.nome,
      numeroClientes: oferta.fornecedor.numero_clientes,
      avaliacaoMedia: parseNumber(oferta.fornecedor.avaliacao_media),
      logoUrl: normalizeLogoUrl(
        oferta.fornecedor.logo.path ?? oferta.fornecedor.logo.url,
      ),
    },
  }));
}

function normalizeFromGraphql(ofertas: OfertaGraphql[]): OfertaNormalizada[] {
  return ofertas.map((oferta) => ({
    solucao: oferta.solucao,
    custoKwh: parseNumber(oferta.custoKwh),
    fornecedor: {
      id: oferta.fornecedor.id,
      nome: oferta.fornecedor.nome,
      numeroClientes: oferta.fornecedor.numeroClientes,
      avaliacaoMedia: parseNumber(oferta.fornecedor.avaliacaoMedia),
      logoUrl: normalizeLogoUrl(
        oferta.fornecedor.logo.path ?? oferta.fornecedor.logo.url,
      ),
    },
  }));
}

async function fetchEstadosRest(): Promise<Estado[]> {
  const response = await api.get<Estado[]>("/estados");
  return response.data;
}

async function fetchEstadosGraphql(): Promise<Estado[]> {
  const response = await api.post<{
    data?: {
      estados: Array<{
        id: number;
        nome: string;
        sigla: string;
        tarifaBaseKwh: string;
      }>;
    };
    errors?: Array<{ message: string }>;
  }>("/graphql", {
    query: `
      query Estados {
        estados {
          id
          nome
          sigla
          tarifaBaseKwh
        }
      }
    `,
  });

  if (response.data.errors?.length) {
    throw new Error(response.data.errors[0].message);
  }

  return (response.data.data?.estados ?? []).map((estado) => ({
    id: estado.id,
    nome: estado.nome,
    sigla: estado.sigla,
    tarifa_base_kwh: estado.tarifaBaseKwh,
  }));
}

async function fetchOfertasRest(estadoId: number): Promise<OfertaNormalizada[]> {
  const response = await api.get<OfertaRest[]>(`/estados/${estadoId}`, {
    params: { page: 1, per_page: 100 },
  });

  return normalizeFromRest(response.data);
}

async function fetchOfertasGraphql(
  estadoId: number,
): Promise<OfertaNormalizada[]> {
  const response = await api.post<{
    data?: { ofertasPorEstado: OfertaGraphql[] };
    errors?: Array<{ message: string }>;
  }>("/graphql", {
    query: `
      query OfertasPorEstado($estadoId: Int!, $page: Int!, $perPage: Int!) {
        ofertasPorEstado(estadoId: $estadoId, page: $page, perPage: $perPage) {
          id
          solucao
          custoKwh
          fornecedor {
            id
            nome
            numeroClientes
            avaliacaoMedia
            logo {
              url
            }
          }
        }
      }
    `,
    variables: { estadoId, page: 1, perPage: 100 },
  });

  if (response.data.errors?.length) {
    throw new Error(response.data.errors[0].message);
  }

  return normalizeFromGraphql(response.data.data?.ofertasPorEstado ?? []);
}

export async function fetchEstadosBySource(
  source: DataSource,
): Promise<Estado[]> {
  return source === "rest" ? fetchEstadosRest() : fetchEstadosGraphql();
}

export async function fetchOfertasBySource(
  source: DataSource,
  estadoId: number,
): Promise<OfertaNormalizada[]> {
  return source === "rest"
    ? fetchOfertasRest(estadoId)
    : fetchOfertasGraphql(estadoId);
}
