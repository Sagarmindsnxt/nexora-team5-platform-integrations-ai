# Team 5 Complete Architecture and Cross-Team Service Analysis

**Evidence baseline:** documentation pack v0.1, dated 2026-10-27. **Prepared:** 2026-11-11. **Scope:** every local Markdown file under `docs/`, recursively. **Labels:** EXPLICITLY DOCUMENTED = requirement/ownership stated; IMPLEMENTATION EVIDENCE = code/runtime proof; INHERITED REQUIREMENT = requirement from source spec; ARCHITECTURAL PROPOSAL = design awaiting acceptance; UNRESOLVED = open decision/conflict; NOT DOCUMENTED = no evidence. “CONFIRMED” means requirement supported, not feature implemented or release-approved.

## Executive summary

Team 5 is the horizontal Platform, Integrations and AI Infrastructure team. It provides shared application conventions and health, enforcement of Team 1 identity/authorization, tenant-safe integration lifecycle and transport, audit/event infrastructure, an AI gateway and bounded registered-tool runtime, and later usage/evaluation infrastructure. Consumer teams retain business meaning and system-of-record data.

**Current target ownership:** Team 1 owns organizations, users, authentication and RBAC; Team 2 canonical project/work records; Team 3 canonical engineering records and intelligence; Team 4 incidents, evidence, RCA, remediation review and domain history. Team 5 consumes authority and owner contracts; it does not become a second IAM or duplicate domain store. This current direction supersedes older Team 5 auth/RBAC assignments, which remain a conflict pending CT-01 acceptance.

**Implementation finding:** docs specify requirements, proposed architecture/contracts/schema/tasks/controls, but contain no application implementation evidence. `validation-report.md` states the inspected workspace lacked app source, dependencies, deployment configuration, tests and cross-team services; no application tests were run. No Team 5 runtime capability can be called implemented from this documentation. Repository/source/runtime inspection is needed to establish status outside that inspected workspace.

**Architecture direction:** FastAPI and PostgreSQL are source-supported at high level. Modular backend, separate API/worker, Team 5 PostgreSQL schema, leases/inbox/outbox and at-least-once delivery are proposals, not accepted deployment facts. Owner-approved APIs/events are proposed; no direct cross-team SQL or exactly-once delivery. Team 5 receipt means durable admission, not canonical owner success.

## 1. Documentation inventory and inspection

Recursive search found **18 Markdown files**, including six ADRs and their index. None is empty. SHA-256 comparison found no byte-identical duplicate. Documents intentionally overlap as indexes/synthesis/detail; no file is marked obsolete. The master document reports original source PDFs/ERD images absent locally; source summaries are not direct reinspection of those artifacts.

| Relative path | Purpose, topics, architecture/T5 responsibilities and T1–4 dependencies | Condition |
|---|---|---|
| `docs/README.md` | Reader index, evidence vocabulary, review order, integrity; directs team leads to contracts. | Non-empty review draft. |
| `docs/PRD.md` | Scope, actors, 22 FRs, workflows, NFR/security, dependencies, acceptance. Covers shared platform, access, audit, connectors, AI, events; depends on T1 authority and T2–4 contracts. | Requirements, not implementation. |
| `docs/architecture.md` | Context/container/component views, modules, flows, runtime, persistence, reliability/ops. Proposes FastAPI/Postgres modules/API-worker; depends on all owner contracts. | Design proposal, no app repo observed. |
| `docs/api-contracts.md` | CT-01–07 proposals, example payloads/routes/errors/retries/acceptance. Specifies boundaries with T1–4. | Explicitly no cross-team approval or deployed API claimed. |
| `docs/database-schema.md` | Proposed entity dictionary, ERD reconciliation, tenant constraints, state machines, transaction/retention/migration. | No approved DDL/migration. |
| `docs/security.md` | Trust zones, invariants, threats, proposed controls/tests/incident response. Depends on T1 and domain resource/approval boundaries. | Proposal, not implementation/certification. |
| `docs/implementation-plan.md` | Readiness classes and 34 tasks with gates, capacity, acceptance evidence. | Proposed tasks; no completion asserted. |
| `docs/open-questions.md` | Q01–Q16 owners, impact, recommendation and closure evidence. | All open per master synthesis. |
| `docs/source-inventory.md` | Six PDFs, five ERD images, resource plan summaries; ownership matrix, journeys, C01–C10. | Source artifacts not local Markdown; summaries cite them. |
| `docs/validation-report.md` | Static validation methods/results and limits. | Documentation only; no runtime test; Mermaid unparsed/unrendered. |
| `docs/NEXORA_PROJECT_MASTER_DOCUMENT.md` | Onboarding synthesis: teams/modules/architecture/API/integrations/AI/plan/gaps. | Overlap by design, not exact duplicate. |
| `docs/adr/README.md` | ADR index, decision authorities/gates. | ADRs all proposed, not accepted. |
| `docs/adr/ADR-0001-identity-and-ownership-boundary.md` | Proposed T1 identity/RBAC authority, T5 consume/enforce boundary. | Pending T1/T5/coordinator. |
| `docs/adr/ADR-0002-modular-service-and-durable-work.md` | Proposed modular FastAPI/API-worker and durable DB work. | Topology/ops open. |
| `docs/adr/ADR-0003-contract-based-cross-team-exchange.md` | Proposed owner APIs/events; avoid direct cross-team tables. | CT acceptance pending. |
| `docs/adr/ADR-0004-gated-ai-tool-execution.md` | Proposed fixed registered tools, authorization, policy, exact human approval. | CT-07/Q08 pending. |
| `docs/adr/ADR-0005-tenant-scoped-integration-references.md` | Proposed tenant-scoped external IDs and mappings, no editable clones. | ID/schema decisions pending. |
| `docs/adr/ADR-0006-minimized-ai-data-and-usage-ledger.md` | Proposed minimized AI records and separate requests/attempts/usage/prices. | Provider/price/retention/eval choices pending. |

**Count discrepancy:** validation-report says 17 Markdown files; current recursive inventory is 18. Master document’s explicit inspection list omits ADR-0006, though it discusses it elsewhere. This report uses filesystem count 18.

**Evidence:** [README.md](README.md) §§1–4; [source-inventory.md](source-inventory.md) §§1–2; [validation-report.md](validation-report.md) lines 22–46; [NEXORA_PROJECT_MASTER_DOCUMENT.md](NEXORA_PROJECT_MASTER_DOCUMENT.md) lines 575–581.

## 2. Why Team 5 exists; responsibility boundaries

Nexora connects organizational ownership, planned work, code changes, builds/deployments, telemetry and incidents. Independent connectors and AI clients multiply credentials, failure handling, costs and inconsistent access. Team 5 supplies reusable controls and transport while domain teams keep the business meaning. Intended outcome: authorized, traceable flow into the correct canonical owner and governed AI assistance within current rights/human review.

