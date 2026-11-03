# ADR-0003: Contract-based cross-team exchange

Status: **PROPOSED — pending provider/consumer agreements (CT-01 through CT-06; Q04/Q11)**

## Context

Teams 1-4 own their business records. The ERDs are proposed designs and show logical references, not approved shared database access. Team 5 must connect providers, transport data, emit audit/events and invoke owner actions. [S00; all team ERD diagrams; S03-S06]

## Problem

Direct database coupling would make schema changes, authorization, idempotency and source-of-truth disputes invisible. An undocumented HTTP endpoint would be equally unsafe if it lacks tenant, identifier, error and compatibility semantics.

## Options considered

1. Read/write other teams' tables directly.
2. Use versioned owner APIs and/or event envelopes with explicit authentication, scope, idempotency, acknowledgment, failure and evolution contracts.
3. Maintain permanent independent copies of every domain entity in Team 5.

## Proposed decision

Use option 2. Team 5 stores only tenant-scoped connection state, external identity mapping, delivery/job state and minimal reference metadata it owns. Domain teams normalize and persist their canonical data. Each CT document is a proposed contract until both provider and consumer accept it.

## Consequences and risks

- Contract delay blocks live integration, not source reconciliation or synthetic test work.
- Delivery may be at-least-once; consumers must declare idempotency and acknowledgment semantics.
- Q04 decides Team 3 canonical GitHub ingestion; Q11 decides event/audit/notification contract.
- No concrete endpoint example in the pack is a declared existing production interface.

## Acceptance / approver

Each CT requires named provider and consumer review, a version, schema/negative fixtures, tenant/auth rule, ownership of error/retry behavior and compatibility approach. Coordinator resolves any ownership conflict.
