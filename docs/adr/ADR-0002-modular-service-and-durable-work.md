# ADR-0002: Modular service and durable work

Status: **PROPOSED — pending local architecture and operations decisions (Q03/Q09/Q14)**

## Context

The overview confirms FastAPI and PostgreSQL but specifies no repository, broker, worker topology, hosting platform, scale target or recovery target. Team 5 needs webhooks, sync, audit/event delivery and AI/tool execution that can survive request boundaries. The team has limited daily capacity. [S01 p18; S06 pp8-20; resource plan]

## Problem

Synchronous remote work risks request timeouts and loss on crash. Starting with many independently deployed services or unapproved infrastructure would exceed the supplied operational evidence and small-team capacity.

## Options considered

1. Multiple microservices plus broker, cache, mesh and dedicated workflow system immediately.
2. One modular FastAPI codebase, separate API/worker processes where needed, PostgreSQL-owned inbox/outbox and leased durable work; add a broker only after measured need.
3. Execute all external/model work synchronously in API requests.

## Proposed decision

Use option 2 as the starting topology. It separates modules and workload processes without pretending that service boundaries or infrastructure are approved. A worker claims fenced/leased jobs; remote side effects use an idempotency boundary and reconciliation after unknown outcomes. This is a design recommendation, not a claim that PostgreSQL provides exactly-once processing.

## Consequences and risks

- Q03 must identify an actual codebase and migration convention before application work.
- Q09/Q14 must set concurrency, failure, backup/restore and deployment thresholds before live operation.
- A database-backed queue may require a later broker/partitioning ADR if throughput, consumer isolation or delivery requirements justify it.
- Jobs must not keep database transactions open during remote calls.

## Acceptance / approver

Sagar/technical lead accepts a repository topology; operations/coordinator accepts deployment and recovery boundaries. Demonstrate migration, duplicate claim, lease expiry, crash/reconcile and disabled-connection behavior before marking a live worker ready.