Team 5 is horizontal because T1–4 consume its infrastructure. It is not another business-function team.

| Capability | Team 5 owns | Must remain with consumer teams |
|---|---|---|
| Shared platform | Common config/API/errors/logging/health; T1 identity adapter/enforcement; tenant/resource guards; audit/events; technical durable state. | Identity issuer, organizations/people/RBAC master, domain APIs and domain history. |
| Integration framework PLAT-006 | Connector lifecycle/capabilities, connection state, credential references, fetch/sync/webhook transport, retry/checkpoint/receipt, external mappings. | Provider truth and consumer canonical records/normalization. |
| Provider connectors PLAT-007–009 | Provider transport/auth/fetch/pagination/webhook verification and mapping to owner contract. | Canonical repository/task/incident semantics; unsupported provider capability must be explicit. |
| AI platform PLAT-010–015 | Approved routing, registry/runtime, policy, attempt usage infrastructure, evaluation runner and execution audit. | T3/T4 domain prompts, expected answers, change/RCA reasoning, source permission and autonomous authority. |

Major deliverables: foundation/access; connector framework; initial GitHub-to-T3 flow; selected PM/observability adapters; audit/events; governed gateway/runtime/policy and minimum attempt tracking; later reports/evaluation/notifications. End-to-end intended outcomes are access+audit, provider-to-owner ingestion with safe replay, and governed advisory AI; operational recovery is an additional proposed gate.

**Evidence:** [PRD.md](PRD.md) §§2–5.2; [architecture.md](architecture.md) §§1,3; [source-inventory.md](source-inventory.md) S06 and ownership matrix; [NEXORA_PROJECT_MASTER_DOCUMENT.md](NEXORA_PROJECT_MASTER_DOCUMENT.md) §§1–4.

## 3. Overall architecture and modules

**Explicit constraints:** FastAPI/PostgreSQL high-level stack; T1–4 own domain data; T5 is horizontal; agent rights cannot exceed human/service rights; assisted remediation has human review. The entity relationship chain does not imply a graph DB.

**Proposal:** modular FastAPI, T5-owned PostgreSQL schema, API and worker processes from one artifact, DB inbox/outbox/leases, owner APIs/events, secret/telemetry systems. **Not documented/undecided:** actual repository, versions, ORM for T5, DB topology, broker/cache/vector/graph store, host/cloud, frontend, CI/CD, model/provider, secrets product, SLO/RPO/RTO/on-call. Shared DB server would not authorize shared tables.

| Module | Requirement mapping | Purpose / boundary | Status |
|---|---|---|---|
| M01 Foundation | PLAT-001, OPS-001 | Config, request context, errors/logging, health/version, DB unit-of-work/deploy hooks. | Planned, no code evidence. |
| M02 Access | PLAT-002–004, DATA-001 | T1 auth adapter, permission/tenant/resource enforcement; no T5 identity store. | Planned; CT-01 gate. |
| M03 Audit/events | PLAT-005, 016, REL-001 | Durable audit/query/event delivery; not domain history/channel selection. | Planned; CT-06/Q10/Q11. |
| M04 Connector runtime | PLAT-006, SEC-001/002, REL-001 | Adapter catalog/lifecycle, connection/secret refs, inbox/jobs/checkpoints/mappings/recovery. | Planned; provider/schema/ops gates. |
| M05 GitHub | PLAT-007 | GitHub fetch/webhook parsing and authorized read tools to T3. | Planned; CT-03/Q04/Q06. |
| M06 Work integrations | PLAT-008 | Selected PM providers mapped to T2. | Planned P1; provider/direction open. |
| M07 Observability | PLAT-009 | Bounded telemetry/event transport to T4. | Planned P1; provider/service open. |
| M08 Gateway | PLAT-010 | Approved model route, request/response validation, timeout/error and metering hooks. | Planned; no provider chosen. |
| M09 Registry/executor | PLAT-011/012, SEC-003 | Versioned agents/tools, context, bounded steps, typed dispatch. | Planned; no domain reasoning. |
| M10 Policy | PLAT-013, SEC-003 | Restrict/deny/approval-needed; cannot grant T1 permission. | Planned; writes gated by Q08. |
| M11 Metering | PLAT-014 | Per-attempt usage, versioned estimates, reconciliation; unknown remains unknown. | Planned; reporting P1. |
| M12 Evaluation | PLAT-015 | Versioned evaluation fixtures/runs/results. | Planned/eventual P1; T3/T4 own ground truth. |

M01–M12 are proposed modules, not separate deployables or implementation evidence. Source priority count conflicts: prose 10 P0/6 P1 vs rows 11/5 (C07/Q13).

**Evidence:** [architecture.md](architecture.md) §§1–3; [PRD.md](PRD.md) §§5.1–5.2; [database-schema.md](database-schema.md) §§1–2; [source-inventory.md](source-inventory.md) C07.

## 4. Services to Teams 1–4

### Team 1 — Identity, HRMS, Organization

T1 owns organizations, users, authentication, RBAC, departments, teams, employees, organizational/reporting roles and project allocations under current coordinator direction. User ID differs from employee ID; allocation is not automatically membership or permission. T5 consumes validated subject/workload, organization membership/status, permission/delegation and lifecycle/revocation via CT-01. T5 provides enforcement, tenant isolation, common APIs, audit/events and shared services that T1 may consume; no separate T5 business service uniquely for T1 is identified. Token type/API is unselected. Old T5 login/logout/refresh/roles/permissions paths require reassignment to T1 and are not target T5 APIs. Flow: T1 authority → verified context → T5 enforcement and resource-owner check → authorized result; fail closed if authority unavailable.

### Team 2 — Project and Task Management

T2 owns canonical projects, epics, tasks/subtasks, assignment/workflow and import decisions. T5 provides PLAT-006 and, if selected, Jira/Linear/Azure DevOps fetch/import, external mapping, checkpoints/retries and proposed CT-02 envelope. T2 decides status/assignee mapping, native-vs-external conflict, deletion, parent behavior and canonical IDs. Canonical Work Item spans Jira Issue, Linear Issue and Azure DevOps Work Item conceptually; no accepted shared schema exists. CT-02 `title`, `description`, `external_status`, `external_assignee_id` are proposed import fields only. Flow: provider → T5 adapter/map → T2 validates and commits → T5 records acknowledgment/checkpoint → T2/downstream consumers use owner data. One-way import is proposed; write-back is not approved.

### Team 3 — Engineering Productivity and Change Intelligence

