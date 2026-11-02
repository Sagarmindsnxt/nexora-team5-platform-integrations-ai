# Nexora Team 5 open decision register

Version 0.1 | Updated 2026-10-27 | Owner: Team 5 / Sagar | Status: OPEN DECISION; no decisions below have stakeholder approval recorded.

This is the authoritative open-question index for the documentation set. Sources and C01-C10 conflicts are in [source-inventory.md](source-inventory.md). Functional requirements are in [PRD.md](PRD.md), proposed contracts CT-01-CT-07 in [api-contracts.md](api-contracts.md), and task readiness in [implementation-plan.md](implementation-plan.md). A recommended option is PROPOSED, not a recorded choice. Sagar coordinates decisions but cannot accept another team's contract or a coordinator-owned scope choice on that team's behalf. “Before implementation” means the affected live behavior or irreversible schema choice; source review, fixtures and draft contracts may proceed where explicitly marked ready.

No deadline or individual commitment is inferred. Resolution phases are proposed gates, not dates. To close a question, record the decision, rationale, accountable approver(s), decision date, accepted contract/schema/ADR version, affected requirement/task updates, and evidence of acceptance. Unsupported defaults must not silently turn an open question into a decision.

## Q01 — Authentication and authorization handoff

| Field | Record |
|---|---|
| Question | How will Team 1 expose authentication, session/account status, organization membership and authorization after the coordinator's current ownership change? Which historical Team 5 auth/roles/permissions interfaces are transferred or retired? |
| Why it matters | C01 affects every protected route, agent/tool call and worker. A second identity/RBAC authority would create conflicting permission decisions. |
| Affected requirements / modules | FR-PLAT-002, FR-PLAT-003, FR-PLAT-004, FR-PLAT-005, FR-PLAT-011, FR-PLAT-012, FR-PLAT-013; identity adapter, tenant enforcement, audit, AI runtime; CT-01. |
| Options | Trusted signed access-token validation plus agreed authorization lookup; online token introspection plus permission lookup; shared interface library against Team 1 authority. Token format, issuer/audience, expiry, revocation/freshness and service identity are all unresolved. |
| Recommendation | Preserve confirmed Team 1 authority; define a small request-context/permission contract, fail closed on unavailable or invalid authorization, and make session lifecycle policy explicit. Keep login, password handling, sessions and grant administration out of Team 5. |
| Decision owner | Coordinator confirms reassignment; Avinash owns Team 1 contract; Sagar owns Team 5 enforcement integration. |
| Blocking / phase | YES: live protected APIs, workers with delegated authority and AI access. Contract drafts and deny-path fixtures can begin. Resolve at contract baseline before protected feature implementation. |
| Closure evidence | Accepted CT-01 including test vectors for invalid token, disabled account, revoked permission, wrong organization, service identity and dependency outage; historical API ownership updated. |

## Q02 — Identifiers, tenant context and user/employee mapping

| Field | Record |
|---|---|
| Question | What are stable IDs and wire formats for organization, authenticated user, employee, team, project, repository, PR, incident and service? Can one user belong to multiple organizations; how is an active organization validated? How are external authors mapped? |
| Why it matters | C06: PDF sample IDs and ERD UUIDs disagree; user and employee are distinct records. Trusting caller-supplied organization or guessing identity from email permits incorrect attribution and tenant access. |
| Affected requirements / modules | FR-PLAT-002 through FR-PLAT-005, FR-PLAT-006 through FR-PLAT-016, FR-DATA-001; all tenant-bearing data, context builders and external mappings; CT-01-CT-07. |
| Options | Opaque stable strings at service boundary with per-owner validation; common UUID format if all owners explicitly agree. Organization in verified claims plus membership verification, or selected org validated online. External actors can remain unresolved rather than auto-linked. |
| Recommendation | Treat foreign IDs as opaque until contracts settle; retain separate user_id and employee_id; keep authoritative organization in trusted execution context, recheck resource ownership, and require explicit external identity mapping provenance. All tenant tables, deduplication and caches must include tenant scope. |
| Decision owner | Avinash for identity/membership; all domain leads for their IDs; Sagar for platform propagation; coordinator for common conventions. |
| Blocking / phase | YES: schema finalization, live isolation and cross-team payload acceptance. Synthetic IDs may be used only in labelled fixtures. Resolve at contract baseline. |
| Closure evidence | Published identifier dictionary and tenant derivation rules, lifecycle/deletion behavior, user/employee mapping cardinality, two-tenant negative fixture set. |

