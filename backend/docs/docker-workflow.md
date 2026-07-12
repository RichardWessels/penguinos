# Docker Development Workflow

Use the local Docker Compose environment for Django commands. The application
dependencies and database service are provided by the `web` and `db` containers.

## Start the local environment

```bash
make local-build
make local-up
```

The local Compose configuration is `compose.yaml` plus `compose.local.yaml`.

## Run Django commands

Run commands in the `web` container after `make local-up`:

```bash
docker compose -f compose.yaml -f compose.local.yaml exec web python manage.py test
docker compose -f compose.yaml -f compose.local.yaml exec web python manage.py migrate --noinput
docker compose -f compose.yaml -f compose.local.yaml exec web python manage.py generate_stories --dry-run
```

For an interactive shell, use:

```bash
make shell-web
```

## Inspect and stop

```bash
make logs-web
make local-down
```

