# ADR-0001: Identity, RBAC and ownership boundary

Status: **PROPOSED — pending coordinator, Team 1 and Team 5 acceptance (Q01/Q02)**

## Context

The current coordinator direction (S00) assigns Organizations, Users, Authentication and RBAC to Team 1, while older Team 1 and Team 5 specifications assign parts of authentication/RBAC to Team 5. Team 5 must authorize connector and AI actions but must not create a competing identity/RBAC source. [S00; `Nexora_Team1_HRMS_Organization_Spec.pdf` p14; `Nexora_Team5_Platform_Integrations_AI_Spec.pdf` pp5-6]

## Problem

Without a single accepted issuer, tenant-membership and permission contract, a valid caller could be interpreted differently by API, worker, tool and domain services. Duplicating users/roles/session state would make revocation and tenant isolation ambiguous.

## Options considered

1. Keep the legacy split and let Team 5 own a second identity/RBAC implementation.
2. Treat Team 1 as canonical identity/RBAC authority; Team 5 validates/consumes a documented delegation and enforces it at its own boundary.
3. Delay all Team 5 authorization until an unnamed shared implementation appears.

## Proposed decision

Adopt option 2 as the planning boundary: Team 1 is canonical for identity, organization and RBAC; Team 5 does not persist credentials, sessions, role grants or users as authoritative data. Team 5 receives verified subject, tenant, permission/delegation and correlation context through CT-01, rechecks domain scope with the owning service, and fails closed when authority cannot be verified. This restates S00; it is not a completed protocol selection.

## Consequences and risks

- Team 5 access, audit, connector and AI work depends on CT-01/Q01/Q02.
- Existing Team 5 ERD `organization` and identity-looking data must not be implemented as canonical Team 5 tables.
- A Team 1 outage/revocation behavior must be explicit for synchronous and queued work.
- Option 1 is rejected as a target architecture because it conflicts with the current coordinator direction, not because it is technically impossible.

## Acceptance / approver

Record the issuer/validation method, tenant derivation, service identity, delegated-agent semantics, revocation/cache behavior and failure mode in CT-01. Required approvers: project coordinator, Team 1 lead and Team 5 lead. Until then, only contract fixtures and negative tests are ready.
