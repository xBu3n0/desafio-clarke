# Clarke Energia Challenge

Projeto fullstack para consulta e comparação de ofertas de energia por estado, com frontend em Next.js, backend em Flask, banco relacional, GraphQL, observabilidade e deploy em Docker.

## Sumário

- [Documento de Solução](#documento-de-solução)
- [Ambiente online](#ambiente-online)
- [Visão geral](#visão-geral)
- [Frontend](#frontend)
- [Backend](#backend)
- [Prefixos e domínios disponíveis](#prefixos-e-domínios-disponíveis)
- [Rotas principais (superficial)](#rotas-principais-superficial)
- [Como rodar localmente](#como-rodar-localmente)
- [Scripts utilitários](#scripts-utilitários)
- [Comandos Make](#comandos-make)
- [Estrutura do repositório](#estrutura-do-repositório)
- [CI/CD](#cicd)
- [Refinamentos futuros](#refinamentos-futuros)

## Documento de Solução

Para contexto completo de produto, requisitos funcionais, regras de negócio, arquitetura e modelagem, consulte:

- [`SOLUCAO.md`](./SOLUCAO.md)

## Ambiente online

| Ambiente | URL |
| --- | --- |
| Produção (EC2) | https://web.mbueno.xyz |

> Observação: o certificado TLS atual está configurado como **self-signed**.

## Visão geral

| Componente | Stack |
| --- | --- |
| Frontend | Next.js (React + TypeScript) |
| Backend | Flask + SQLAlchemy |
| Banco | SQLite (produção simplificada) e PostgreSQL (desenvolvimento) |
| API | REST e GraphQL |
| Storage | MinIO (assets públicos, logos) |
| Observabilidade | Prometheus + Grafana |
| Reverse proxy/TLS | Nginx |
| Orquestração local | Docker Compose |

## Frontend

| Item | Valor |
| --- | --- |
| Diretório | `frontend/` |
| Documentação detalhada | [`frontend/README.md`](./frontend/README.md) |

## Backend

| Item | Valor |
| --- | --- |
| Diretório | `backend/` |
| Documentação detalhada | [`backend/README.md`](./backend/README.md) |

## Prefixos e domínios disponíveis

Os hosts abaixo são roteados pelo Nginx com `SERVER_NAME=mbueno.xyz`.

| Prefixo | URL | Finalidade |
| --- | --- | --- |
| `web.*` | https://web.mbueno.xyz | Aplicação frontend |
| `api.*` | https://api.mbueno.xyz | Backend (REST/GraphQL/Swagger) |
| `minio.*` | https://minio.mbueno.xyz | MinIO API / bucket público |
| `minio-console.*` | https://minio-console.mbueno.xyz | Painel do MinIO |
| `prometheus.*` | https://prometheus.mbueno.xyz | Prometheus |
| `grafana.*` | https://grafana.mbueno.xyz | Grafana |

## Rotas principais (superficial)

### REST (backend)

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/api/v1/health` | Healthcheck da API |
| `GET` | `/api/v1/estados` | Lista de estados |
| `GET` | `/api/v1/estados/{estado_id}?page=1&per_page=10` | Lista paginada de ofertas por estado |
| `GET` | `/api/v1/swagger` | Swagger UI |
| `GET` | `/api/v1/swagger.json` | OpenAPI JSON |

### GraphQL

| Método | Rota | Operações principais |
| --- | --- | --- |
| `POST` | `/api/v1/graphql` | `health`, `estados`, `estado`, `ofertasPorEstado`, `fornecedoresCount` |

### Métricas

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/metrics` | Métricas Prometheus/OpenMetrics |

## Como rodar localmente

### Pré-requisitos

- Docker + Docker Compose
- (Opcional) Node 22+ e Python 3.12+ para rodar testes fora de container

### 1. Configurar ambiente

```bash
cp .env.example .env
```

Esse passo é opcional para desenvolvimento: os scripts usam `.env.example` automaticamente quando `.env` não existe.
Use `.env` apenas se quiser sobrescrever variáveis (principalmente `SERVER_NAME`, portas e credenciais).

### 2. Subir ambiente de desenvolvimento

```bash
./scripts/dev.sh
```

### 3. Subir ambiente de produção local (compose de produção)

```bash
./scripts/prod.sh
```

### 4. Rebuild/forçar recriação

```bash
./scripts/recreate.sh dev
# ou
./scripts/recreate.sh prod
```

### 5. Build das imagens

```bash
./scripts/build.sh dev
# ou
./scripts/build.sh prod
```

## Scripts utilitários

| Script | Descrição |
| --- | --- |
| `./scripts/dev.sh` | Sobe stack de desenvolvimento (`compose.dev.yml`) |
| `./scripts/prod.sh` | Sobe stack de produção (`compose.yml`) |
| `./scripts/build.sh [dev|prod]` | Build das imagens |
| `./scripts/recreate.sh [dev|prod]` | Rebuild + force recreate |
| `./scripts/cov.sh [all\|application\|domain\|infrastructure\|value_objects\|entities\|http]` | Cobertura do backend |

## Comandos Make

| Comando | Descrição |
| --- | --- |
| `make install` | Instala dependências backend/frontend |
| `make lint` | Roda lint backend/frontend |
| `make test` | Roda testes backend/frontend |
| `make ci` | Executa `install + lint + test` |
| `make deploy-ec2` | Deploy no EC2 (usado pelo GitHub Actions) |

## Estrutura do repositório

| Caminho | Descrição |
| --- | --- |
| `frontend/` | Aplicação web Next.js |
| `backend/` | API Flask + domínio + infraestrutura |
| `nginx/` | Configuração de roteamento e TLS |
| `docker/` | Dockerfiles e configs de serviços auxiliares |
| `scripts/` | Atalhos de execução/build/recriação/cobertura |
| `compose.yml` | Stack de produção local |
| `compose.dev.yml` | Stack de desenvolvimento local |

## CI/CD

| Pipeline | Arquivo | Observação |
| --- | --- | --- |
| CI | `.github/workflows/ci.yml` | Executa validações em `push` e `pull_request` |
| CD | `.github/workflows/cd.yml` | Deploy no EC2 após sucesso da CI na branch `main` |

## Observação de desempenho

O requisito não funcional de latência foi validado empiricamente por meio de consultas executadas na aplicação e pela análise do histórico de métricas no Grafana.

## Refinamentos futuros

| Prioridade | Frente | Ação |
| --- | --- | --- |
| P1 | Contratos | Padronizar os contratos REST/GraphQL para reduzir mapeamentos e normalizações no cliente. |
| P2 | DTOs | Refinar DTOs de entrada/saída para padronizar nomes, tipos e responsabilidade por camada. |
| P3 | Backend | Consolidar os cálculos de comparação em um contrato único de aplicação, evitando duplicação fora da API. |
| P4 | Frontend | Reorganizar componentes para reduzir responsabilidades por componente e aumentar reutilização. |
| P5 | Testes | Expandir testes de integração ponta a ponta cobrindo contratos e regressões de fluxo. |
| P6 | Código | Executar refatorações incrementais para reduzir acoplamento e elevar legibilidade/consistência. |
| P7 | Qualidade contínua | Endurecer checks automáticos de lint/format e critérios de revisão de código. |
| P8 | Documentação | Manter README(s), `SOLUCAO.md` e contratos alinhados com o estado real da implementação. |