## Q03 — Repository, database topology and shared implementation conventions

| Field | Record |
|---|---|
| Question | Where is the actual Nexora repository and what existing structure, package versions and deployment conventions must be preserved? Will teams share a database instance/schema or communicate as independently deployed services? Which ORM/migration/test packages and API conventions are accepted? |
| Why it matters | Only documents were supplied; there is no inspected application code to extend. FastAPI/PostgreSQL are source-stated but package versions, ORM usage, message infrastructure, frontend and service topology are not. |
| Affected requirements / modules | FR-PLAT-001, FR-DATA-001, FR-REL-001, FR-OPS-001; all migrations/modules and CT-05/CT-06 conventions. |
| Options | Modular Team 5 API plus worker and owned PostgreSQL schema; multiple microservices; integrate into an existing modular application if the real repository requires it. Shared instance with separate ownership is different from direct cross-team table access. |
| Recommendation | Use the smallest modular deployment compatible with the real repository, proposed API plus worker with PostgreSQL-backed durable work; no broker or extra services without a concrete need. Use owner APIs/events across boundaries. Recheck folder proposals and dependency versions against the actual repository before scaffolding. |
| Decision owner | Sagar and technical lead Vignesh for technical direction, with affected team leads/coordinator for cross-team deployment boundaries; actual infrastructure owner to be named. |
| Blocking / phase | YES: production structure/migrations/runtime integration. Documentation and architecture review ready. Resolve before implementation setup and migration baseline. |
| Closure evidence | Repository location/revision review, accepted ADR/topology, owned schema permissions, dependency lockfile policy, CI/test/migration conventions and API compatibility/versioning decision. |

## Q04 — Canonical ingestion, external mapping and synchronization semantics

| Field | Record |
|---|---|
| Question | What payloads and acknowledgments will Teams 2-4 accept; who defines each normalization rule; what are duplicate, ordering, partial update, delete, reconciliation, and sync-direction rules? What if external and native edits conflict? |
| Why it matters | C03/C04/C05: Team 5 connector data must not become competing Task/Project/Repository/Incident truth. Team 4 explicitly owns incident normalization. Retry success requires domain acknowledgment and idempotency, not just a provider HTTP response. |
| Affected requirements / modules | FR-PLAT-006, FR-PLAT-007, FR-PLAT-008, FR-PLAT-009, FR-PLAT-016, FR-REL-001, FR-DATA-001; connectors, mapping, durable delivery; CT-02/CT-03/CT-04/CT-06. |
| Options | Versioned domain ingestion APIs; versioned owner-consumed events; read-through context retrieval. One-way import, manual association or bidirectional sync for work items. Domain-owned normalization adapters or Team 5 adapters implementing domain-approved schemas. |
| Recommendation | Start with provider-specific read/import behavior and domain-owned canonical rules; external IDs scoped by tenant/connection/type; at-least-once delivery with receiver deduplication and durable acknowledgments. Avoid bidirectional writes until conflict ownership and delete policy are agreed. Unsupported fields must be explicit rather than guessed. |
| Decision owner | Abhishek for work items, Srushti for engineering, Poonam for incident/evidence semantics, Sagar for transport. |
| Blocking / phase | YES: end-to-end live synchronization. Adapter interface drafts and synthetic transformation fixtures may proceed; finalize before first connector vertical slice. |
| Closure evidence | Signed-off CT-02-CT-04 schemas and examples, external identifier scope, ordering/deletion/conflict policy, replay fixture results and receiver acknowledgment contract. |