T3 owns canonical repositories, branches, commits, PRs, builds/deployments, work-code links, metrics, impact and change intelligence. T5 provides GitHub authentication/fetch/pagination/webhook/mapping/retry/provenance and proposed CT-03 delivery; authorized read context may serve T3/T4 agents. T5 does not own engineering truth or automatically enable writes. Canonical Pull Request concept spans GitHub PR, GitLab MR, Azure DevOps PR. T3 source summary names repository ref, external ID, author, branches, state/review/approval/merge timestamps and change size. No accepted common schema/import contract; CT-03 sample is illustrative. Flow: provider → T5 verifies/maps → T3 validates/persists/deduplicates → receipt → T5 checkpoint → T3 analysis.

### Team 4 — Incident Management and RCA

T4 owns incident normalization/interpretation, incidents/timeline/evidence, correlation, RCA/findings, remediation proposals, validation and human review/history. T5 provides observability transport, bounded queries/events, provenance/completeness, and shared AI/policy/usage/audit. It does not interpret evidence or create canonical incidents. Canonical Incident concept spans Sentry, Datadog, PagerDuty. Source summary lists org/project/service refs, source/external ID, severity SEV1–4, states OPEN/INVESTIGATING/MITIGATED/RESOLVED/CLOSED, owners/timestamps. No accepted schema/import API. Proposed CT-04 sample does not settle unresolved service mapping. Flow: provider → T5 verifies/bounds → proposed envelope → T4 canonicalizes/correlates T1–3 context → T4 owns RCA/review; T5 provides governed AI as requested. Partial evidence explicit; no automatic merge/deploy.

Owner assignments above are documented current direction. CT-01–04 paths, payloads, acknowledgments and transport are proposals requiring agreement. Intended service does not mean a reachable service exists.

**Evidence:** [PRD.md](PRD.md) §§5,10; [source-inventory.md](source-inventory.md) C01–C10/ownership; [api-contracts.md](api-contracts.md) CT-01–04; [NEXORA_PROJECT_MASTER_DOCUMENT.md](NEXORA_PROJECT_MASTER_DOCUMENT.md) §4.

## 5. Canonical models and integration architecture

Canonical means the owner’s vendor-neutral official representation and business rules; it does not mean T5 stores that record. T5 transports/maps; owner validates and persists. No example below is an accepted schema.

| Category | External objects | Documented fields/intent | T5 vs owner | Schema status |
|---|---|---|---|---|
| Pull Request | GitHub PR, GitLab Merge Request, Azure DevOps PR | Change/review object attached to repository. T3 source summary lists repository ref, external ID, author ref, branches, state, review/approval/merge timestamps and change size. | T5 authenticates/fetches/verifies/transports; T3 defines canonical model and analyzes. | No accepted schema. CT-03 sample is proposal; separate variants needed. |
| Work Item | Jira Issue, Linear Issue, Azure DevOps Work Item | Project-scoped planned work with identity/title/description/status and possibly parent/assignee; T2 owns workflow. | T5 adapter/mapping/import; T2 decides canonical create/update and conflicts. | No accepted schema. CT-02 sample fields illustrative. |
| Incident | Sentry, Datadog, PagerDuty incidents | Operational occurrence with provider ID/revision/time/title/severity/service; T4 owns severity/status/evidence meanings. | T5 bounded transport/provenance; T4 canonicalizes and owns RCA. | No accepted schema. Source model summary and CT-04 sample are not accepted schema. |

Canonicalization supports cross-provider reasoning without vendor-specific domain logic. Mapping scope should include tenant, connection/provider namespace, entity kind and external ID (plus parent scope as needed), and bind only after owner acknowledgment. IDs are opaque; user ≠ employee; unresolved external people stay unresolved. Revisions/provenance aid replay; timestamps are not necessarily a total order.

**Evidence:** [source-inventory.md](source-inventory.md) S03–S05; [api-contracts.md](api-contracts.md) CT-02–04; [database-schema.md](database-schema.md) §§2–4; [PRD.md](PRD.md) FR-PLAT-007–009.

## 6. Connector architecture — PLAT-006

PLAT-006 documents the seven method names `authenticate()`, `connect()`, `disconnect()`, `health_check()`, `sync()`, `fetch()`, `handle_webhook()`. It supplies no signatures, parameter/return schemas, base class, exception taxonomy or concurrency rules. Capability manifest/typed outcomes are proposals. Providers need not support every method. No implementation is evidenced.

| Method | Purpose / documented expectations | Inputs/outputs/dependencies | Status |
|---|---|---|---|
| `authenticate()` | Provider connection/credential authentication. | Provider auth mode/scopes unresolved; secret reference expected, not plaintext. | Name required; signature/working method NOT DOCUMENTED/UNVERIFIED. |
| `connect()` | Establish/validate tenant-scoped connection/config. | Proposed provider, safe config, credential ref, tenant; CT-01/05, Q04/06. | No implementation evidence. |
| `disconnect()` | Disable/revoke/detach and prevent future dispatch; handle queued work. | Exact disable/cancel/revoke semantics need agreement. | Details proposed; no implementation evidence. |
| `health_check()` | Report provider/connection health or degraded/reauth state. | Shape/exposure unresolved. | Schema absent; no implementation evidence. |
| `sync()` | Bounded synchronization; checkpoint after owner acknowledgment. | Proposed scope/mode/cursor and durable job; worker is ADR proposal. | Behavior partly proposed; no implementation evidence. |
| `fetch()` | Retrieve provider records/pages or scoped requested data. | Provider IDs/pagination/resource authorization/rate limits unresolved. | Common schema absent; no implementation evidence. |
| `handle_webhook()` | Verify/process supported provider callbacks. | Raw bounded body, provider signature/delivery headers and trusted connection; durable inbox-before-ack proposed. | Generic route/signature absent; no implementation evidence. |

**Proposed lifecycle—not a running sequence:**

```text
External Provider
       |
       v
Registered adapter / capability check
       |
       v
Authenticate provider connection
       |
       v
Connect and validate configuration
       |
       v
Health check / active or degraded state
       |
       +-----------------------------+
       |                             |
       v                             v
Fetch / sync job                 Verified webhook
       |                             |
       +-------------+---------------+
                     v
       Bounded validation, connection/tenant binding,
       dedupe and durable inbox/job (proposal)
                     |
                     v
       Provider normalization and provenance
                     |
                     v
       Owner-approved canonical envelope/API
                     |
                     v
       Owner validation + durable canonical acknowledgment
                     |
                     v
       T5 mapping/checkpoint/status
```

For admin actions, T5 needs current T1 permission and connection scope. Worker identity differs from user delegation and authority is rechecked before dispatch. Webhook signature authenticates provider, not user. Acknowledge only after durable T5 admission; canonical completion requires owner ack. Delivery is at least once; reconcile uncertain effects rather than blind replay. Proposed connection states: pending/active/degraded/disabled/disconnected; job states: queued/running/retry_wait/succeeded/failed/cancelled.

