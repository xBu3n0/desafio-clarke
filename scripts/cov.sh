#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
BACKEND_ROOT="${PROJECT_ROOT}/backend"
PYTHON_BIN="${BACKEND_ROOT}/.venv/bin/python"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "backend virtualenv not found: ${PYTHON_BIN}" >&2
  exit 1
fi

TARGET="${1:-all}"
shift || true

TEST_PATHS=()
REPORT_DIR=""
INCLUDE_PATTERN=""

case "${TARGET}" in
  all)
    TEST_PATHS=(
      "tests/application"
      "tests/domain"
      "tests/infrastructure"
      "tests/interfaces/http"
    )
    REPORT_DIR="coverage/all"
    ;;
  application)
    TEST_PATHS=("tests/application")
    REPORT_DIR="coverage/application"
    INCLUDE_PATTERN="app/application/*"
    ;;
  domain)
    TEST_PATHS=("tests/domain")
    REPORT_DIR="coverage/domain"
    INCLUDE_PATTERN="app/domain/*"
    ;;
  infrastructure)
    TEST_PATHS=("tests/infrastructure")
    REPORT_DIR="coverage/infrastructure"
    INCLUDE_PATTERN="app/infrastructure/*"
    ;;
  value_objects)
    TEST_PATHS=("tests/domain/value_objects")
    REPORT_DIR="coverage/value_objects"
    INCLUDE_PATTERN="app/domain/value_objects/*"
    ;;
  entities)
    TEST_PATHS=("tests/domain/entities")
    REPORT_DIR="coverage/entities"
    INCLUDE_PATTERN="app/domain/entities/*"
    ;;
  http)
    TEST_PATHS=("tests/interfaces/http")
    REPORT_DIR="coverage/http"
    INCLUDE_PATTERN="app/interfaces/http/*"
    ;;
  *)
    echo "usage: ./scripts/cov.sh [all|application|domain|infrastructure|value_objects|entities|http] [pytest args...]" >&2
    exit 1
    ;;
esac

cd "${BACKEND_ROOT}"

rm -f .coverage
rm -rf "${REPORT_DIR}"
mkdir -p "${REPORT_DIR}"

"${PYTHON_BIN}" -m pytest \
  --cov=app \
  --cov-branch \
  --cov-report= \
  "${TEST_PATHS[@]}" \
  "$@"

if [[ -n "${INCLUDE_PATTERN}" ]]; then
  "${PYTHON_BIN}" -m coverage report --show-missing --include="${INCLUDE_PATTERN}"
  exec "${PYTHON_BIN}" -m coverage html \
    --include="${INCLUDE_PATTERN}" \
    -d "${REPORT_DIR}"
fi

"${PYTHON_BIN}" -m coverage report --show-missing
exec "${PYTHON_BIN}" -m coverage html -d "${REPORT_DIR}"