## Q05 — Service catalog, delivery records and evidence-source boundary

| Field | Record |
|---|---|
| Question | Who owns the canonical Service catalog, service-to-project/organization relationship and service lookup API? Which Team 3 build/deployment contracts are exposed? How does Team 4 evidence_source reference Team 5 telemetry connections? |
| Why it matters | C05: service appears in the Team 5 ERD and Team 3/4 graphs without an agreed owner. Builds/deployments are explicitly Team 3 deliverables; evidence is Team 4-owned. Duplicating connection configuration can expose secrets and drift. |
| Affected requirements / modules | FR-PLAT-007, FR-PLAT-009, FR-PLAT-011, FR-PLAT-012, FR-DATA-001; engineering/observability adapters and context building; CT-03/CT-04. |
| Options | Assign Service to a named domain team with platform references; or explicitly assign a minimal service catalog to Team 5 after coordinator approval. Keep T4 evidence-source descriptors linked to T5 connection IDs instead of credential copies. |
| Recommendation | Coordinator assigns one service owner. Preserve confirmed T3 canonical build/deployment ownership and T4 evidence/investigation ownership. Team 5 can manage provider connection metadata and deliver authorized telemetry, while Team 4 owns relevance/correlation/storage. |
| Decision owner | Coordinator with Srushti, Poonam and Sagar. |
| Blocking / phase | YES: canonical service persistence, service-scoped authorization and live evidence assembly. Does not block generic connector/gateway design. Resolve before observability/RCA integration. |
| Closure evidence | Named service authority/API and identifiers, ownership mapping, accepted build/deployment payloads, and evidence-source connection-reference model. |

## Q06 — Provider selection, credentials, egress and connector capability profiles

| Field | Record |
|---|---|
| Question | Which GitHub tenancy/installation method, project-management provider and observability provider are in the first increment? Which credentials/scopes, approved destinations, secret store, rotation/revocation method, webhook signature scheme and rate limits apply? |
| Why it matters | Listed provider examples are not evidence of an installed account, available credential or uniform capabilities. Generic connect/fetch/sync/webhook methods cannot imply every provider supports every method. |
| Affected requirements / modules | FR-PLAT-006 through FR-PLAT-009, FR-SEC-001, FR-SEC-002, FR-REL-001; connector registry, credential references, webhook ingress and outbound clients. |
| Options | Provider installation/app authorization vs approved scoped token; one selected provider per category vs multiple concurrently; capability-specific adapters sharing common lifecycle/transport. Secret-store integration chosen with operations. |
| Recommendation | Confirm first GitHub scope, then one approved provider at a time; credentials as secret references, explicit read-only initial scopes, host allowlist, bounded response sizes and provider-specific verification. No real credential needed for synthetic tests. |
| Decision owner | Sagar and Sharanbasava with provider-account administrator/security/operations owner; coordinator/domain lead selects business priority. |
| Blocking / phase | YES: live connector or paid/provider-account access. Common interface and fake-provider tests may proceed after internal architecture approval. Resolve before provider integration testing. |
| Closure evidence | Provider profile with capability flags, allowed endpoints/scopes, credential ownership and rotation runbook, redacted signature/rate-limit fixtures, and approved account/environment. |

## Q07 — AI models, request policy, usage accounting and budgets