**Evidence:** [PRD.md](PRD.md) FR-PLAT-006; [architecture.md](architecture.md) §10; [api-contracts.md](api-contracts.md) CT-05; [database-schema.md](database-schema.md) §§4–6.

### Provider-specific scope

- **PLAT-007 GitHub:** initial source-required target; retrieve repositories, branches, commits, PRs, diffs/changed files and build/workflow/deployment data where available; webhooks and authorized reads. Verify installation/repo scope, raw-body signature, delivery identity, pagination/rate limits and provenance. T3 canonicalizes; T5 holds mapping/sync state. No PR write automatically enabled. GitLab/Azure DevOps are candidates.
- **PLAT-008 PM:** Jira, Linear, Azure DevOps are inherited examples; subset/direction open. Proposed inbound import to T2. T2 owns workflow/conflict/status/assignee/deletion/IDs. No T5 editable work master or silent write-back. P1 source row.
- **PLAT-009 Observability:** Sentry, Datadog, PagerDuty, Prometheus, OpenTelemetry are candidates. Incident callbacks, telemetry pulls, metrics, traces and logs differ. T5 transports bounded authorized source/time data with provenance/completeness; T4 owns incident/evidence meaning. Service catalog owner unresolved. P1.

**Evidence:** [PRD.md](PRD.md) FR-PLAT-007–009; [architecture.md](architecture.md) §§2.1,3,10; [source-inventory.md](source-inventory.md) S06/C03–05.

## 7. AI platform

| Component | Responsibility | Consumers / owner | Gate/status |
|---|---|---|---|
| M08 gateway / PLAT-010 | Validate logical request, tenant/model/data route; resolve provider secret; normalize response/error; bound timeout/retry; record attempts/usage; no silent fallback. | T3/T4 agents and authorized clients. | No provider/model chosen; Q06/07/10. Planned. |
| Model/provider registry | Catalog approved versions/capabilities; trusted config controls endpoint. | Platform policy/config. | No selected runtime. Planned. |
| M09 registry/runtime / PLAT-011/012 | Versioned agent/tools, schemas/permission/risk/audit metadata, context references, bounded steps and fixed handlers. | T3/T4 own prompts/reasoning and validate business meaning. | CT-07/Q07/08/09. Planned. |
| M10 policy / PLAT-013 | Deny/allow/approval-required; intersect T1 authority, owner scope, tool/agent, policy and approval. | T1 permission authority; domain review remains owner-side. | Write path gated by Q08/CT-04/07. |
| M11 usage / PLAT-014 | Separate logical requests and provider attempts; usage source, price version/currency, unknowns/corrections. | Authorized tenant consumers/ops. | Q07/10; report P1. Planned. |
| M12 evaluation / PLAT-015 | Versioned synthetic/redacted cases, expected/actual refs, rubric/scorer version, latency/cost. | T3/T4 provide truth and criteria. | P1/eventual; Q10/12; no automatic promotion. |

Model output, retrieved code/logs/issues and tool output are untrusted. They cannot select tenant, grant access, change policy, choose arbitrary URL/code or forge approval. Server validates tool/arguments, rechecks current permission and policy, and requires exact authoritative single-use approval for enabled high-risk writes. T4 review is not automatically technical execution permission. No automatic merge/deploy. First live profile recommended read-only/advisory.

**Proposed flow:** T3/T4 request → T1/resource authorization and data policy → provenance-bearing context → bounded runtime → M08 approved route → validated response → optional M10 authorization/policy/approval → fixed handler → audit/usage → domain team validates and persists meaning.

**Evidence:** [PRD.md](PRD.md) FR-PLAT-010–015; [architecture.md](architecture.md) §11; [api-contracts.md](api-contracts.md) CT-07; ADR-0004/0006.

## 8. Persistence and operations

PostgreSQL is named at high level. SQLAlchemy/Alembic are named by T1 source only; T5 usage is proposed. Proposed T5 entity groups:

- Integration: `tenant_setting`, `integration_provider`, `integration_connection`, `external_id_mapping`, `sync_job`, `webhook_inbox`, deferred `observability_source`.
- AI: `ai_provider`, `ai_model`, `agent_definition`, `tool_definition`, `agent_tool`, `policy_version`, `guardrail_definition`, `agent_run`, `ai_request`, `ai_attempt`, `tool_execution`, conditional `approval_binding`.
- Usage/evaluation: `model_price`, `usage_event`, deferred `evaluation_case`, `evaluation_run`, `evaluation_result`; budget reservation only if approved.
- Audit/events: `audit_event`, `outbox_event`, `event_delivery`.

All are proposed, not DDL. Tenant scope on rows/relations; opaque IDs; cross-team logical references validated by owner. Do not create T1 org/user/role, T2 work, T3 engineering, T4 incident/RCA or unapproved service master. JSON bounded/validated; secrets as references; raw prompt/payload off by default. Retention/residency/deletion/hold unresolved.

ADR-0002 proposes API + same-package worker, potentially separate processes, DB leases/inbox/outbox initially. Worker claims lease/fencing token, releases DB transaction before remote call, records attempts/idempotency and advances checkpoint only after owner ack. At-least-once delivery. Crash after remote effect before local result is unknown and must be reconciled.

Required but unselected capabilities: typed config, finite deadlines/body/retry limits, host allowlists/egress, secrets resolver, safe telemetry, health/readiness/version, controlled migration, compatible rollback, backup and restore/reconciliation. Host/cloud, CI/CD, alert routes/owners and SLO/RPO/RTO are not selected/documented.

**Evidence:** [database-schema.md](database-schema.md) §§1–8; [architecture.md](architecture.md) §§4–6,12–14; [ADR-0002](adr/ADR-0002-modular-service-and-durable-work.md); [open-questions.md](open-questions.md) Q03/Q09/Q14.

## 9. Team 5 API inventory

No endpoint implementation is evidenced. Source-listed routes are interface intentions; most schemas and auth details are absent or proposed.

