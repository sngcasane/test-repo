# ADR-0001: Use PostgreSQL as our primary datastore

- **Status**: Accepted
- **Date**: 2024-03-12
- **Deciders**: J. Roberts (CTO), M. Singh (Principal Engineer)

## Context

We need a primary datastore for the payments platform. Requirements:

- Strong consistency (we're handling money)
- ACID transactions across multiple tables
- Mature operational tooling (backups, replication, monitoring)
- Decent query planner for analytical workloads (reporting service)
- A team that already knows it

## Decision

We will use **PostgreSQL 16** on AWS RDS (multi-AZ) as the primary
datastore for all services. Each service owns its own schema within
a single shared cluster.

## Alternatives considered

### MongoDB
Rejected. Multi-document transactions exist but are not the path of
least resistance. Strong consistency on writes is harder to reason
about. The team has more Postgres experience.

### DynamoDB
Rejected. Excellent at point lookups but the reporting service runs
analytical queries that would be painful (and expensive) in DynamoDB.
We'd end up shipping data to a second store anyway.

### MySQL
Rejected. Postgres has a more capable query planner, better JSON support,
and `EXCLUDE` constraints (which we use in the ledger).

## Consequences

- **Positive**: Single datastore simplifies operations. Strong consistency
  by default. Team is productive.
- **Negative**: PostgreSQL writes are bound by the primary node. Sharding
  is a future problem if transaction volume grows 10x.
- **Neutral**: We commit to schema-per-service as a soft boundary between
  services. Cross-schema joins are allowed but discouraged.
