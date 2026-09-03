# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

## Deployment

```bash
docker compose up -d
```

## Metrics

- `/health` → `ok`
- `/health` (Accept: application/json) → `{"status":"ok","version":"..."}` 
- `/version` → `{"version":"..."}`
- `/metrics` → Prometheus