| Method / route | Source vs proposal | Purpose / consumer / auth and status |
|---|---|---|
| `GET /health` | Source-specified | Process liveness; response/exposure proposed; unverified. |
| `GET /ready` | Source-specified | Local readiness; proposed DB/schema readiness, provider degradation separate; Q14; unverified. |
| `GET /version` | Source-specified | Safe release/build ID; exposure proposal; unverified. |
| `GET /api/v1/integrations` | Source path, CT-05 behavior proposed | Tenant-scoped list; T1 read grant, sanitized cursor/filter; unverified. |
| `POST /api/v1/integrations` | Source path, payload proposed | Create integration; manage grant, provider/config/credential reference, proposed 201; unverified. |
| `GET /api/v1/integrations/{id}` | Source path, behavior proposed | Same-tenant connection state/health; sanitized; unverified. |
| `POST /api/v1/integrations/{id}/sync` | Source path, behavior proposed | Enqueue scoped sync; idempotency, proposed 202 durable job receipt/status URL, not completion; unverified. |
| `DELETE /api/v1/integrations/{id}` | Source path, behavior proposed | Disconnect; manage/revision grant, proposed 202 async or 204 post-lifecycle; unverified. |
| `GET /api/v1/audit/events` | Source-specified | Audit query; permission/filter/schema incomplete; unverified. |
| `POST /api/v1/ai/chat` | Source-specified S06 p16 | Gateway chat; schema/auth proposed/incomplete; unverified. |
| `POST /api/v1/ai/execute` | Source-specified S06 p16 | Agent/tool execution; semantics/policy/approval proposed; unverified. |
| `GET /api/v1/ai/usage` | Source-specified | Usage/cost view; fields/rate permissions incomplete; unverified. |
| `GET /api/v1/ai/tools` | Source-specified | Tool manifest; proposed visibility filtering; unverified. |
| `GET /api/v1/ai/tools/{id}` | Source-specified | Tool metadata; auth/schema incomplete; unverified. |
| `GET /api/v1/integrations/{id}/sync-jobs/{job_id}` | Additional proposal | Sync job status; unverified. |
| `POST /api/v1/integrations/{id}/sync-jobs/{job_id}/cancel` | Additional proposal | Cancel job; unverified. |
| `POST /api/v1/webhooks/github/{connection_id}` | Illustrative proposal | GitHub callback; signature/binding required; route unresolved; unverified. |
| `POST /internal/v1/audit/events`, `POST /internal/v1/events` | Proposed CT-06 | Authenticated service producers; workload/tenant contract; unverified. |
| `POST /internal/v1/work-items/import` | Proposed CT-02 | T2 work import; unverified. |
| `POST /internal/v1/engineering/import` | Proposed CT-03 | T3 handoff; no source ingest route; unverified. |
| `POST /internal/v1/incidents/import` | Proposed CT-04 | T4 handoff; unverified. |
| `POST /internal/v1/authorization/decisions` | Illustrative CT-01 | Permission lookup; service identity/transport unresolved; unverified. |
| `GET /api/v1/ai/requests/{id}`, `/api/v1/ai/runs/{id}` | Additional proposals | Async AI status; scoped authority; unverified. |
| `POST /api/v1/ai/runs/{id}/cancel`, `/resume` | Additional proposals | Cancel/resume; resume with approval ref/current checks; unverified. |

Historical Team 5 auth routes POST `/api/v1/auth/login`, `/logout`, `/refresh`; GET `/api/v1/permissions`, `/roles`; abbreviated `/auth/login`, `/auth/refresh`, `check_permission(...)` are not target T5 APIs under current ownership; reassign to T1. Other-team dependencies: T1 organization/people/assignment, T2 project/member/task, T3 repository, T4 incident/timeline/evidence/RCA/related-change source paths. They are intentions, not accepted integrations; canonical import routes are missing.

**Evidence:** [api-contracts.md](api-contracts.md) §§2,6–8; [PRD.md](PRD.md) FR-PLAT-001; [NEXORA_PROJECT_MASTER_DOCUMENT.md](NEXORA_PROJECT_MASTER_DOCUMENT.md) §10.

## 10. Implementation status matrix

“CONFIRMED” in PRD means requirement confirmed, not built. UNVERIFIED means no code/runtime proof in docs. Validation report says no app source, manifest, deployment config, tests or cross-team service in inspected workspace. Source inspection is required to determine status elsewhere.

| Component | PLAT ID | Purpose | Status | Dependencies / remaining work |
|---|---|---|---|---|
| Foundation | M01/001 | Config/API/errors/logging/DB/health/version. | UNVERIFIED; planned. | Q03/09/14, CT-05; locate repo, implement/test. |
| T1 auth adapter | M02/002 | Consume T1 identity; no T5 issuer/store. | UNVERIFIED; CT-01 open. | Q01/02, T1; agree protocol/delegation/revocation, test. |
| Resource authorization | M02/003 | Enforce grants and owner resource scope. | UNVERIFIED. | CT-01–04, Q01/02/16; vocabulary and fail-closed tests. |
| Tenant context | M02/004 | Validate organization/isolate records. | UNVERIFIED. | CT-01, Q02/15; rules and two-tenant tests. |
| Audit/events | M03/005 | Audit capture/query. | UNVERIFIED. | CT-06, Q10/11/15; schema/failure/retention agreement. |
| Connector framework | M04/006 | Seven methods/lifecycle/fetch/sync/webhook. | UNVERIFIED; names documented. | CT-01/05, Q04/06; signatures/capability registry/conformance. |
| GitHub | M05/007 | Fetch/webhooks/map to T3. | UNVERIFIED; target requirement only. | CT-03, Q02/04/06; scopes/schema/owner ack/E2E. |
| PM adapters | M06/008 | Selected work provider to T2. | UNVERIFIED; planned P1. | CT-02/Q02/04/06/13; choose provider/direction/import semantics. |
| Observability | M07/009 | Bounded source input to T4. | UNVERIFIED; planned P1. | CT-04/Q05/06/10/13; service owner/provider/evidence boundary. |
| AI gateway | M08/010 | Route/validate/call provider and track attempts. | UNVERIFIED; provider unselected. | CT-07/Q06/07/09/10; route/data/secret choices. |
| Registry | M09/011 | Versioned agents/tools/schemas/permissions/risk. | UNVERIFIED. | CT-01/07/Q08/15; admin/version rules/handlers. |
| Runtime/context | M09/012 | Authorized context and bounded execution. | UNVERIFIED. | CT-02–04/07, Q07–10; context/provenance/cancel tests. |
| Policy/approval | M10/013 | Restrict/gate tools and approval. | UNVERIFIED; writes gated. | CT-01/04/07, Q08/13; proof/race/revocation; no merge/deploy. |
| Usage/cost | M11/014 | Per-attempt usage and estimates. | UNVERIFIED; report P1. | Q07/10, CT-07; minimum ledger with first AI; price/currency. |
| Evaluation | M12/015 | Versioned cases/runs/results. | UNVERIFIED; eventual P1. | T3/T4, Q10/12; fixtures/rubric/release criteria. |
| Events/notifications | M03/016 | Common event delivery; notification capability. | UNVERIFIED; P1/channel open. | CT-06/Q10/11/13; producer/subscriber/retry/channel rules. |
| Secret/egress | SEC-001 | Secret refs, rotation, destination controls. | UNVERIFIED; proposed. | Q06/14, CT-01; select store and test rotation/SSRF/disconnect. |
| Webhook security | SEC-002 | Verify provider/tenant and durable receipt. | UNVERIFIED; proposed. | Q06/09/10, REL-001; provider-specific signature/replay tests. |
| AI executable boundary | SEC-003 | Treat inputs/output as untrusted; deterministic validation. | UNVERIFIED; proposed. | PLAT-011–013, Q08/10; handlers/adversarial tests. |
| Durable recovery | REL-001 | Jobs/idempotency/leases/unknown outcomes. | UNVERIFIED; proposed. | Q03/04/09/10/14, owner ack; worker/crash/reconcile tests. |
| Mapping integrity | DATA-001 | Tenant-scoped mappings/references. | UNVERIFIED; proposed. | CT-01–04, Q02/04/15; approved schema/owner checks. |
| Deployment/recovery | OPS-001 | Deploy/migrate/rollback/restore/runbook. | UNVERIFIED; proposed gate. | Q03/09/10/14; actual deploy/restore evidence and owner. |
| T01–T03 prep | Tasks | Conflict review, fixtures, acceptance/adversarial design. | READY only as prep; completion not verified here. | Docs; stakeholder decisions/records still needed. |

