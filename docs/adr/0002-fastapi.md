# ADR-0002: Use FastAPI as our web framework

- **Status**: Accepted
- **Date**: 2024-03-15
- **Deciders**: J. Roberts (CTO), M. Singh (Principal Engineer)

## Context

We need a Python web framework for all platform services. Requirements:

- Async-native (we make a lot of outbound API calls)
- Strong type integration (we use Pydantic everywhere)
- Auto-generated OpenAPI documentation
- Mature enough to be safe in production

## Decision

We will use **FastAPI** (with uvicorn as the ASGI server) as the web
framework for every backend service.

## Alternatives considered

### Django REST Framework
Rejected. Sync-first. The ORM is excellent but we don't want it dictating
our data layer choices. Too opinionated about project structure.

### Flask
Rejected. Sync-first. The plugin ecosystem is great but the lack of native
async support is a non-starter for our workload.

### Starlette directly
Rejected. FastAPI is built on Starlette and gives us Pydantic integration
and auto-OpenAPI for free. No reason to drop down a layer.

## Consequences

- **Positive**: Pydantic models bridge HTTP, the database (via SQLAlchemy
  2.0 typed annotations), and our internal APIs with one type system.
- **Positive**: `/docs` Swagger UI is free per service — great for
  cross-team consumption.
- **Negative**: FastAPI is younger than Django; some patterns (auth,
  permissions) require more boilerplate.
- **Neutral**: We pin uvicorn and FastAPI exact versions across all
  services. Bumps are coordinated.
