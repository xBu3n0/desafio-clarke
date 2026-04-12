# Backend

Este diretório implementa o backend do desafio da Clarke Energia com **Python + Flask**, seguindo a direção arquitetural descrita em `../SOLUCAO.md` e respeitando o problema definido em `../DESAFIO.md`.

O foco atual da codebase está em:

- modelagem de domínio;
- organização por camadas alinhada à Clean Architecture;
- interface HTTP mínima;
- testes automatizados;
- cobertura de testes segmentada.

## Objetivo do Backend

O backend existe para sustentar a consulta de fornecedores e soluções de energia a partir de:

- estado selecionado;
- consumo mensal informado;
- tarifa base do estado;
- ofertas disponíveis por fornecedor e solução.

No desafio, isso permitirá calcular:

- custo base por estado;
- custo por fornecedor;
- economia estimada;
- economia percentual;
- comparação por solução.

## Estado Atual da Implementação

No estágio atual, o backend já possui a base estrutural e o domínio principal modelado.

Implementado:

- domínio com entidades e value objects;
- `Estado` tratado como parte de `shared`;
- `Fornecedor`, `Logo` e `Oferta` tratados como parte de `energy`;
- exceções de domínio separadas por arquivo;
- value objects imutáveis com Pydantic;
- handlers globais de erro na interface HTTP;
- endpoint de health check;
- testes de domínio e testes HTTP;
- relatórios de cobertura por camada.

Ainda não implementado:

- camada de `application`;
- casos de uso da busca (`search`);
- repositórios;
- persistência;
- seeds/mock de dados do desafio;
- endpoint principal de consulta de fornecedores;
- cálculo completo de economia;
- ordenação dos resultados por economia;
- GraphQL.

## Organização da Codebase

```text
app/
  domain/
    entities/
      energy/
      shared/
    exceptions/
    value_objects/
      energy/
      shared/
  interfaces/
    http/
      controller/
tests/
  domain/
  interfaces/
```

## Modelagem de Domínio

### `shared`

Contém elementos reutilizáveis que não pertencem exclusivamente ao contexto de energia:

- `Estado`
- `EstadoId`
- `NomeEstado`
- `SiglaEstado`

### `energy`

Contém os conceitos específicos do problema de comparação de fornecedores:

- `Fornecedor`
- `Logo`
- `Oferta`
- `FornecedorId`
- `NomeFornecedor`
- `NumeroClientes`
- `AvaliacaoTotal`
- `NumeroAvaliacoes`
- `AvaliacaoMedia`
- `LogoId`
- `UrlLogo`
- `OfertaId`
- `Solucao`
- `CustoKwh`
- `ConsumoKwh`

## Regras de Modelagem Adotadas

- Value objects são criados com `.create(...)`.
- Value objects são readonly.
- Value objects não normalizam o valor recebido.
- Validações verificam regra de negócio, não fazem transformação silenciosa.
- Nomes de entidades e value objects seguem a nomenclatura do `SOLUCAO.md`.
- `Estado` foi isolado em `shared` para permitir reuso fora do contexto `energy`.
- A interface HTTP usa `controller`, não `routes`.
- `__init__.py` foram mantidos enxutos, funcionando principalmente como re-export.

## Interface HTTP

A aplicação Flask atualmente expõe:

- `GET /api/v1/health`

Também há tratamento global para:

- `ValidationError` -> `422`
- `EntityNotFoundError` -> `404`
- `DuplicateEntityError` -> `409`
- `KeyError` -> `400`
- `ValueError` -> `400`
- `DomainError` -> `400`
- `HTTPException` -> status original
- `Exception` -> `500`

## Como Rodar

### Ambiente local

```bash
.venv/bin/python app.py
```

### Stack completa em desenvolvimento

```bash
../scripts/dev.sh
```

## Testes

### Rodar lint

```bash
.venv/bin/ruff check .
```

### Validar formatação

```bash
.venv/bin/ruff format --check .
```

### Rodar testes

```bash
.venv/bin/python -m pytest tests/interfaces/http tests/domain
```

## Cobertura

Os relatórios de cobertura são gerados em HTML dentro de `coverage/`.

### Cobertura completa

```bash
../scripts/cov.sh all
```

### Cobertura por recorte

```bash
../scripts/cov.sh domain
../scripts/cov.sh value_objects
../scripts/cov.sh entities
../scripts/cov.sh http
```

Relatórios gerados:

- `coverage/all/index.html`
- `coverage/domain/index.html`
- `coverage/value_objects/index.html`
- `coverage/entities/index.html`
- `coverage/http/index.html`

## Qualidade Atual

Validação do estado atual do backend:

- `ruff check` passando;
- `ruff format --check` passando;
- suíte de testes passando;
- cobertura geral em `100%` no escopo atualmente implementado.

## Próximos Passos Naturais

Para avançar o backend em direção ao desafio completo, os próximos passos mais coerentes são:

1. [x] criar a camada de `application` para o fluxo de busca;
2. [x] definir ports e contratos de repositório;
3. [x] implementar infraestrutura e dados fictícios;
4. [x] criar o endpoint principal de consulta;
5. [x] calcular custo base, economia e economia percentual;
6. [x] ordenar os fornecedores por economia dentro de cada solução.
