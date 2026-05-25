# Acme Corp Platform Architecture

This is the high-level architecture of the Acme Corp platform.

## System overview

The platform is composed of five services, all written in Python with
FastAPI, deployed to AWS ECS Fargate behind an Application Load Balancer.
A single PostgreSQL cluster (RDS, multi-AZ) backs all services. A Redis
ElastiCache cluster provides session storage and cross-service caching.

```
                          ┌─────────────────┐
                          │   Web (Angular) │
                          └────────┬────────┘
                                   │
                          ┌────────▼────────┐
                          │   API Gateway   │
                          └────────┬────────┘
            ┌──────────────┬───────┼───────┬──────────────┐
            │              │       │       │              │
        ┌───▼────┐   ┌─────▼──┐ ┌──▼───┐ ┌─▼─────────┐ ┌──▼─────┐
        │  auth  │   │payments│ │ledger│ │ reporting │ │webhooks│
        └───┬────┘   └────┬───┘ └──┬───┘ └────┬──────┘ └────┬───┘
            │             │        │          │             │
            └─────────────┴────────┼──────────┴─────────────┘
                                   │
                          ┌────────▼────────┐
                          │   PostgreSQL    │
                          └─────────────────┘
```

## Services

| Service | Responsibility |
|---|---|
| **auth** | User authentication, session management, JWT issuance |
| **payments** | Transaction processing, refunds, dispute handling |
| **ledger** | Double-entry bookkeeping, balance reconciliation |
| **reporting** | Analytics, dashboards, exports |
| **webhooks** | Outbound event delivery to merchant integrations |

## Communication

Services communicate over HTTP. We do NOT use a message broker — the
ledger service is the only service with sequential ordering requirements
and we handle that with database row-level locks rather than a queue.

For asynchronous work (e.g. webhook delivery retries), each service runs
its own background task workers using FastAPI's lifespan hooks and an
in-process asyncio queue.

## Database

Single PostgreSQL cluster, schema-per-service. The ledger service has the
strictest data integrity requirements — all ledger writes use serializable
transaction isolation.
