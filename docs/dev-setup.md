# Local Development Setup

These instructions assume macOS or Linux. Windows users — use WSL2.

## Prerequisites

- Python 3.13 (we standardise on this exact version — newer is not yet supported)
- PostgreSQL 16 (Homebrew: `brew install postgresql@16`)
- Redis 7+ (`brew install redis`)
- Docker Desktop (for running integration tests)
- A GitHub PAT with `read:org` scope (set as `GITHUB_TOKEN` in your shell)

## First-time setup

1. Clone this repo and `cd` into it.
2. Create a Python virtualenv: `python3.13 -m venv .venv && source .venv/bin/activate`
3. Install dev dependencies: `pip install -r requirements-dev.txt`
4. Copy `.env.example` to `.env` and fill in the local secrets. Ask in
   `#engineering` Slack if you need access to the dev secrets vault.
5. Start the local databases: `docker compose up -d postgres redis`
6. Run migrations: `make migrate`
7. Seed dev data: `make seed`
8. Verify the setup: `make test-fast` — should pass in under 30 seconds.

## Running a service locally

Each service has its own `make dev` target:

```
cd services/auth
make dev          # starts uvicorn with --reload on port 8001
```

The ports are fixed per service so you can run multiple at once:

| Service | Port |
|---|---|
| auth | 8001 |
| payments | 8002 |
| ledger | 8003 |
| reporting | 8004 |
| webhooks | 8005 |

## Common problems

**`psycopg.OperationalError: connection refused`**
→ Postgres isn't running. Run `docker compose up -d postgres`.

**`ImportError: No module named 'acme.common'`**
→ You forgot to `pip install -e ./libs/acme-common`.

**Tests pass locally but fail in CI**
→ You probably depend on data from `make seed`. Production tests run
against an empty database — fix your test fixtures.
