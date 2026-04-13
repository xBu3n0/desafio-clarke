# Backend

Backend do desafio Clarke Energia implementado com **Python + Flask + SQLAlchemy**, organizado por camadas com abordagem de **Clean Architecture**.

## Sumário

- [Visão geral](#visão-geral)
- [Estrutura (Clean Architecture)](#estrutura-clean-architecture)
- [Principais fluxos implementados](#principais-fluxos-implementados)
- [Regras de domínio relevantes](#regras-de-domínio-relevantes)
- [Persistência e dados](#persistência-e-dados)
- [Cache e observabilidade](#cache-e-observabilidade)
- [Variáveis de ambiente principais](#variáveis-de-ambiente-principais)
- [Execução local (isolada)](#execução-local-isolada)
- [Qualidade e testes](#qualidade-e-testes)

---

## Visão geral

| Item | Detalhe |
| --- | --- |
| Stack | Python 3.12, Flask, SQLAlchemy, Alembic, Gunicorn |
| Arquitetura | Clean Architecture (Domain, Application, Interfaces, Infrastructure) |
| API | REST e GraphQL |
| Observabilidade | OpenMetrics/Prometheus (`/metrics`) |
| Testes | Pytest + cobertura por camada |

---

## Estrutura (Clean Architecture)

| Camada | Caminho | Responsabilidade |
| --- | --- | --- |
| Domain | `app/domain/` | Regras de negócio puras, entidades, value objects e exceções |
| Application | `app/application/` | Casos de uso, DTOs e ports (contratos) |
| Interfaces | `app/interfaces/` | Controllers HTTP, schema/resolvers GraphQL, serialização e validação de entrada/saída |
| Infrastructure | `app/infrastructure/` | ORM, repositórios, UoW, cache, seed, migração e wiring técnico |

---

## Principais fluxos implementados

| Fluxo | Implementação |
| --- | --- |
| Listar estados | `GET /api/v1/estados` |
| Listar ofertas por estado (paginado) | `GET /api/v1/estados/{estado_id}?page=1&per_page=10` |
| Consultas GraphQL | `POST /api/v1/graphql` (`health`, `estados`, `estado`, `ofertasPorEstado`, `fornecedoresCount`) |
| Healthcheck | `GET /api/v1/health` |
| Métricas | `GET /metrics` |

---

## Regras de domínio relevantes

| Regra | Status |
| --- | --- |
| `sigla_estado` com 2 letras maiúsculas | Validado em value object |
| `consumo_kwh > 0` e `custo_kwh > 0` | Validado em value object e restrições de banco |
| Solução permitida: `GD` ou `Mercado Livre` | Validado em enum/value object |
| Unicidade por (`estado`, `fornecedor`, `solucao`) | Garantida por unique constraint no ORM |
| Ordenação por maior economia | Coberta no caso de uso de busca comparativa |

---

## Persistência e dados

| Item | Detalhe |
| --- | --- |
| Banco em produção local | SQLite (`DATABASE_URL=sqlite:////data/clarke.db`) |
| Banco em desenvolvimento | PostgreSQL (`compose.dev.yml`) |
| Migração | Alembic (`python -m app.infrastructure.migrate`) |
| Dados iniciais | Seed idempotente (`python -m app.infrastructure.seed`) |

---

## Cache e observabilidade

| Item | Detalhe |
| --- | --- |
| Cache de queries | `RedisJsonCache` (uso opcional via `REDIS_URL`) |
| Métricas HTTP | Contadores, histogramas/summaries para requests e status |
| Stack de monitoramento | Prometheus + Grafana via Docker Compose |

---

## Variáveis de ambiente principais

| Variável | Uso |
| --- | --- |
| `DATABASE_URL` | URL de conexão do banco |
| `API_PREFIX` | Prefixo da API (default `/api/v1`) |
| `MINIO_BUCKET_NAME` | Bucket de assets |
| `MINIO_PUBLIC_ENDPOINT` | Endpoint público do MinIO |
| `REDIS_URL` | URL do Redis (cache opcional) |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Endpoint OTLP (opcional) |

---

## Execução local (isolada)

Pré-requisito: virtualenv configurada em `backend/.venv`.

```bash
cd backend
.venv/bin/python app.py
```

---

## Qualidade e testes

```bash
cd backend
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/pytest -q
```

Cobertura por recorte:

```bash
./scripts/cov.sh all
./scripts/cov.sh domain
./scripts/cov.sh application
./scripts/cov.sh infrastructure
./scripts/cov.sh http
```
