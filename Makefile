.PHONY: ci install backend-install frontend-install lint test backend-lint backend-test frontend-lint frontend-test deploy-ec2

PYTHON ?= python3
BACKEND_DIR ?= backend
BACKEND_VENV ?= $(BACKEND_DIR)/.venv
FRONTEND_DIR ?= frontend

EC2_PORT ?= 22
DEPLOY_REF ?= main

ci: install lint test

install: backend-install frontend-install

backend-install:
	$(PYTHON) -m venv $(BACKEND_VENV)
	$(BACKEND_VENV)/bin/pip install --upgrade pip
	$(BACKEND_VENV)/bin/pip install -r $(BACKEND_DIR)/requirements-dev.txt

frontend-install:
	cd $(FRONTEND_DIR) && npm ci

lint: backend-lint frontend-lint

test: backend-test frontend-test

backend-lint:
	cd $(BACKEND_DIR) && .venv/bin/ruff check .
	cd $(BACKEND_DIR) && .venv/bin/ruff format --check .

backend-test:
	cd $(BACKEND_DIR) && .venv/bin/python -m pytest tests/application tests/domain tests/infrastructure tests/interfaces/http

frontend-lint:
	cd $(FRONTEND_DIR) && npm run lint

frontend-test:
	cd $(FRONTEND_DIR) && npm run test

deploy-ec2:
	@: "$${EC2_HOST:?EC2_HOST is required}"
	@: "$${EC2_USER:?EC2_USER is required}"
	@: "$${EC2_SSH_PRIVATE_KEY:?EC2_SSH_PRIVATE_KEY is required}"
	@: "$${DEPLOY_PATH:?DEPLOY_PATH is required}"
	@: "$${DEPLOY_ENV_B64:?DEPLOY_ENV_B64 is required}"
	KEY_FILE="$$(mktemp)"; \
	ENV_FILE="$$(mktemp)"; \
	EC2_PORT_VALUE="$${EC2_PORT:-22}"; \
	printf "%s" "$$EC2_SSH_PRIVATE_KEY" > "$$KEY_FILE"; \
	chmod 600 "$$KEY_FILE"; \
	printf "%s" "$$DEPLOY_ENV_B64" | base64 -d > "$$ENV_FILE"; \
	scp -P "$$EC2_PORT_VALUE" -o StrictHostKeyChecking=no -i "$$KEY_FILE" "$$ENV_FILE" "$$EC2_USER@$$EC2_HOST:$$DEPLOY_PATH/.env"; \
	ssh -p "$$EC2_PORT_VALUE" -o StrictHostKeyChecking=no -i "$$KEY_FILE" "$$EC2_USER@$$EC2_HOST" \
		"set -euo pipefail; cd '$$DEPLOY_PATH'; git fetch --all --prune; git checkout '$$DEPLOY_REF'; git pull --ff-only origin '$$DEPLOY_REF'; docker compose --env-file .env -f compose.yml up -d --build --remove-orphans"; \
	rm -f "$$KEY_FILE" "$$ENV_FILE"