| Field | Record |
|---|---|
| Question | Which provider/model/version and data-processing arrangement may be used; what routing/fallback rules apply; what token/step/time/cost budgets and pricing units/currencies/effective periods are accepted? How are unknown usage, retries and estimates reconciled? |
| Why it matters | No approved model/provider/price/budget exists in sources. Gateway usage/cost handling is P0 while aggregate reporting is P1. Retries may incur billable work without a successful response. |
| Affected requirements / modules | FR-PLAT-010, FR-PLAT-012, FR-PLAT-013, FR-PLAT-014, FR-PLAT-015, FR-REL-001; gateway, model catalog, usage/cost and agent budgets; CT-07. |
| Options | One explicitly allowed provider/model initially; per-use-case routes; fallback only among approved providers with compatible data policy. Hard reservation limits or alerts; unknown billable state reconciled manually/provider-side rather than recorded as zero. |
| Recommendation | Single approved route initially, bounded execution, record attempts and actual-vs-estimated/unknown usage separately, version prices, prevent duplicate metering and reserve budget before dispatch if approved. Any numerical limit in implementation is a proposal until accepted; no silent cross-provider fallback. |
| Decision owner | Sagar with coordinator/budget holder, security/data owner and Teams 3/4 use-case owners. |
| Blocking / phase | YES: real model calls, pricing reports presented as authoritative or budget enforcement. Fake provider can test lifecycle without spending. Resolve before AI pilot. |
| Closure evidence | Approved model profile, limits/routing/failure policy, pricing source/version/unit/currency, retry/reconciliation rules and accounting test examples. |

## Q08 — Tool risk, human approvals and execution authority

| Field | Record |
|---|---|
| Question | Which tools are enabled in each phase; who may approve which operation; does Team 4 domain review authorize a concrete Team 5 execution; how are approval identity, tenant, tool version, resource/input digest, expiry and revocation bound? Where may tests/code changes execute? |
| Why it matters | C09: tool examples include writes, but T4 marks branch/patch/test/PR flow future. Model output cannot grant permission. Generic approval unrelated to exact operation is unsafe and untestable. |
| Affected requirements / modules | FR-PLAT-011, FR-PLAT-012, FR-PLAT-013, FR-SEC-003; tool registry, policy, execution/approval and T4 handoff; CT-04/CT-07. |
| Options | Advisory/read tools only; assisted writes with per-operation human approval; explicitly approved narrow automation. Separate technical approval from domain review, or signed/verifiable domain approval evidence under agreed semantics. |
| Recommendation | Start advisory; explicitly deny merge/deploy/production mutation. Require resource authorization at execution time, immutable operation binding, no permission expansion by model text, and isolated approved execution for future tests/patches. Keep Team 4 domain workflow ownership. |
| Decision owner | Coordinator and Poonam for remediation scope; Sagar for policy/security; Avinash for delegated permission; provider/resource owner for external writes. |
| Blocking / phase | YES: any write or elevated tool execution; read-only execution still requires Q01/Q02 and accepted tool profile. Resolve before enabling each tool class. |
| Closure evidence | Accepted risk/permission/approval matrix, replay/expiry/changed-input/changed-permission negative tests and explicit approval proof contract. |

## Q09 — Capacity, performance, availability and recovery objectives

| Field | Record |
|---|---|
| Question | What organization/user/provider volumes, concurrent AI runs, event bursts and data sizes must be supported; what latency, availability, sync-lag, restore-time/data-loss and support targets are required? |
| Why it matters | Sources contain no measured baselines or numeric SLOs. Capacity assumptions drive worker limits, database sizing, test workloads and operational obligations for a part-time team. |
| Affected requirements / modules | FR-PLAT-001, FR-PLAT-006, FR-PLAT-010, FR-PLAT-012, FR-REL-001, FR-OPS-001; API/worker/database/observability and PRD NFRs. |
| Options | Explicit small pilot workload then measured scaling; larger supported launch envelope with funded operations. Targets per API class rather than including external-model latency in one blanket SLA. |
| Recommendation | Agree workload and test data first, measure a pilot, then set approved latency/error/lag/recovery targets. Keep provider time separate and bounded; do not invent 24/7 coverage or numeric guarantees. |
| Decision owner | Coordinator/product owner, Sagar, technical lead and operations owner; all teams supply expected workloads. |
| Blocking / phase | YES: performance/availability acceptance and production sizing, not deterministic functional test drafting. Resolve before pilot acceptance and production readiness. |
| Closure evidence | Workload matrix, agreed targets/baselines and load/restore test procedures with pass criteria. |

