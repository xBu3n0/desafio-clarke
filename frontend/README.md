# Frontend

Frontend do desafio Clarke Energia implementado com **Next.js + React + TypeScript**, responsável por consulta de estados/ofertas e comparação de custos/economia na interface.

## Sumário

- [Visão geral](#visão-geral)
- [Estrutura principal](#estrutura-principal)
- [Fluxo funcional implementado](#fluxo-funcional-implementado)
- [Contratos consumidos](#contratos-consumidos)
- [Variáveis de ambiente principais](#variáveis-de-ambiente-principais)
- [Executar localmente (isolado)](#executar-localmente-isolado)
- [Build e qualidade](#build-e-qualidade)

---

## Visão geral

| Item | Detalhe |
| --- | --- |
| Stack | Next.js (App Router), React, TypeScript |
| UI | Componentes próprios (`components/`) |
| Integração | REST e GraphQL no backend |
| Testes | Jest + Testing Library |
| Build/Run | Node + npm |

---

## Estrutura principal

| Caminho | Responsabilidade |
| --- | --- |
| `app/` | Página principal e entrypoint da aplicação |
| `components/energy/` | Blocos de tela (hero, busca, resultados) |
| `components/layout/` | Navbar e componentes estruturais |
| `lib/clients/` | Cliente HTTP e normalização de payload REST/GraphQL |
| `lib/hooks/` | Estado da consulta e orquestração do fluxo |
| `lib/energy/` | Regras de comparação no cliente (custo/economia/percentual) |
| `lib/constants/` | Links e constantes da plataforma |
| `test/` | Utilitários de teste frontend |

---

## Fluxo funcional implementado

| Etapa | Comportamento |
| --- | --- |
| Carregar estados | Busca estados via REST ou GraphQL |
| Selecionar estado e consumo | Form com validação de entrada |
| Consultar ofertas | Busca ofertas por `estado_id` |
| Comparar resultados | Calcula custo base, custo por fornecedor, economia e percentual no cliente |
| Exibir por solução | Agrupa em `GD` e `Mercado Livre`, com ordenação por economia |

---

## Contratos consumidos

| Fonte | Operação |
| --- | --- |
| REST | `GET /api/v1/estados` |
| REST | `GET /api/v1/estados/{estado_id}?page=1&per_page=100` |
| GraphQL | `POST /api/v1/graphql` (`estados`, `ofertasPorEstado`) |

---

## Variáveis de ambiente principais

| Variável | Uso |
| --- | --- |
| `NEXT_PUBLIC_API_URL` | Base pública da API consumida no browser |
| `NEXT_PUBLIC_SERVER_NAME` | Montagem de links da plataforma (`web.*`, `api.*`, etc.) |
| `NEXT_PUBLIC_IMAGE_SERVER_PREFIX` | Prefixo para resolver logos/imagens |

---

## Executar localmente (isolado)

```bash
cd frontend
npm ci
npm run dev
```

---

## Build e qualidade

```bash
cd frontend
npm run build
npm run lint
npm run test
```
