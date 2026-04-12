#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
ENV_FILE="${PROJECT_ROOT}/.env"

if [[ ! -f "${ENV_FILE}" ]]; then
  ENV_FILE="${PROJECT_ROOT}/.env.example"
fi

exec docker compose --env-file "${ENV_FILE}" -f "${PROJECT_ROOT}/compose.yml" up -d "$@"
