# ADR-0005: Tenant-scoped integration references and external ID mappings

Status: **PROPOSED — pending identifier/schema reconciliation (Q02/Q04/Q15/Q16)**

## Context

Provider identifiers can overlap across connections or organizations. The Team 5 blueprint proposes copied GitHub, project/task, service and organization tables even though current ownership assigns canonical entities to Teams 1-4. The supplied ERDs also differ in identifier/name details. [S00; Team 5 ERD; S02-S06]

## Problem

Copying source domain rows turns Team 5 into an accidental source of truth. A mapping keyed only by external ID permits cross-tenant contamination and ambiguous replay/repair.

## Options considered

1. Copy and mutate Team 1-4 core entities inside Team 5.
2. Persist a tenant-scoped integration connection, opaque external references/IDs, mapping provenance and sync state; obtain canonical objects/actions through owner contracts.
3. Never retain an external ID, so every delivery must be rediscovered remotely.

## Proposed decision

Use option 2. An external reference is unique in its provider namespace plus tenant-scoped connection, entity kind and external ID. A mapping records canonical owner/team/reference only after the owner contract accepts it. Team 5 can retain minimal safe display metadata/cache with clear freshness/provenance, not an editable canonical clone.

## Consequences and risks

- Mappings need collision, disconnect, remap, deletion and reconciliation semantics.
- Q16 must distinguish Team 1 allocation from Team 2 membership; neither becomes permission evidence by default.
- Physical foreign keys to another team's proposed tables are not assumed.
- A final schema/migration waits for Q15 material ERD decisions.

## Acceptance / approver

Team 5, relevant provider/domain owner and coordinator accept identifier scope and canonical mapping rules. Demonstrate two tenants with identical external IDs, wrong-connection delivery, mapping repair and owner rejection before live sync.