Static validation PASS concerns documents, not implementation.

**Evidence:** [validation-report.md](validation-report.md) §§1–5; [implementation-plan.md](implementation-plan.md) §§1–2,4–5; [README.md](README.md) lines 19–28.

## 11. Dependency and contract matrix

| Dependency | Provider | Consumer | Purpose | Contract status | Blocking impact |
|---|---|---|---|---|---|
| CT-01 identity/membership/permission/delegation | T1 | T5, all teams | Identity, org, grants, workload/delegation, revocation. | Target owner T1; Q01/02 open. | Protected APIs, jobs and AI. |
| CT-02 work context/import | T2 | T5, then T3/T4 | Project/task reads and proposed import/receipt. | Proposed; Q02/04/16. | Live PM import/context. |
| CT-03 engineering handoff | T3 | T5; T4 context | GitHub records, IDs, canonical reads. | Proposed; source ingest route absent; Q02/04/05. | GitHub-to-T3 completion. |
| CT-04 incident/evidence/approval | T4 | T5 | Incident ingest/context, evidence and review ref. | Proposed; Q04/05/08/10. | Observability/RCA and writes. |
| CT-05 T5 API | T5 | Clients/T1–4 | Foundation/integration lifecycle/status/common API. | Paths source-listed; behavior proposed; Q03/09/14/15. | Client integration/release. |
| CT-06 audit/events | Domain producers + T5 | T1–4 | Audit intake/query and durable events. | Proposed; Q10/11. | Production events/audit/notifications. |
| CT-07 AI/tools | T5 | T3/T4/authorized clients | Gateway/registry/execution/policy/usage/eval. | Proposed; Q07/08/12/13. | Live model/tool use. |
| IDs/tenant | T1–4/coordinator | All | IDs, tenant derivation, user/employee/external actor. | Unresolved Q02/15/16. | Isolation/schema/mapping. |
| Service catalog | Owner TBD | T3/T4/T5 | Service identity/evidence linkage. | Unresolved Q05. | Service-scoped observability. |
| Provider/secrets/egress | Admin/security/ops + T5 | T5 | Accounts/scopes/secrets/rotation/allowlists. | Unresolved Q06/14. | Live connectors. |
| AI data/cost | Coordinator/data/security/budget + T5 | T3/T4 | Model/data/rates/fallback/budget. | Unresolved Q07/10/12. | Live/paid AI/cost claims. |
| Membership vs allocation | T1 and T2 | T5/domain consumers | Project people/access semantics. | Unresolved Q16. | Membership authorization. |
| Audit/event policy | Producers/consumers/coordinator | T5 | Event catalog/retention/ack/replay/notifications. | Unresolved Q10/11. | Production delivery. |

Conflicts C01–C10: identity ownership; organization in T5 ERD; duplicate GitHub repository; external work duplication/membership; service/telemetry/evidence config; ID and user/employee mismatch; priority totals; events/notifications underspecified; assisted writes vs future workflow; staff spelling/QA ambiguity. Directional resolutions are not stakeholder acceptance.

**Evidence:** [api-contracts.md](api-contracts.md) contract register; [source-inventory.md](source-inventory.md) C01–C10/ownership matrix; [open-questions.md](open-questions.md) Q01–Q16.

## 12. End-to-end data flows

### GitHub → Team 3

```text
GitHub API/event --> T5 connection/scope check --> verified webhook OR bounded fetch/sync
  --> proposed inbox/job + dedupe/lease --> typed envelope/external mapping
  --> Team 3 owner API (schema/route not agreed)
  --> T3 validates tenant/domain, persists canonical record and receipt
  --> T5 stores mapping/checkpoint/status/audit --> T3 change intelligence
```

Webhook is push; fetch/sync may be request or worker initiated. Worker is proposed, not evidenced. Owner ack precedes checkpoint; no direct T3 DB write.

### Jira / Linear → Team 2

```text
Selected provider (subset/direction open) --> T5 approved read/sync
  --> tenant/connection-scoped mapping --> proposed T2 import + idempotency key
  --> T2 validates project/status/parent/assignee/conflicts and commits
  --> owner receipt/ID --> T5 mapping/checkpoint/sync status
```

Initial inbound-only flow is proposed. Poll/webhook mode is provider-dependent and not finalized; no import API/schema or bidirectional write is approved.

### Sentry / Datadog / PagerDuty → Team 4

```text
Selected provider (open) --> T5 verifies connection and bounds event/query
  --> provenance/completeness envelope --> proposed T4 import/context contract
  --> T4 canonicalizes incident/evidence and owns severity/state
  --> T4 correlates T1–3 data and performs RCA/review
  --> T5 supplies governed AI/runtime/audit/usage if requested
```

Incident push, telemetry pull and log/metric/trace queries differ. Empty, partial, denied, stale and failed stay distinct. Service owner/API unresolved.

### Team 1 auth/tenant → Team 5

```text
Caller identity + selected org/resource --> accepted CT-01 T5 adapter
  --> T1 validates identity/status/membership/permission/delegation
  --> owner checks resource tenant/scope --> T5 enforces scoped operation + audit
  --> invalid/revoked/unavailable/mismatch => deny or unavailable
```

Token/introspection, service identity, caching/revocation and routes are unresolved. Header/body org is not membership proof; user ≠ employee.

### AI Gateway → consuming teams

```text
T3/T4 request --> T1/resource authorization + data policy
  --> permitted owner context with provenance/partial state
  --> bounded runtime --> M08 approved route --> validated advisory result
  --> attempt/usage/audit --> optional tool policy/approval/fixed handler
  --> domain owner validates and persists business meaning
```

Interactive sync vs async status mode is undecided. No model/provider/context API chosen. Timeout may be unknown billable outcome; no silent fallback or unsafe retry.

**Evidence:** [architecture.md](architecture.md) §§2.4–2.5,7,10–13; [PRD.md](PRD.md) W01–W06/E2E; [api-contracts.md](api-contracts.md) CT-02–07.