## Q10 — Data classification, retention, residency and deletion

| Field | Record |
|---|---|
| Question | Which source code, employee data, telemetry, prompts, tool results and evidence may leave the system or be retained; where; for how long; under what access/deletion/hold policy? How are audit durability, user erasure and provider retention reconciled? |
| Why it matters | S12 contains raw prompt/response/payload/config columns with no minimization rules. Domain evidence/AI inputs may contain personal data or credentials; retaining it by default creates uncontrolled exposure. |
| Affected requirements / modules | FR-PLAT-005 through FR-PLAT-016, FR-SEC-001, FR-SEC-003, FR-DATA-001, FR-OPS-001; audit, connector inbox, AI/evaluation storage, backups. |
| Options | Metadata/digests/redacted summaries by default with purpose-approved content retention; encrypted bounded raw payload storage where required; domain-owned evidence retention and Team 5 technical references. |
| Recommendation | Minimize raw content, classify before provider dispatch, redact secrets, tenant-scope retrieval, and require approved retention classes for each storage area including backups/evaluation corpora. Do not assume legal requirements, geography or provider permission. |
| Decision owner | Coordinator/designated data/security stakeholder with Sagar and each domain owner; responsible compliance approver not supplied. |
| Blocking / phase | YES: production data ingestion, persistent raw-content logging, real-model data sharing and retention jobs. Sanitized synthetic data work can proceed. Resolve before pilot data access. |
| Closure evidence | Data-flow/classification table, allowed provider data categories/residency, retention/deletion/hold matrix, redaction tests and access review. |

## Q11 — Audit, platform events and notifications

| Field | Record |
|---|---|
| Question | Which domain events are published, by whom, to which consumers; what versioning/delivery/replay/ordering and audit-failure semantics apply? Which notification channels, recipients, preferences and sensitive fields are in scope? |
| Why it matters | C08: common events are required but channel behavior is unspecified. Domain event delivery and immutable security audit have different failure and retention requirements. |
| Affected requirements / modules | FR-PLAT-005, FR-PLAT-016, FR-REL-001; audit/event ingress, subscriptions, worker and domain outboxes; CT-06. |
| Options | Durable local outbox and HTTP consumers; approved broker later if justified. In-product notifications, external channels or event subscriptions only, each separately scoped. Fail closed on required audit vs durable local retry depending operation. |
| Recommendation | Versioned small event envelopes, domain producer authority, at-least-once acknowledged delivery with deduplication; distinguish business history from audit; no arbitrary outbound webhook URL or notification channel without explicit approval. Audit-failure behavior must be accepted by operation risk. |
| Decision owner | Sagar with all domain leads; coordinator for notification scope and audit retention policy. |
| Blocking / phase | YES: production event handoff, sensitive audit mutations and notification delivery. Schema proposals/synthetic replay tests ready after internal design agreement. Resolve before first cross-team event release. |
| Closure evidence | Event catalog/producer/consumer mapping, CT-06 schema version and failure contracts, required audit list, channel/recipient authorization specification if notifications included. |

## Q12 — AI evaluation datasets, rubrics and release gates

