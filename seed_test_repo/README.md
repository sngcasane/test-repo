# Acme Corp Engineering

Welcome to the Acme Corp engineering monorepo. This repository contains the
source for our internal platform services, our architecture documentation,
and the development standards every engineer is expected to follow.

## What we do

Acme Corp builds and operates a B2B payments platform used by mid-market
retailers across the UK and EU. We process roughly £40M in transaction
volume per month across the platform.

## Tech stack

- **Backend**: Python 3.13, FastAPI, PostgreSQL, Redis
- **Frontend**: Angular 19, TypeScript
- **Infrastructure**: AWS (ECS Fargate, RDS, ElastiCache), GitHub Actions
- **Observability**: Datadog, Sentry

## Repository structure

| Path | What's there |
|---|---|
| `services/` | Individual platform services (one folder per service) |
| `docs/` | Architecture overview, ADRs, dev-setup guide |
| `docs/adr/` | Architecture Decision Records — read these to understand *why* we built things the way we did |

## Getting started

New to the team? Start with [`docs/dev-setup.md`](docs/dev-setup.md) for your
local environment, then read [`CONTRIBUTING.md`](CONTRIBUTING.md) before
opening your first pull request.

## Asking questions

We run a SmartPlatform internal AI assistant — drop questions about any of
this codebase or the company docs into the chat and it will search the
repo and the document library for you.
