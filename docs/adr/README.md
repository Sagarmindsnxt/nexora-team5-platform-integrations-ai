# Architecture decision record index

These ADRs preserve proposed decisions and the evidence needed to accept or reject them. They are not approvals, do not override the coordinator's current ownership direction, and must be updated when an accountable stakeholder makes a documented decision.

| ADR | Subject | Status | Decision authority / gate |
|---|---|---|---|
| [ADR-0001](ADR-0001-identity-and-ownership-boundary.md) | Identity, RBAC and ownership boundary | PROPOSED | Coordinator, Team 1 and Team 5; Q01/Q02 |
| [ADR-0002](ADR-0002-modular-service-and-durable-work.md) | Modular FastAPI deployment and durable work | PROPOSED | Sagar/technical lead and operations; Q03/Q09/Q14 |
| [ADR-0003](ADR-0003-contract-based-cross-team-exchange.md) | Contract-based exchange, no direct cross-team database access | PROPOSED | Coordinator and Teams 1-4 leads; CT-01..CT-06, Q04/Q11 |
| [ADR-0004](ADR-0004-gated-ai-tool-execution.md) | Gated AI tool execution and human approval | PROPOSED | Coordinator, Team 1, domain owners and security; CT-07, Q08 |
| [ADR-0005](ADR-0005-tenant-scoped-integration-references.md) | Tenant-scoped integration references and external ID mappings | PROPOSED | Team 5 and provider/domain owners; Q02/Q04/Q15/Q16 |
| [ADR-0006](ADR-0006-minimized-ai-data-and-usage-ledger.md) | Minimized AI data handling and separate usage ledger | PROPOSED | Coordinator, data/security/operations; Q06/Q07/Q10/Q12/Q14 |

The source evidence and conflict register are in [source-inventory.md](../source-inventory.md); implementation consequences are in [architecture.md](../architecture.md) and [implementation-plan.md](../implementation-plan.md).