| Field | Record |
|---|---|
| Question | Who supplies sanitized evaluation cases, expected results, evidence-grounding rubrics, thresholds and approval of prompt/model/policy changes? Is evaluation a required release gate for the first AI pilot or a later reporting feature? |
| Why it matters | S06 p15 lists expected/actual results, versions, score/latency/cost but no dataset, metric definition or passing threshold. A generic guardrail result is insufficient evidence of RCA quality. |
| Affected requirements / modules | FR-PLAT-010, FR-PLAT-012, FR-PLAT-013, FR-PLAT-015; evaluation runner, case/result records and T3/T4 agent configuration. |
| Options | Deterministic schema/security tests plus domain-labelled replay corpus; human-reviewed evaluation; scored automated checks where rubric is validated. No invented accuracy percentage. |
| Recommendation | T3/T4 own domain expected results/rubrics; T5 owns reproducible versioned run metadata and infrastructure. Require authorization/redaction/prompt-injection regression tests for any AI release, and agree domain quality gate before pilot. |
| Decision owner | Srushti and Poonam for domain quality; Sagar for platform reproducibility; coordinator for release acceptance. |
| Blocking / phase | YES: claiming AI quality/production acceptance. Evaluation schema and synthetic harness work can proceed after internal approval. Resolve before AI acceptance; rollout scope in Q13. |
| Closure evidence | Versioned sanitized cases, rubric, human review rule, accepted thresholds or qualitative criteria, responsible reviewer and failing-run behavior. |

## Q13 — MVP priorities, release scope and staffing feasibility

| Field | Record |
|---|---|
| Question | Which source P0/P1 capabilities are mandatory for the first release, how is C07's priority-count mismatch resolved, and how will six nominal person-hours/day include review, onboarding, coordination, testing and support? |
| Why it matters | Three people at about two hours each daily cannot responsibly treat all sixteen modules, all providers and advanced agent writes as one ungated delivery promise. Required safety controls cannot be postponed merely because aggregate cost/evaluation modules are P1. |
| Affected requirements / modules | FR-PLAT-001 through FR-PLAT-016 and proposed security/reliability/data/ops requirements; all task readiness/release grouping. |
| Options | Staged access -> GitHub -> governed advisory AI vertical slices, then PM/observability/reporting/evaluation enhancements; alternative domain priority set by coordinator. No deadline established in sources. |
| Recommendation | Confirm source row priorities, split work into reviewable slices, reserve coordination/review capacity, pair Varshini on bounded tests/configuration/redaction tasks, and agree minimum metering/authorization/audit before any real AI call. Keep future write tools separately gated. |
| Decision owner | Coordinator with Sagar and affected leads; each person accepts assignments separately. |
| Blocking / phase | YES: release commitments and activation of proposed work; ready discovery/contract/test design proceeds. Resolve at implementation planning baseline. |
| Closure evidence | Accepted increment scope with feature exits/dependencies, corrected priority interpretation, realistic capacity plan and review allocation; no inferred delivery dates. |

## Q14 — Hosting, deployment, recovery and operational ownership

| Field | Record |
|---|---|
| Question | Where will development/test/staging/production run; who provisions TLS/network/database/secrets/backups; how are migrations, rollout, rollback, alerts, incidents and restore rehearsals owned? |
| Why it matters | No hosting platform, environment inventory or support coverage is supplied. A worker queue without recovery, alert ownership and safe migrations is not deployable completion. |
| Affected requirements / modules | FR-PLAT-001, FR-REL-001, FR-OPS-001; environment config, health/readiness, worker/database, release runbooks. |
| Options | Managed app/database with platform-approved secrets/backups; existing organizational hosting; container deployment if compatible. No Kubernetes/broker requirement inferred. |
| Recommendation | Use existing supported hosting with least operational overhead; separate environment credentials/data, one migration owner, compatible rollback, worker lease recovery, restore validation and named alert responder. Bind numerical recovery goals to Q09. |
| Decision owner | Sagar, Vignesh/technical lead and designated operations owner; coordinator approves support expectations and resources. |
| Blocking / phase | YES: deployment and operational acceptance. Runbook drafts and local fault scenarios ready after internal design decision. Resolve before staging rollout. |
| Closure evidence | Approved environment/config matrix, migration/rollback/backup/restore runbook, service-account ownership, health checks and alert routing exercised in staging. |