## 13. Required line-based diagrams

**Legend:** DOCUMENTED = source ownership/capability; PROPOSED = design; UNRESOLVED = pending. No diagram claims implementation.

### Diagram 1 — Overall Nexora Team Architecture

```text
                       Nexora users / domain clients
                         |       |       |       |
                         v       v       v       v
+------------------+ +------------------+ +-----------------------+
| T1 DOCUMENTED    | | T2 DOCUMENTED    | | T3 DOCUMENTED         |
| Org, users,      | | Canonical project| | Canonical engineering |
| auth, RBAC       | | and work         | | + change intelligence |
+--------+---------+ +--------+---------+ +-----------+-----------+
         | CT-01 authority          ^                  ^
         v                          | CT-02            | CT-03
+--------+---------------------------------------------------------+
| T5 PROPOSED: foundation, access, audit/events, connector, AI     |
+--------+---------------------------+-----------------------------+
         | CT-04                     | provider/model calls
         v                           v
+--------+---------+          +------+--------------------+
| T4 DOCUMENTED   |          | External providers        |
| Incident/evidence|          | GitHub, PM/observability |
| RCA/review/history|         | candidates                |
+-----------------+          +---------------------------+
T3/T4 -- governed AI request --> T5. Canonical data stays at owners.
All runtime transport requires contract acceptance.
```

### Diagram 2 — Team 5 Internal Architecture

```text
Client/provider callback --> M01 API/foundation (PROPOSED)
                                |
                                v
                     M02 access / tenant / owner checks
                        |                    |
                        v                    v
                 M04 connector         M09 registry/runtime
                 /   |    \             /      |      \
               M05  M06   M07        M10 policy M08 gateway --> model TBD
                GH   PM    Obs           |          |
                 \   |    /              +------- M11 usage
                  owner APIs                         |
                    |                              M12 evaluation
                    +---------- M03 audit/events --+
T5 PostgreSQL + worker are proposals; logging/metrics != audit.
```

### Diagram 3 — Integration Framework

```text
Provider registry/capability check (PROPOSED)
  --> common interface: authenticate/connect/disconnect/health_check/
      sync/fetch/handle_webhook (names DOCUMENTED)
  --> provider adapter --> connection/secret ref/tenant binding
  --> fetch/sync OR verified webhook --> inbox/job/dedupe (PROPOSED)
  --> normalization/provenance --> owner-approved envelope
  --> T2/T3/T4 validates/persists --> owner receipt
  --> T5 mapping/checkpoint/status/audit
Provider caps/schema/owner API remain UNRESOLVED.
```

### Diagram 4 — Team 5 services to Team 1

```text
T1 [DOCUMENTED: org/user/auth/RBAC authority]
  -- CT-01 identity/membership/permission/delegation -->
T5 M02 [PROPOSED: consume identity, validate tenant, enforce]
  --> tenant-scoped platform APIs/connectors/AI
  --> T2/T3/T4 owner checks for their resources
Protocol/routes/revocation UNRESOLVED. T5 issues no credentials.
```

### Diagram 5 — Team 5 services to Team 2

```text
Jira / Linear / Azure DevOps (subset UNRESOLVED)
  --> T5 M04/M06 connector + external mapping
  --> proposed Canonical Work Item envelope --> T2 validation/commit
  --> owner receipt/ID --> T5 checkpoint --> T2 canonical work
Import-only is proposed; no T5 task master or approved write-back.
```

### Diagram 6 — Team 5 services to Team 3

```text
GitHub (initial target; scope UNRESOLVED)
  --> T5 M05 verify/fetch/webhook/map engineering records
  --> proposed Canonical Pull Request/engineering envelope
  --> T3 tenant/domain validation + canonical persistence
  --> T3 receipt --> T5 mapping/checkpoint
  --> T3 work-code links/metrics/impact/change intelligence
T5 owns no canonical engineering or automatic provider writes.
```

### Diagram 7 — Team 5 services to Team 4

```text
Sentry / Datadog / PagerDuty / telemetry (selection UNRESOLVED)
  --> T5 M07 verified/bounded transport + provenance/completeness
  --> proposed incident/evidence envelope --> T4 canonicalizes/interprets
  --> T4 correlates T1 org + T2 work + T3 engineering/deployments
  --> T4 RCA/remediation/validation/human review
  <-- T5 gateway/runtime/policy/audit/usage if requested
Service catalog, source API, approval and retention UNRESOLVED.
```

### Diagram 8 — AI Platform Architecture

```text
T3/T4 request --> M02 identity + owner access --> M09 agent/context
  --> M10 policy/data/tool gate --> M08 approved provider (TBD)
  --> validated result --> M11 per-attempt usage (unknown preserved)
  --> optional typed tool proposal --> current auth + exact approval
  --> fixed handler/owner API --> audit outcome
M12 evaluates synthetic/redacted cases with T3/T4 rubric (later).
All modules planned; no automatic merge/deploy.
```

### Diagram 9 — Complete End-to-End Platform Flow

```text
T1 identity/org --CT-01--> T5 access/tenant boundary
Provider --webhook/fetch--> T5 connector --envelope--> T2/T3/T4 owner
                              |                         |
                              +--> sync/audit/event     +--> canonical data
T2 work ----context/API----+                                + business logic
T3 code/build/deploy ------+--> T4 evidence/RCA or T3/T4 agent
                                      |
                                      +--> T5 registry/policy/gateway
                                              +--> approved model TBD
                                              +--> fixed authorized tool
                                              +--> audit/usage/eval
T1 owns identity; T2 work; T3 engineering; T4 incident/RCA;
T5 shared infrastructure. CT/provider/model/deploy remain proposed.
```

**Diagram sources:** [architecture.md](architecture.md) §§2–3,7,10–14; [PRD.md](PRD.md) §§7,11; [NEXORA_PROJECT_MASTER_DOCUMENT.md](NEXORA_PROJECT_MASTER_DOCUMENT.md) §§6,13,17. Mermaid structural check only.

## 14. Documentation gaps, conflicts and blockers

