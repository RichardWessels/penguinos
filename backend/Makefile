.PHONY: lint \
	local-build local-up local-down local-restart local-rebuild \
	prod-build prod-up prod-down prod-restart prod-rebuild prod-release prod-migrate prod-collectstatic \
	logs logs-web logs-db \
	shell-web prod-shell-web createsuperuser migrate collectstatic

PYTHON_DIRS := dopios_backend mainApp scripts

COMPOSE_BASE := docker compose -f compose.yaml
COMPOSE_LOCAL := $(COMPOSE_BASE) -f compose.local.yaml

lint:
	ruff format $(PYTHON_DIRS)
	ruff check $(PYTHON_DIRS)

# -------------------------
# Local
# -------------------------

local-build:
	$(COMPOSE_LOCAL) build

local-up:
	$(COMPOSE_LOCAL) up -d

local-down:
	$(COMPOSE_LOCAL) down

local-restart:
	$(COMPOSE_LOCAL) down
	$(COMPOSE_LOCAL) up -d

local-rebuild:
	$(COMPOSE_LOCAL) down
	$(COMPOSE_LOCAL) build
	$(COMPOSE_LOCAL) up -d

# -------------------------
# Production
# -------------------------

prod-build:
	$(COMPOSE_BASE) build

prod-up:
	$(COMPOSE_BASE) up -d

prod-down:
	$(COMPOSE_BASE) down

prod-restart:
	$(COMPOSE_BASE) down
	$(COMPOSE_BASE) up -d

prod-rebuild:
	$(COMPOSE_BASE) down
	$(COMPOSE_BASE) build
	$(COMPOSE_BASE) up -d

prod-release: prod-migrate prod-collectstatic

prod-migrate:
	$(COMPOSE_BASE) exec web python manage.py migrate --noinput

prod-collectstatic:
	$(COMPOSE_BASE) exec web python manage.py collectstatic --noinput

# -------------------------
# Logs / shell / django
# Defaulting to local
# -------------------------

logs:
	$(COMPOSE_LOCAL) logs -f --tail=100

logs-web:
	$(COMPOSE_LOCAL) logs -f --tail=100 web

logs-db:
	$(COMPOSE_LOCAL) logs -f --tail=100 db

shell-web:
	$(COMPOSE_LOCAL) exec web bash

prod-shell-web:
	$(COMPOSE_BASE) exec web bash

createsuperuser:
	$(COMPOSE_LOCAL) exec web python manage.py createsuperuser --noinput

migrate:
	$(COMPOSE_LOCAL) exec web python manage.py migrate --noinput

collectstatic:
	$(COMPOSE_LOCAL) exec web python manage.py collectstatic --noinput
