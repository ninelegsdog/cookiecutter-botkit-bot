# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

Generated from
[cookiecutter-botkit-bot](https://github.com/ninelegsdog/cookiecutter-botkit-bot)
and built on [`botkit-core`](https://github.com/ninelegsdog/botkit-core).

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env        # then fill in TELEGRAM_BOT_TOKEN
pytest -q
python -m bot               # long polling
```

With `WEBHOOK_URL` set, the bot serves its own Telegram webhook on
`METRICS_PORT` instead of long polling.

## Configuration

Every variable is read by `src/core/config.py` (flat names, no prefix). See
`.env.example`:

| Variable               | Required | Default                            |
| ---------------------- | -------- | ---------------------------------- |
| `TELEGRAM_BOT_TOKEN`   | yes      | —                                  |
| `ADMIN_IDS`            | no       | *(empty)*                          |
| `DATABASE_URL`         | no       | `sqlite+aiosqlite:///data/app.db`  |
| `REDIS_URL`            | no       | `redis://127.0.0.1:6379/0`         |
| `WEBHOOK_URL`          | no       | *(empty → long polling)*           |
| `WEBHOOK_SECRET_TOKEN` | no       | *(empty)*                          |
| `SENTRY_DSN`           | no       | *(empty)*                          |
| `METRICS_PORT`         | no       | `{{ cookiecutter.port }}`          |

## Deployment

```bash
docker compose up -d
```

## Endpoints

- `/health` → `ok`, or `{"status":"ok","version":"…"}` for `Accept: application/json`
- `/version` → `{"version":"…"}`
- `/metrics` → Prometheus