| Gap/source | Missing or conflicting information | Owner if known | Why it matters / blocks |
|---|---|---|---|
| C01/Q01 identity | Old specs assign auth/RBAC to T5; current direction gives T1 authority. Token/introspection, service identity, delegation/revocation absent. | Coordinator, T1, T5. | Protected APIs, jobs and AI. |
| C06/Q02 IDs/tenant | PDF IDs vs ERD UUID; user vs employee; multi-org/external-author mapping and lifecycle unclear. | T1/all leads. | Schema, isolation and mapping. |
| Q03 topology | No repo/package/runtime/ORM/migration/DB/worker/deployment conventions. | T5 technical lead/ops. | Implementation and migrations. |
| Q04 ingestion | No accepted work/engineering/incident payload, ack, revision, conflict/delete/order/partial rules. | T2/T3/T4 + T5. | Live provider-to-owner flows. |
| C05/Q05 service | Service owner/API/project-org relationship/evidence source link unresolved. | Coordinator/T3/T4/T5. | Service-scoped observability/correlation. |
| Q06 providers/secrets | Provider account/scope, secret store/rotation, egress, webhook capability absent. | T5/provider admin/security/ops. | Live connectors/webhooks. |
| Q07 AI route/cost | Model/vendor/version, data class/fallback/limits/rates/currency/budget absent. | Coordinator/data/security/budget/T3/T4/T5. | Live/paid AI and cost claims. |
| C09/Q08 approvals | Who approves writes; binding/revocation/race; test isolation; T4 review vs technical permission. | Coordinator/T1/T4/T5/provider owner. | Write tools; read-only still needs auth. |
| Q09 NFR | Volumes, latency, availability, lag, retry/concurrency thresholds absent. | Product/coordinator/T5/ops/teams. | Sizing/performance acceptance. |
| Q10 privacy | Classification/disclosure/residency, raw retention, purge/hold, backups absent. | Coordinator/data/security/domain owners. | Production data and real AI. |
| C08/Q11 events | Event catalog, producer/consumer, replay/order, audit outage, notification channel/recipient/preferences absent. | T5/all teams/coordinator. | Production events/notifications. |
| Q12 evaluation | Dataset, ground truth, rubric, threshold, human release gate absent. | T3/T4/T5/coordinator. | Quality claims/acceptance. |
| C07/C10 Q13/Q16 | P0/P1 count mismatch; names/QA conflict; ~6 gross hrs/day, no dates. | Coordinator/T5/domain leads. | Scope/staff commitments. |
| Q14 operations | Host/TLS/backup/restore/monitoring/on-call/RPO/RTO absent. | T5 technical/ops/coordinator. | Production readiness. |
| C02–06/Q15 ERD | Duplicate domains, missing tenant fields, schema drift; no approved DDL. | T5 and domain owners. | Final schema/migrations. |
| Q16 membership | T1 allocation vs T2 project membership/permission unclear. | T1/T2. | Membership-based authorization. |
| Connector signatures | Seven names only; no DTOs/errors/version/concurrency/discovery. | T5/provider owners. | Reusable interface implementation. |
| Canonical schemas | Concepts named but no accepted PR/work-item/incident schema. | Domain owners/T5. | Safe mapping/API. |
| API contracts | Source paths lack auth/request/response/error details; added routes are proposals. | Each route owner/T5. | Client integration. |
| Execution mechanism | Worker/broker/sync-event async behavior is proposed, not evidenced. | T5/ops. | Durability/recovery claims. |
| Original artifacts | PDFs/ERD images are summaries, not local Markdown. | Documentation owner. | Direct original-source reinspection. |

ADRs are proposed; no acceptance record is documented. Static validation does not establish app behavior. This evidence limit does not establish the state of an unprovided repository/private environment.

## 15. Evidence register and main takeaways

**Evidence map:** scope [PRD.md](PRD.md) §§2–6 and [source-inventory.md](source-inventory.md); modules/flows [architecture.md](architecture.md) §§1–15; API [api-contracts.md](api-contracts.md) CT-01–07; data [database-schema.md](database-schema.md) §§1–8; security [security.md](security.md) §§1–7; task status [implementation-plan.md](implementation-plan.md) §§1–5; decisions [open-questions.md](open-questions.md) Q01–16; conflicts [source-inventory.md](source-inventory.md) C01–10; static limits [validation-report.md](validation-report.md); ADRs `docs/adr/`; onboarding synthesis [NEXORA_PROJECT_MASTER_DOCUMENT.md](NEXORA_PROJECT_MASTER_DOCUMENT.md).

1. Team 5 is shared infrastructure, not a fifth canonical business domain.
2. T1 is identity/org/RBAC authority; T5 consumes/enforces. Historical T5 assignment remains a conflict.
3. T2 owns work; T3 engineering; T4 incident/RCA. T5 transports provider data and keeps integration state.
4. PLAT-006 has seven method names but no signatures/implementation evidence; provider capabilities differ.
5. GitHub is initial target; PM/observability providers remain candidates/gated.
6. Canonical PR/Work Item/Incident are not accepted schemas. Proposal examples are not canonical contracts.
7. FastAPI/PostgreSQL are high-level named stack; API/worker/inbox/outbox/leases/schema are proposals.
8. AI is intended as permission-bound advisory infrastructure with registered tools, audit and human review; no provider selected, no automatic merge/deploy.
9. No component is confirmed implemented by these docs. Documentation validation passed; app status unverified.
10. C01–C10 and Q01–Q16 leave substantial cross-team/API/security/ops work. T01–T03 are prep, not shipped features.

## 16. Limits of Markdown evidence

- This report covers local Markdown under `docs/`. Six PDFs, five team ERD images and a staffing image are summarized/cited by `source-inventory.md`; master document says they are absent from the local docs workspace. Direct artifact reinspection is outside this Markdown-only analysis.
- At report preparation, the working tree showed untracked `src/nexora_platform/integrations/core/{contracts.py,errors.py,registry.py}` and `tests/unit/test_connector_registry.py`. These files were not inspected or used as implementation evidence. This differs from the older validation report's statement that no app source/test suite existed in its inspected workspace; current feature status therefore remains UNVERIFIED pending source/test review.
- Markdown cannot establish code in another repository, running services, provider accounts/credentials or private post-document decisions.
- Validator PASS concerns docs/examples, not endpoints/migrations/provider calls/security. Mermaid was not renderer-parsed.
- No endpoint/schema/auth protocol/tenant implementation/worker/model/deployment topology is final without separate acceptance and verification.

## Appendix A — Complete inspected path list

1. `docs/api-contracts.md`
2. `docs/architecture.md`
3. `docs/database-schema.md`
4. `docs/implementation-plan.md`
5. `docs/NEXORA_PROJECT_MASTER_DOCUMENT.md`
6. `docs/open-questions.md`
7. `docs/PRD.md`
8. `docs/README.md`
9. `docs/security.md`
10. `docs/source-inventory.md`
11. `docs/validation-report.md`
12. `docs/adr/ADR-0001-identity-and-ownership-boundary.md`
13. `docs/adr/ADR-0002-modular-service-and-durable-work.md`
14. `docs/adr/ADR-0003-contract-based-cross-team-exchange.md`
15. `docs/adr/ADR-0004-gated-ai-tool-execution.md`
16. `docs/adr/ADR-0005-tenant-scoped-integration-references.md`
17. `docs/adr/ADR-0006-minimized-ai-data-and-usage-ledger.md`
18. `docs/adr/README.md`

**Inspected count: 18 Markdown documents.**
