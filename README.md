# cookiecutter-botkit-bot

A [cookiecutter](https://github.com/cookiecutter/cookiecutter) template for a new
[BotKit](https://github.com/ninelegsdog/botkit-core) Telegram bot — the same `src`
layout, tests, `Dockerfile` and `docker-compose.yml` that the nine production bots
in this portfolio are built on.

## Quick start

```bash
pipx install cookiecutter        # or: pip install cookiecutter
cookiecutter gh:ninelegsdog/cookiecutter-botkit-bot
```

Answer the prompts, then:

```bash
cd <project_slug>
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
docker compose up -d
```

No secrets are generated: copy `.env.example` to `.env` and fill in
`BOTKIT_BOT_TOKEN` and `BOTKIT_ADMIN_IDS` before the first run.

## What you get

```text
<project_slug>/
├── .env.example         # env template (copy to .env)
├── bot.py               # entry point
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml       # deps, pytest, ruff, mypy (strict)
├── README.md            # project readme with placeholders filled in
├── src/
│   └── core/            # the bot's own core package
└── tests/
    └── test_placeholder.py
```

The generated project wires in [`botkit-core`](https://github.com/ninelegsdog/botkit-core)
for payments, metrics, structured logging, tracing, Sentry and the aiohttp
webhook app, and ships with `pytest --cov-fail-under=70`, `ruff` and strict
`mypy` already configured.

## Template variables

| Variable              | Default        | Meaning                                                                 |
| --------------------- | -------------- | ----------------------------------------------------------------------- |
| `project_name`        | `my-bot`       | Human-readable name; the slug is derived from it                        |
| `project_slug`        | `my-bot`       | Directory and package name (`lower`, spaces → `-`)                      |
| `bot_name`            | `my-bot`       | Display name used in logs and the health payload                        |
| `port`                | `8090`         | Port for the webhook / metrics server                                   |
| `description`         | `Telegram bot` | One-line description, written into `pyproject.toml`                     |
| `author`              | `ninelegsdog`  | `pyproject.toml` author                                                 |
| `use_tracing`         | `y`            | Add the OpenTelemetry dependencies and tracer setup                     |
| `use_loki`            | `y`            | Configure the Loki log handler                                          |
| `use_yookassa`        | `n`            | Add the YooKassa payment provider dependency                            |
| `botkit_core_version` | `0.8.2`        | Pinned `botkit-core` git tag the generated project installs             |

## Health and metrics

The generated project exposes, out of the box:

| Endpoint   | Response                                             |
| ---------- | ---------------------------------------------------- |
| `/health`  | `ok`, or `{"status":"ok","version":"…"}` for JSON    |
| `/version` | `{"version":"…"}`                                    |
| `/metrics` | Prometheus metrics                                   |

## License

MIT — see [LICENSE](LICENSE).
