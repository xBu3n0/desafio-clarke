#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
ENV_FILE="${PROJECT_ROOT}/.env"

if [[ ! -f "${ENV_FILE}" ]]; then
  ENV_FILE="${PROJECT_ROOT}/.env.example"
fi

MODE="${1:-prod}"
if [[ "${MODE}" == "dev" || "${MODE}" == "prod" ]]; then
  shift || true
else
  MODE="prod"
fi

COMPOSE_FILE="${PROJECT_ROOT}/compose.yml"
if [[ "${MODE}" == "dev" ]]; then
  COMPOSE_FILE="${PROJECT_ROOT}/compose.dev.yml"
fi

exec docker compose --env-file "${ENV_FILE}" -f "${COMPOSE_FILE}" up -d --build --force-recreate "$@"