## Q15 — ERD reconciliation and schema approval

| Field | Record |
|---|---|
| Question | Which source ERD structures are accepted, replaced or deferred; are Team 5's duplicate organization/repository/work tables only references/projections; what tenant constraints, indexes, state machines, secrets references and retention changes are approved? |
| Why it matters | ERDs are proposals with cross-domain duplication, missing tenant fields and material differences from PDFs. Silent merge would create competing systems of record and unsafe migrations. |
| Affected requirements / modules | FR-DATA-001; FR-PLAT-004 through FR-PLAT-016; all Team 5 persistence and foreign-domain refs. |
| Options | Accept reviewed Team 5-only model with logical external refs; selectively retain source names after reconciliation; shared physical FKs only if Q03/owners agree. Remove duplicate masters or approve narrowly bounded read/transport projections. |
| Recommendation | Review [database-schema.md](database-schema.md) as a proposal; approve only tables for the current increment, with tenant-scoped uniqueness and ownership rules, transaction/replay semantics, and no plaintext secrets/raw sensitive-content default. Keep domain-specific schema changes with respective owners. |
| Decision owner | Sagar plus affected owners Avinash/Abhishek/Srushti/Poonam; technical lead reviews cross-team consequences. |
| Blocking / phase | YES: final migrations and data model acceptance; ERD review/draft migration design can proceed. Resolve per increment before migration implementation. |
| Closure evidence | Entity-by-entity disposition, accepted identifiers/constraints/indexes/state transitions, migration/rollback review and linked ADR decision. |

## Q16 — Project membership, assignments and people references

| Field | Record |
|---|---|
| Question | How do Team 1 organizational project allocations differ from Team 2 project membership/roles; which relationship is authoritative for authorization? Confirm staffing spellings and shared QA identity/availability for review planning. |
| Why it matters | S02 owns employee/team project assignments; S09 introduces project_member/project_role. C10 also has Sharanbasava/Sharanbasva and Meghana/Megha variants. Incorrect membership inference is a security issue; incorrect QA allocation hides delivery dependencies. |
| Affected requirements / modules | FR-PLAT-002, FR-PLAT-003, FR-PLAT-004, FR-PLAT-008, FR-PLAT-012, FR-DATA-001; CT-01/CT-02 context/permission interpretation and implementation review plan. |
| Options | Organizational allocation for planning plus distinct domain membership for access; one agreed membership authority with projections. Shared QA may be one person with naming variation or separately designated resource; not inferable. |
| Recommendation | Separate planning role from authorization unless T1/T2 explicitly define a grant rule; permission decision remains T1-authoritative under accepted resource contract. Use user-provided Team 5 spellings now and leave QA availability uncommitted. |
| Decision owner | Avinash and Abhishek for relationships, Sagar for consumption; coordinator for staffing/QA clarification. |
| Blocking / phase | YES: permission behavior based on project membership and firm review allocation. Does not block independent documentation/test drafting. Resolve membership at contract baseline; staffing before task assignment acceptance. |
| Closure evidence | Written membership/allocation/permission ownership and fixture examples, corrected people references and accepted reviewer allocation. |

## Decision order

1. Sagar coordinates Q01/Q02/Q03/Q13 first: ownership handoff, trust/IDs, real repository and first increment.
2. Each domain lead agrees Q04 and relevant Q05/Q16 contracts; provider administrator resolves Q06. These unlock connector slices without duplicate domain models.
3. Coordinator/data/AI owners resolve Q07/Q08/Q10/Q12 before real-data AI or any write tool is enabled.
4. Sagar and operations resolve Q09/Q11/Q14; Q15 approves only the relevant schema increment after its dependencies settle.

Decision work may proceed in parallel. A closed question does not mark an implementation feature complete: its contract, security, integration, recovery and acceptance tests must still pass.
