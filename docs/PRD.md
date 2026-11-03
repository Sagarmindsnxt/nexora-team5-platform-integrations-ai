# Nexora Team 5 Product Requirements Document

## 1. Document control

| Field | Value |
|---|---|
| Purpose | Define Team 5 product behavior, boundaries, verification and implementation gates |
| Status | Draft for review; no stakeholder approval recorded |
| Version | 0.1 |
| Last updated | 2026-10-27, Asia/Calcutta |
| Accountable owner | Sagar, Team 5 lead, per supplied staffing context; adoption of this draft pending |
| Intended reviewers | Project coordinator; Vignesh (technical lead in resource plan); Teams 1-4 leads; Varshini; Sharanbasava; shared QA (identity to confirm) |
| Related documents | [Architecture](architecture.md), [sources and ownership](source-inventory.md), [contracts](api-contracts.md), [schema](database-schema.md), [security](security.md), [plan](implementation-plan.md), [questions](open-questions.md), [ADRs](adr/README.md), [validation](validation-report.md) |
| Approval required | Coordinator resolves scope conflicts; provider/consumer leads accept cross-team contracts; Sagar and technical lead review architecture/security; QA reviews acceptance coverage. These are proposed review gates, not approvals already received. |

### 1.1 Evidence and status rules

**CONFIRMED** means explicitly supported by an available source, not implemented, tested, funded, or approved for release. **PROPOSED** means recommended design or behavior awaiting agreement. **OPEN DECISION** means a choice whose owner must resolve it. **ASSUMPTION** means a temporary planning premise, with consequences in section 12. The current coordinator boundaries in the user's request outrank older specifications. Conflicts remain visible in the source inventory and question register.

Requirement cards separate the confirmed capability from its proposed operational contract. Unless directly attributed to a source, preconditions, validation/error details, acceptance scenarios, test designs and rollout gates are **PROPOSED operationalizations**. A CONFIRMED card does not silently approve those details. No application is present in this workspace, and no API availability or database deployment has been verified.

### 1.2 Source key

Page numbers below are PDF page numbers (matching printed page numbers). PNG citations use named panels. Full inventory and review limitations are in [source-inventory.md](source-inventory.md).

| Key | Filename / source |
|---|---|
| S00 | Current user request: coordinator ownership boundaries, staffing and approximately two hours/person/day |
| S01 | Nexora_Product_Solution_Overview.pdf |
| S02 | Nexora_Team1_HRMS_Organization_Spec.pdf |
| S03 | Nexora_Team2_Task_Project_Management_Spec.pdf |
| S04 | Nexora_Team3_Engineering_Productivity_Change_Intelligence_Spec.pdf |
| S05 | Nexora_Team4_Incident_RCA_Spec.pdf |
| S06 | Nexora_Team5_Platform_Integrations_AI_Spec.pdf |
| S07 | Detailed HRMS Organization ERD Schema.png |
| S08 | Nexora_Resource_Plan.png |
| S09 | Team 2 Project Management ER Diagram.png |
| S10 | Team 3 Engineering ERD Diagram.png |
| S11 | Team 4 Incident Management ERD.png |
| S12 | Team 5 Platform ERD Blueprint.png |

## 2. Executive summary

Nexora connects organizational ownership, project intent, engineering changes and production incidents so users can understand what changed, what was affected, and how remediation was validated. Team 5 supplies the shared technical foundation: integration infrastructure, AI access, governed tool execution, audit, events and operational visibility. Teams 1-4 retain their domain systems of record and business decisions. [S01 pp3-9, 15-18, 20; S06 pp3, 19-23]

Under the coordinator's current direction, Team 1 owns authentication, users, organizations and RBAC. Team 5 integrates with those services and enforces their decisions in platform operations. It does not implement a second identity system. This differs materially from S06 pp5-6 and the older expectations in the other team specifications; Q01 records the required handoff.

The proposed delivery strategy is a small modular backend using the source-specified FastAPI and PostgreSQL foundation, with durable integration work and an explicitly authorized AI execution path. First prove the access, integration and AI chains in S06 p22. Provider choices, schemas, service authentication, approval semantics, operating targets and release scope remain gated decisions.

## 3. Problem statement and objectives

### 3.1 Problem and value

People, work, Git changes, deployments, telemetry and incident evidence are fragmented. Independent connectors and model clients would multiply credentials, failure handling, costs and inconsistent authorization. Unrestricted AI operations would turn incomplete evidence into unsafe actions. Team 5 provides reusable capabilities while keeping business meaning with domain teams. [S01 pp5-6; S06 pp9, 11-14, 20]

### 3.2 Objectives and success criteria

| Objective | Observable success criterion | Evidence / status |
|---|---|---|
| Shared access | A Team 1 authenticated principal reaches only authorized organization resources; an unauthorized principal and its AI agent are denied identically | Confirmed boundary and least privilege: S00, S06 pp6-7,20; exact test matrix proposed |
| Reusable integration | A GitHub delivery reaches a Team 3 canonical record through an agreed contract, with replay not duplicating the record | Source chain confirmed S06 pp9-10,22; replay semantics proposed |
| Governed AI | A domain agent uses the gateway and registered tools; denied actions cause no tool side effect and remain auditable | S01 p15; S06 pp12-14,20,22 |
| Traceability | Every selected acceptance scenario links request, integration/AI execution and audit outcome by identifiers | Correlation/audit confirmed S06 pp5,8; precise envelope proposed |
| Metering | An authorized organization consumer can reconcile request attempts, known token counts and estimated cost, with unknown charges explicitly marked | S06 pp11,15; reconciliation mechanics proposed |
| Parallel delivery | Teams can review contract examples and use clearly marked fixtures before live providers exist | S06 p18; fixture process proposed |

No source provides adoption, revenue, incident-time reduction, latency, throughput, availability or cost-saving baselines or targets. Q09 and Q13 must set relevant baselines and release criteria. Do not claim business improvement from successful unit tests alone.

## 4. Users, actors and permissions

These are workflow personas, not new RBAC role definitions. Permission names in examples require Team 1 agreement (CT-01).

| Actor | Responsibility and permitted operations | Authorization dependency | Workflow |
|---|---|---|---|
| Organization integration administrator | Connect, inspect, sync and disconnect approved integrations in their organization | Team 1 identity, membership and integration permission; provider grant scopes | W02 |
| Developer / engineering reviewer | Read authorized engineering context; request analysis; review proposed changes | Team 1 permission plus Team 3 resource access | W03-W04 |
| Incident investigator / reviewer | Request RCA context; review findings and remediation proposals | Team 1 identity; Team 4 incident/evidence access and approval workflow | W03-W04 |
| Audit reviewer | Query permitted audit events without access to credentials or unrelated tenants | Team 1 audit-read permission and field visibility | W05 |
| Platform operator | Diagnose failures, rotate credential references, reconcile jobs under explicit grants | Separate operational permissions from tenant admin; no implicit all-tenant access | W02, W05 |
| Team 1-4 service | Submit audit/events and consume integrations or AI infrastructure | Authenticated workload identity plus tenant and delegated subject when acting for a user | W01-W03 |
| Connector worker | Fetch and deliver provider data for an enabled connection | Scoped service authority tied to validated connection tenant; current credential and status | W02 |
| AI agent | Assemble allowed context and request registered tool calls | Effective authority is intersection of delegated user, service, agent, tool and resource grants; model output confers none | W03-W04 |
| External provider / webhook sender | Deliver a provider event, not assert Nexora user permissions | Provider-specific verification and installation-to-organization binding | W02 |
| QA / domain evaluator | Execute synthetic tests and approved evaluation datasets | Test-environment privileges and dataset access; production data requires a separate grant | W06 |

## 5. Scope and ownership

### 5.1 Team 5 scope

Source-supported capabilities are platform configuration and API standards; access enforcement using the current owning identity system; tenant context; audit/security events; shared connector lifecycle; GitHub; project-tool and observability integrations; AI gateway; tool and agent infrastructure; policies; usage/cost visibility; evaluation infrastructure; common events/notifications. A capability being in scope does not establish that every named provider or future operation belongs in the first release. [S06 pp4-15,23]

| Area / entities | System of record and owner | Team 5 boundary | Consumers / unresolved question |
|---|---|---|---|
| Organization, department, team, employee, user, credentials, sessions, roles, permissions | Team 1, S00; HR entities S02/S07 | Validate context, retain logical identifiers; no credentials/session/user tables | All teams; Q01-Q02 identity and permission contract |
| Workspace (ERD-only proposal), project, epic, task, sprint and collaboration | Team 2, S00/S03/S09 | External ID mapping and transport only; no competing project/task CRUD | Teams 3-5; canonical import and membership semantics Q04/Q16 |
| Organizational employee/team-to-project allocations | Team 1, S02 pp10-11 | May consume an agreed reference only; never infer resource permission from allocation | Team 2-5; distinguish planning allocation from Team 2 project membership under Q16 |
| Repository, branch, commit, PR, changed files, builds, deployments, engineering metrics and analysis | Team 3, S00/S04 pp6,15,20 | Provider retrieval and technical normalization to Team 3-approved contracts; store delivery state | Teams 2/4/5; Q04 mapping; Q05 graph references |
| Incident, evidence, RCA, candidates, remediation, validation and human review | Team 4, S00/S05 pp5-15/S11 | Transport telemetry, provide AI/runtime/audit; Team 4 owns incident and evidence meaning/normalization | Teams 3/5; Q08 approval evidence |
| Service identity / catalog | OPEN DECISION; S12 proposes service, S04/S05 reference it | No new canonical service catalog without Q05 decision | Teams 3-5 |
| Connection, credential reference, sync checkpoint, external mapping | Team 5 infrastructure; schema proposed | Own lifecycle, not provider or domain truth | Teams 2-4; CT-02/03/04 |
| AI registry, executions, policies, usage, evaluation framework | Team 5 infrastructure; domain prompts and correctness owned by Teams 3/4 | Enforce runtime boundaries and expose evidence of execution | Q07-Q08/Q12 |
| Audit transport, platform events, operational instrumentation | Team 5; business facts authored by domain owners | Preserve provenance; domain histories remain with owners | All teams; Q10-Q11 |

See the complete ownership matrix in [source-inventory.md](source-inventory.md). No service name or endpoint in this matrix asserts a deployed service exists.

### 5.2 Exclusions and phased scope

Team 5 excludes HRMS business logic, user/role administration, native project/task management, engineering analytics/change-risk logic, incident/evidence interpretation, RCA conclusions, remediation approval authority and domain dashboards. Direct cross-team database reads/writes, duplicated canonical entities, arbitrary AI shell/code execution, autonomous production deployment, automatic merges and a new graph/vector database are not approved by these sources.

**PROPOSED first slice:** foundation, delegated identity, tenant enforcement, durable audit, connector framework, one agreed GitHub read flow into Team 3, one approved AI provider/model, read-only registered tools and a bounded advisory agent. Minimum policy, tool authorization, redaction and usage instrumentation accompany the first AI call; they cannot be postponed until an unsafe execution path already ships.

**PROPOSED later slices:** selected Jira/Linear/Azure DevOps integrations, selected observability adapters, metering reports, offline evaluation and notification channels; assisted write tools only after Q08 and domain approval integration. Level 3 automation is not a release commitment. S06 pp4,17,21 provide priorities and cycles, but not a dated schedule. Its scope sentence says ten P0/six P1 while its table lists eleven P0/five P1; Q13 resolves the discrepancy.

## 6. Functional requirements

Priority P0/P1 on FR-PLAT cards comes from the S06 p4 row, not the inconsistent total. For 002/003 it describes urgency of the revised integration responsibility, not authority to implement Team 1's system. Additional security/reliability requirements have proposed priorities. Each card defines one acceptance bundle AC-* and test bundle TC-*; individual cases use `.a`, `.b`, etc. IDs do not change when a task is split.

All platform operations inherit these proposed cross-cutting rules: validate schema before side effects; establish tenant and subject from trusted contracts; authorize resources before use; return a sanitized error with request ID; never turn a timeout into authorization success; never log a credential or raw sensitive payload. Actor, validation and failure fields below specialize these rules.

### FR-PLAT-001 - Platform foundation

**Requirement ID:** FR-PLAT-001

**Requirement name:** Platform foundation

**Description:** Provide shared configuration, environment handling, database access foundations, API/error/logging conventions and health/version endpoints.

**Rationale:** Reduce inconsistent service behavior and make deployment failures diagnosable.

**Actor:** Domain developer; platform operator; health probe.

**Preconditions:** Repository layout and environment contract accepted (Q03/Q14); valid runtime configuration.

**Trigger:** Service startup or API/health request.

**Expected behavior:** Validate required configuration before readiness. Expose source-specified GET /health, /ready and /version. Proposed semantics: liveness reports process health; readiness reports mandatory local dependencies and compatible schema; version exposes release identifier without secret configuration. Propagate generated request/correlation IDs and a common error envelope.

**Inputs:** Environment values, secret references, release metadata and request headers.

**Outputs:** Validated config; health/readiness/version response; sanitized log/error with correlation.

**Validation rules:** Reject invalid or missing mandatory config; validate externally supplied IDs before reuse; never dump environment values.

**Authorization requirements:** Public probe payloads reveal minimal state; detailed diagnostics require operational authority, subject to Q14.

**Error scenarios:** Missing secret, inaccessible database or incompatible migration => not ready; unexpected exception => sanitized internal error.

**Dependencies:** M01; Q03/Q09/Q14; FR-OPS-001.

**Priority:** P0 (source row)

**Acceptance criteria:** AC-PLAT-001.a: valid configuration starts and all three endpoints follow the agreed schema. .b: missing config or mandatory DB failure prevents readiness. .c: an induced exception yields the same request ID in safe response and log, with no secret.

**Verification method:** TC-PLAT-001: configuration matrix, API contract checks and DB fault injection; inspect response/log canaries.

**Source reference:** S06 p5 §03; S01 p18 §15.

**Status:** CONFIRMED

### FR-PLAT-002 - Delegate authentication to Team 1

**Requirement ID:** FR-PLAT-002

**Requirement name:** Delegate authentication to Team 1

**Description:** Consume the owning authentication system; Team 5 does not issue identities, passwords, sessions or refresh tokens.

**Rationale:** Preserve the coordinator boundary and one authentication authority despite older Team 5 auth ownership text.

**Actor:** User; domain service; background worker.

**Preconditions:** CT-01 issuer, token/session validation, workload identity and revocation behavior agreed; Q01 resolved.

**Trigger:** Protected platform request or resumed background execution.

**Expected behavior:** Establish validated subject and actor type using Team 1-approved verification. Reject absent, invalid, expired or revoked identity. Distinguish invalid authentication from unavailable verification. Do not implement the older source login/logout/refresh paths without an explicit routing/handoff decision.

**Inputs:** Bearer/session credential or authenticated service identity; trusted validation configuration.

**Outputs:** Immutable validated principal context or sanitized authentication/unavailability error.

**Validation rules:** Validate issuer, audience, signature/verification result, validity and revocation using the selected protocol; token format is not assumed.

**Authorization requirements:** No authenticated identity implies no tenant or resource authority. Service identity is not permission to impersonate a user.

**Error scenarios:** Invalid credential => authentication failure; validation dependency unavailable => deny with unavailable status; no fallback to decoded/unverified claims.

**Dependencies:** CT-01; Q01/Q02; Team 1 availability and policy.

**Priority:** P0 (source urgency, ownership revised)

**Acceptance criteria:** AC-PLAT-002.a: valid Team 1 credential produces the agreed context. .b: expired, forged, wrong-audience and revoked credentials never reach business logic. .c: unavailable validation cannot grant access; no Team 5 credential/session store exists.

**Verification method:** TC-PLAT-002: Team 1 contract fixtures and live integration; inspect storage/routes for competing identity behavior.

**Source reference:** S00 coordinator boundary; conflicting S06 pp5,16,18; S02 p14.

**Status:** CONFIRMED

### FR-PLAT-003 - Enforce delegated authorization

**Requirement ID:** FR-PLAT-003

**Requirement name:** Enforce delegated authorization

**Description:** Apply a single Team 1-owned permission model, resource constraints and least privilege to platform APIs, services and AI tools.

**Rationale:** A model or background process must not bypass the permissions of the principal it represents.

**Actor:** Validated human/service/agent principal.

**Preconditions:** CT-01 permission vocabulary and domain resource authorization contracts accepted.

**Trigger:** Access to a protected resource or operation.

**Expected behavior:** Obtain current permission decision for action, resource and organization. Combine it with domain resource access and platform policy; deny unless all required checks allow. Recheck before queued or assisted side effects. No local role membership authority.

**Inputs:** Validated subject, actor type, action, resource type/ID, organization and delegation.

**Outputs:** Allow/deny decision metadata and permitted result or error.

**Validation rules:** Reject unknown actions, mismatched resource tenant and missing delegation; bound any decision cache by agreed revocation semantics.

**Authorization requirements:** Effective agent access cannot exceed user, service, agent and tool grants; management permission does not automatically imply domain-data access.

**Error scenarios:** Deny => forbidden or non-disclosing not-found per agreed API rule; policy service failure => unavailable and no side effect.

**Dependencies:** CT-01 plus CT-02/03/04 for owner checks; Q01/Q02/Q08.

**Priority:** P0 (source row)

**Acceptance criteria:** AC-PLAT-003.a: allow and deny fixtures produce expected results. .b: the same inaccessible resource is denied to a user and its agent. .c: permission revoked after enqueue prevents execution. .d: denial creates safe security audit metadata.

**Verification method:** TC-PLAT-003: permission matrix, delegated-agent parity and revocation race tests.

**Source reference:** S00; S06 pp6,12,20; S01 p15.

**Status:** CONFIRMED

### FR-PLAT-004 - Validate tenant context

**Requirement ID:** FR-PLAT-004

**Requirement name:** Validate tenant context

**Description:** Establish and enforce organization context on every relevant request and stored platform record.

**Rationale:** Prevent cross-organization data disclosure or mutation while retaining Team 1 organizational ownership.

**Actor:** All authenticated platform actors and connector workers.

**Preconditions:** Organization membership/status and resource-to-tenant contract agreed (Q02).

**Trigger:** Request ingress, job claim, lookup, event ingestion or provider callback.

**Expected behavior:** Bind the tenant to validated membership or scoped service/connection authority. Scope queries, uniqueness keys, caches, jobs, exports and audit access. Revalidate foreign resources through their owner. A webhook uses a trusted connection binding, not an arbitrary payload organization field.

**Inputs:** Validated principal and tenant selector; connection binding; resource references.

**Outputs:** Tenant-scoped context and scoped result or denial.

**Validation rules:** Reject missing tenant on tenant-owned data, cross-tenant references and organization status incompatible with the operation; global catalogs must be explicitly designated.

**Authorization requirements:** Team 1 membership and permission plus domain ownership check; no implicit operator superuser.

**Error scenarios:** Unknown/mismatched organization denies access without leaking existence; unresolved owner reference quarantines asynchronous data.

**Dependencies:** CT-01/02/03/04; Q02/Q15; FR-DATA-001.

**Priority:** P0 (source row)

**Acceptance criteria:** AC-PLAT-004.a: tenant A cannot read/write/list/export/replay tenant B data. .b: worker and webhook paths obey the same tenant rule. .c: reused external IDs in different organizations remain separate. .d: no Team 5 organization business table.

**Verification method:** TC-PLAT-004: two-tenant API, persistence, cache, worker and webhook negative suite.

**Source reference:** S00; S06 p7 §06; S12 panel1 is proposed and conflicts with ownership.

**Status:** CONFIRMED

### FR-PLAT-005 - Central audit and security events

**Requirement ID:** FR-PLAT-005

**Requirement name:** Central audit and security events

**Description:** Provide an audit capability consumable by all teams with actor, organization, action, resource, metadata and timestamp.

**Rationale:** Explain access decisions, connector changes and AI operations across services.

**Actor:** Authenticated event-producing service; authorized auditor.

**Preconditions:** CT-06 event schema, producer trust and retention policy agreed.

**Trigger:** Sensitive action, security decision, integration change or audit query.

**Expected behavior:** Accept validated producer events, retain provenance and correlate requests. Proposed: append-only writes, deduplicate by producer/tenant/event ID, bound/redact metadata and enforce tenant-filtered query. Producers retain responsibility for business facts. Critical local mutations couple audit intent to the same transaction.

**Inputs:** Event identity, producer, tenant, subject/actor, action, resource reference, outcome, UTC time, request/correlation IDs and allowlisted metadata.

**Outputs:** Durable acknowledgment or explicit failure; authorized paginated audit result.

**Validation rules:** Reject missing identity, invalid event version, unauthorized tenant/type and sensitive payload fields; preserve occurred and received times separately.

**Authorization requirements:** Producer service grant for ingestion; Team 1 audit.read-equivalent for query; no ordinary update/delete API.

**Error scenarios:** DB outage prevents durable acceptance; replay returns existing acknowledgment; failed noncritical exporter does not erase committed audit.

**Dependencies:** CT-01/06; Q10/Q11; FR-REL-001.

**Priority:** P0 (source row)

**Acceptance criteria:** AC-PLAT-005.a: one protected action can be traced through its audit record. .b: duplicate submission does not create duplicate logical event. .c: unauthorized read/update is denied. .d: secret canaries do not appear in stored metadata.

**Verification method:** TC-PLAT-005: producer contract, query authorization, dedupe, audit-write failure and redaction tests.

**Source reference:** S06 p8 §07; S12 panel10.

**Status:** CONFIRMED

### FR-PLAT-006 - Reusable integration framework

**Requirement ID:** FR-PLAT-006

**Requirement name:** Reusable integration framework

**Description:** Define connector authenticate/connect/disconnect/health_check/sync/fetch/handle_webhook interfaces and common lifecycle.

**Rationale:** Share credential handling, status and delivery mechanics while keeping provider-specific behavior explicit.

**Actor:** Integration administrator; connector implementation; worker.

**Preconditions:** Approved adapter registration, secret reference and domain delivery contract.

**Trigger:** Connection create/test/disconnect, sync request, scheduled fetch or callback.

**Expected behavior:** Register allowed adapters; validate config; create tenant connection; report health; schedule and record jobs; deactivate connection and prevent later dispatch on disconnect. Each interface reports supported, unsupported, success or categorized failure; the common interface does not imply every provider has webhooks or bidirectional sync.

**Inputs:** Provider key, non-secret config, credential reference, scoped tenant, sync cursor and typed fetch request.

**Outputs:** Connection status, job/delivery identity, capability declaration and categorized outcome.

**Validation rules:** Allowlist provider types and config fields; validate connection ownership; never accept arbitrary import paths or network endpoints from an AI response.

**Authorization requirements:** Connection management/sync permissions plus service authority for worker; retrieve only scoped credentials.

**Error scenarios:** Unsupported operation => explicit unsupported; expired grant => action-required; provider limit => deferred; invalid config => validation error.

**Dependencies:** CT-01/05; Q04/Q06; FR-SEC-001/002; FR-REL-001.

**Priority:** P0 (source row)

**Acceptance criteria:** AC-PLAT-006.a: fake and first real adapter share the same lifecycle contract. .b: unsupported webhook capability is explicit. .c: disconnect after enqueue stops dispatch. .d: job history distinguishes provider and consumer failure.

**Verification method:** TC-PLAT-006: adapter conformance suite and disconnect/rate-limit/config fault tests.

**Source reference:** S06 p9 §08 and p16 integration API list.

**Status:** CONFIRMED

### FR-PLAT-007 - GitHub engineering integration

**Requirement ID:** FR-PLAT-007

**Requirement name:** GitHub engineering integration

**Description:** Retrieve repositories, branches, commits, PRs, diffs, changed files, build/workflow data and deployments where available; support webhooks and authorized read tools.

**Rationale:** Give Team 3 normalized provider data and Team 4 approved change/deployment context.

**Actor:** Connection administrator; GitHub; worker; authorized domain agent.

**Preconditions:** Selected GitHub authorization mode and scopes; verified installation binding; CT-03 ingest/read semantics accepted.

**Trigger:** Accepted webhook, sync request or permitted read-tool request.

**Expected behavior:** Map provider records to Team 3-approved canonical envelopes; use stable provider IDs scoped to connection; preserve source timestamp/version and provenance; deliver to Team 3. Missing deployment/build data is unavailable, not fabricated. Team 5 stores mappings and synchronization state, not canonical repositories/PRs.

**Inputs:** Verified webhook or cursor; GitHub identifiers; permitted repository context.

**Outputs:** Canonical ingest envelope, owner acknowledgment and scoped external-ID mapping; tool result with provenance.

**Validation rules:** Check provider account/repository access, event type/version and mapping tenant; reject unsupported/malformed delivery and quarantine ambiguous mapping.

**Authorization requirements:** GitHub installation/token scope and Team 1/domain permissions must both permit the operation.

**Error scenarios:** Provider revocation pauses; unknown repository mapping quarantines; pagination timeout retries safely; downstream conflict does not advance checkpoint.

**Dependencies:** CT-03; Q04/Q06; FR-PLAT-006; FR-SEC-002; FR-REL-001.

**Priority:** P0 (source row)

**Acceptance criteria:** AC-PLAT-007.a: fixtures cover each listed record kind, including unavailable deployment data. .b: verified PR delivery is accepted by Team 3. .c: replay/rename/out-of-order fixtures do not duplicate canonical entities. .d: unauthorized repository tool access fails.

**Verification method:** TC-PLAT-007: GitHub adapter fixtures, signature tests, pagination/replay and Team 3 consumer-contract integration.

**Source reference:** S06 p10 §09; S04 pp6,15,20; S12 panel3 is not canonical ownership approval.

**Status:** CONFIRMED

### FR-PLAT-008 - Project management integration

**Requirement ID:** FR-PLAT-008

**Requirement name:** Project management integration

**Description:** Support integration with project tools, with Jira, Linear and Azure DevOps named initial targets; complement Team 2 native work management.

**Rationale:** Link external work intent to engineering without a separate Team 5 task system.

**Actor:** Work integration administrator; worker; Team 2 consumer.

**Preconditions:** Provider subset, import direction, conflict/deletion rules and CT-02 mapping accepted.

**Trigger:** Approved provider sync or event.

**Expected behavior:** Retrieve permitted external work data, attach provenance, map external identity and deliver to Team 2. Team 2 owns canonical project/task semantics and changes. Proposed first direction is inbound; no automatic write-back until separately approved.

**Inputs:** External project/work-item IDs and fields, provider revision, connection and tenant.

**Outputs:** Team 2-approved work envelope; mapping to Team 2 canonical ID; sync outcome.

**Validation rules:** Validate supported field mapping; distinguish unknown user from a resolved employee; do not map people by email without explicit agreement.

**Authorization requirements:** Connection management plus source read scope; Team 2 resource and ingest authorization.

**Error scenarios:** Conflicting revision, unresolved identity or missing parent => quarantine/explicit partial result; never overwrite native task silently.

**Dependencies:** CT-02; Q02/Q04/Q06/Q13; connector framework.

**Priority:** P1 (source row)

**Acceptance criteria:** AC-PLAT-008.a: selected provider fixture creates/updates only through Team 2 contract. .b: conflict and deleted-source fixtures follow agreed rules. .c: no Team 5 core project/task table or write-back side effect.

**Verification method:** TC-PLAT-008: provider mapping, revision conflict, person-mapping and Team 2 contract tests.

**Source reference:** S06 p10 §09; S03; S12 panel4 proposes external projections only.

**Status:** CONFIRMED

### FR-PLAT-009 - Observability integration

**Requirement ID:** FR-PLAT-009

**Requirement name:** Observability integration

**Description:** Provide selected observability/incident connector capabilities; Sentry, Datadog, PagerDuty, Prometheus and OpenTelemetry are potential sources.

**Rationale:** Make authorized runtime information available for Team 4 investigation.

**Actor:** Incident investigator; telemetry provider; worker.

**Preconditions:** Provider and telemetry kinds selected; service identity boundary Q05 and CT-04 accepted.

**Trigger:** Provider event, bounded telemetry query or authorized collection job.

**Expected behavior:** Fetch bounded time/resource-scoped telemetry, retain provenance and deliver to Team 4. Team 4 interprets and normalizes incidents/evidence. Provider-specific capabilities differ: metrics scraping/querying, traces and incident callbacks are not a single mandatory connector behavior.

**Inputs:** Connection, service/resource references, time range, query type and tenant.

**Outputs:** Telemetry transport envelope or allowed result with source/time/completeness; domain acknowledgment.

**Validation rules:** Validate query scope and time range; sanitize content; cap result volume by accepted limits; unknown service mapping is explicit.

**Authorization requirements:** User/service resource permission and provider scope; no unrestricted telemetry query language exposed to models.

**Error scenarios:** Partial source availability returns explicit partial status; no-data differs from failure; provider outage retains retryable job.

**Dependencies:** CT-04; Q05/Q06/Q10/Q13; FR-PLAT-006.

**Priority:** P1 (source row)

**Acceptance criteria:** AC-PLAT-009.a: chosen source produces a Team 4-consumable envelope. .b: denied service/time scope is not queried. .c: partial, empty and failed responses are distinct. .d: Team 5 does not create incident/evidence records independently.

**Verification method:** TC-PLAT-009: bounded-query fixtures, leakage tests and Team 4 incident/evidence ingestion contract.

**Source reference:** S06 p10 §09; S05 p6 §04; S12 panel5 unresolved catalog ownership.

**Status:** CONFIRMED

### FR-PLAT-010 - Provider-agnostic AI gateway

**Requirement ID:** FR-PLAT-010

**Requirement name:** Provider-agnostic AI gateway

**Description:** Provide central model selection, provider routing/authentication, request/response handling, retry/timeout controls, policy, logging and usage/cost hooks.

**Rationale:** Avoid independent domain provider clients with inconsistent governance and accounting.

**Actor:** Authorized domain service or agent.

**Preconditions:** Approved provider/model allowlist, credential reference, data-transfer policy, timeout and budget settings.

**Trigger:** Validated AI chat or execution model step.

**Expected behavior:** Authorize requested model/capability and tenant; apply policy; record attempt before dispatch; enforce limits; invoke selected provider; validate normalized response; record safe usage and outcome. Proposed retry only when permitted and safe; unknown billable outcome is visible. Fallback requires explicit approved route and data policy.

**Inputs:** Subject/tenant, model alias, prompt/context or safe reference, generation parameters and idempotency key where accepted.

**Outputs:** Normalized result, request/attempt IDs, provider/model version, finish state, usage quality and error category.

**Validation rules:** Reject unknown/disabled model, invalid parameters, excessive context and forbidden data/provider combination; do not persist raw prompt by default.

**Authorization requirements:** CT-01 delegated identity, domain resource access and model policy; provider secret never returned.

**Error scenarios:** Rate limit => retryable or deferred; timeout => failed/unknown attempt as appropriate; malformed result => validation failure; no model selected => configuration error.

**Dependencies:** CT-07; Q06/Q07/Q09/Q10; policy, metering, secret lifecycle.

**Priority:** P0 (source row)

**Acceptance criteria:** AC-PLAT-010.a: fake providers normalize to one contract. .b: disabled model and denied tenant never cause provider call. .c: timeout/retry attempts remain separately metered. .d: provider text cannot invoke a tool directly.

**Verification method:** TC-PLAT-010: provider adapter contract, dispatch-denial, output validation, timeout and ambiguous-billing tests.

**Source reference:** S06 p11 §10; S01 p18.

**Status:** CONFIRMED

### FR-PLAT-011 - Versioned tool and agent registry

**Requirement ID:** FR-PLAT-011

**Requirement name:** Versioned tool and agent registry

**Description:** Register controlled tools with name, description, input/output schemas, permission, risk and audit requirements; bind agents to allowed tools.

**Rationale:** Make capabilities reviewable and remove unrestricted model access.

**Actor:** Authorized registry maintainer; executor; domain agent author.

**Preconditions:** Permission vocabulary and reviewed executable adapters; registry administration policy accepted.

**Trigger:** Tool/agent registration, version publication, lookup or execution resolution.

**Expected behavior:** Validate complete metadata; associate a server-owned adapter and explicit version; expose only permitted tools; disable/revoke versions without granting an agent extra authority. The S12 agent/agent_tool design is a proposal for representing these relationships, not a finalized schema.

**Inputs:** Tool/agent name/version, schemas, required action, risk, audit flag, allowed bindings and implementation key.

**Outputs:** Versioned registry entry and permitted manifest; rejection report.

**Validation rules:** Reject duplicate version with changed content, missing schemas, unknown permission or arbitrary executable path; require approved schema dialect.

**Authorization requirements:** Separate registry management and execution permission; agent_tool binding restricts capability but never grants user access.

**Error scenarios:** Unknown/disabled version => no execution; incompatible schema => registration failure; revoked version stops pending dispatch.

**Dependencies:** CT-01/07; Q08/Q15; FR-PLAT-013.

**Priority:** P0 (source row)

**Acceptance criteria:** AC-PLAT-011.a: missing metadata is rejected. .b: tool version resolves to reviewed adapter. .c: denied/disabled tools are unavailable for execution. .d: registry changes emit audit and cannot alter an already recorded version.

**Verification method:** TC-PLAT-011: registry validation, version immutability, permission filtering and revocation tests.

**Source reference:** S06 p12 §11; S01 p15 §12; S12 panel7.

**Status:** CONFIRMED

### FR-PLAT-012 - Bounded agent execution and context

**Requirement ID:** FR-PLAT-012

**Requirement name:** Bounded agent execution and context

**Description:** Provide common agent lifecycle and context mechanisms; Teams 3 and 4 retain domain planning, prompts and interpretation.

**Rationale:** Reuse safe execution infrastructure without centralizing domain intelligence in Team 5.

**Actor:** Authorized user/domain service; registered agent; worker.

**Preconditions:** Approved agent/tool/model/policy versions and domain context contracts.

**Trigger:** AI execution request or continuation after an allowed pause.

**Expected behavior:** Create execution bound to tenant and initiating authority; retrieve only authorized context through tools; record source references and missing inputs; run bounded model/tool steps; validate all proposals; complete, fail, cancel or pause for approval explicitly. Resume rechecks authority and version/policy validity.

**Inputs:** Agent/version, domain resource references, purpose, requested limits and delegated context.

**Outputs:** Execution ID/status, permitted result references, steps/tool outcomes and usage correlation.

**Validation rules:** Bound iterations, wall time, context size and concurrency by approved configuration; reject unknown agent or stale/mismatched continuation.

**Authorization requirements:** Per-step Team 1 and resource-owner checks; no service-level bypass of user permissions.

**Error scenarios:** Context unavailable => explicit partial/blocked result; tool failure => typed step failure; cancellation prevents new calls but cannot undo external completed side effects.

**Dependencies:** CT-02/03/04/07; Q07/Q08/Q09; gateway, registry and policy.

**Priority:** P0 (source row)

**Acceptance criteria:** AC-PLAT-012.a: an advisory agent consumes permitted context and returns result with provenance. .b: loop/time limit stops new dispatch. .c: cancellation or revocation stops later steps. .d: failed tool output is not presented as successful evidence.

**Verification method:** TC-PLAT-012: deterministic agent fixtures, partial context, loop limit, restart, cancellation and revocation tests.

**Source reference:** S06 p13 §12; S01 pp13-15.

**Status:** CONFIRMED

### FR-PLAT-013 - AI policy and human approval enforcement

**Requirement ID:** FR-PLAT-013

**Requirement name:** AI policy and human approval enforcement

**Description:** Enforce advisory, assisted and explicitly controlled automation boundaries; assisted actions require human review and production change is restricted.

**Rationale:** Keep executable action under human and organizational authority.

**Actor:** Agent executor; policy maintainer; human reviewer through Team 4.

**Preconditions:** Policy precedence, risk classification and approval semantics accepted (Q08).

**Trigger:** AI/model request, proposed tool call or approved-action continuation.

**Expected behavior:** Evaluate policy before dispatch. Proposed default is advisory read-only. Deny unregistered/forbidden operations; require current resource permission and bound human approval for configured assisted actions. Team 4 owns remediation approval record; Team 5 verifies proof and enforces it. No automatic merge/deploy default.

**Inputs:** Actor/resource context, tool and argument digest, model route, policy version and trusted approval reference if required.

**Outputs:** Allow, deny or approval-required decision with reason and audit metadata.

**Validation rules:** Reject ambiguous policy, changed arguments, mismatched tenant/tool/resource, expired/revoked approval and model-generated approval claims.

**Authorization requirements:** Policy is an additional restriction, not a replacement for Team 1/domain permission. Reviewer authority must be validated.

**Error scenarios:** Policy/approval service unavailable => fail closed; denied decision has no external effect; unknown completed action requires reconciliation.

**Dependencies:** CT-01/04/07; Q08/Q13; FR-SEC-003.

**Priority:** P0 (source row)

**Acceptance criteria:** AC-PLAT-013.a: advisory request cannot call write tool. .b: changed arguments or wrong-tenant approval fails. .c: approved operation still fails if current permission is revoked. .d: every decision is auditable; production deploy is unavailable absent explicit policy and approval.

**Verification method:** TC-PLAT-013: policy matrix, approval-binding and time-of-check/time-of-use tests with Team 4 fixtures.

**Source reference:** S06 pp14,20,23; S01 pp14-15; S05 pp12,14.

**Status:** CONFIRMED

### FR-PLAT-014 - AI usage and estimated cost tracking

**Requirement ID:** FR-PLAT-014

**Requirement name:** AI usage and estimated cost tracking

**Description:** Track organization, user, agent, model/provider, tokens, request count, response time, estimated cost and timestamp.

**Rationale:** Explain consumption and make provider charges and retries observable.

**Actor:** Gateway; authorized usage reader; operator.

**Preconditions:** Provider usage normalization and model pricing source/units/currency agreed (Q07).

**Trigger:** Provider dispatch/outcome, reconciliation or usage query.

**Expected behavior:** Record per-attempt usage with logical request correlation. Keep input/output counts distinct and mark reported, estimated or unknown. Calculate decimal cost from effective pricing snapshot; absence of price is unknown, not zero. Summaries remain rebuildable from ledger. Hard budget enforcement is proposed and requires atomic reservation/reconciliation policy.

**Inputs:** Provider attempt IDs, tenant/subject/agent, timestamps/latency, token categories and applicable price version.

**Outputs:** Usage ledger and authorized time-window summary with currency and completeness.

**Validation rules:** Nonnegative known quantities; missing counts remain null/unknown; no double count on repeated completion; do not combine currencies as one sum.

**Authorization requirements:** Organization usage permission; per-user/agent visibility determined by Team 1 policy; producer is trusted gateway only.

**Error scenarios:** Unpriced model => cost unknown; ambiguous timeout => pending reconciliation; reporting outage does not erase dispatch record.

**Dependencies:** CT-07; Q07/Q10; gateway and durable audit/storage.

**Priority:** P1 reporting (source); minimal dispatch metering accompanies P0 gateway as proposed safety dependency

**Acceptance criteria:** AC-PLAT-014.a: repeated completion counts once. .b: two provider attempts are distinguishable from one logical request. .c: missing usage/pricing is never reported as zero. .d: recomputed summary agrees with ledger and price versions.

**Verification method:** TC-PLAT-014: decimal pricing, effective dates, retry accounting, duplicate receipt and reconciliation tests.

**Source reference:** S06 pp11,15 §14; S12 panels6,9.

**Status:** CONFIRMED

### FR-PLAT-015 - Evaluation infrastructure

**Requirement ID:** FR-PLAT-015

**Requirement name:** Evaluation infrastructure

**Description:** Eventually support prompt/model version, input, expected/actual result, score, latency and cost for AI evaluation.

**Rationale:** Make domain quality changes assessable, especially RCA grounding and change intelligence.

**Actor:** Domain evaluator; approved evaluation worker.

**Preconditions:** Q12 dataset/rubric/promotion ownership and Q10 data policy agreed; approved synthetic fixtures can precede real data.

**Trigger:** Versioned evaluation run requested.

**Expected behavior:** Run authorized cases through gateway and policies; preserve dataset/case/prompt/model versions and evaluator identity; report score, failures, latency and usage. Domain teams define expected results/rubrics. No implicit production promotion or correctness claim from an infrastructure score.

**Inputs:** Dataset/case references, approved expected result, prompt/model versions and rubric version.

**Outputs:** Evaluation run/case outcomes with score or explicit unevaluated state, latency and cost completeness.

**Validation rules:** Dataset permission and versions required; incomplete/provider-failed cases are not passes; redact retained input/output.

**Authorization requirements:** Evaluation execution and dataset access grants; use nonproduction resources unless separately approved.

**Error scenarios:** Provider failure or missing expected result => failed/unevaluated case; reproducibility limitations recorded.

**Dependencies:** CT-07; Q10/Q12/Q13; domain teams and gateway.

**Priority:** P1 (source row; eventual capability)

**Acceptance criteria:** AC-PLAT-015.a: fixed synthetic cases produce versioned results. .b: failed case is visible and cannot improve pass count. .c: domain rubric and dataset provenance are retained. .d: no automatic deployment follows a score.

**Verification method:** TC-PLAT-015: deterministic evaluator fixture, invalid dataset permission and partial-run tests.

**Source reference:** S06 p15 §14; S12 evaluation_result lacks full dataset model.

**Status:** CONFIRMED

### FR-PLAT-016 - Common events and notification capability

**Requirement ID:** FR-PLAT-016

**Requirement name:** Common events and notification capability

**Description:** Provide common platform events that domain consumers can subscribe to; notifications are named but channel, recipient and preference behavior are not specified.

**Rationale:** Decouple domain workflows and expose important changes without duplicating business logic.

**Actor:** Domain producer; authorized subscriber; eventual notification recipient.

**Preconditions:** CT-06 event schemas/ownership and Q11 subscription/channel decisions agreed.

**Trigger:** Accepted domain event or due delivery attempt.

**Expected behavior:** Proposed: validate producer/tenant/event version, persist delivery state, deliver at least once and deduplicate logical events. Consumers own business reactions and reauthorize resource access. Notification dispatch remains disabled until channel, recipient eligibility, preference and sensitive-content policy are accepted.

**Inputs:** Versioned event identity, resource reference, producer/tenant, occurrence time and safe payload; subscription reference.

**Outputs:** Durable acknowledgment, subscriber delivery status and, only after approval, notification outcome.

**Validation rules:** Allowed event types and subscriber scope; no arbitrary callback URLs or cross-tenant fanout; no exactly-once promise.

**Authorization requirements:** Authenticated producer and subscribed consumer grants; delivery of a resource ID does not itself authorize retrieval.

**Error scenarios:** Subscriber failure => bounded retry/dead-letter; schema mismatch => quarantine; notification-channel outage never mutates source business record.

**Dependencies:** CT-06; Q10/Q11/Q13; FR-REL-001.

**Priority:** P1 (source row)

**Acceptance criteria:** AC-PLAT-016.a: agreed event is delivered and replay deduplicated by consumer. .b: invalid producer/subscription is denied. .c: failed delivery is visible. .d: unapproved notification channels cannot send.

**Verification method:** TC-PLAT-016: event schema/producer authorization, delivery retry and notification-disabled tests.

**Source reference:** S06 pp8,23; S12 platform_event/event_delivery proposed.

**Status:** CONFIRMED

### FR-SEC-001 - Credential lifecycle and safe egress

**Requirement ID:** FR-SEC-001

**Requirement name:** Credential lifecycle and safe egress

**Description:** Store provider/model credentials as restricted references and enforce connector-specific egress controls.

**Rationale:** Limit credential leakage and server-side request forgery risk introduced by integrations.

**Actor:** Authorized operator; adapter; secret store.

**Preconditions:** Q06 approved secret storage, workload identity, provider hosts and rotation process.

**Trigger:** Connection provisioning, outbound call, rotation or disconnect.

**Expected behavior:** Resolve secret only at dispatch through least-privilege identity; never return it to API/model. Validate approved destination, redirects and resolved addresses. Rotate by staging, verifying, switching reference and retiring old credential; cancellation/disconnect blocks future retrieval.

**Inputs:** Credential reference/version, provider configuration and approved outbound target.

**Outputs:** Authenticated provider call; redacted lifecycle audit; rotation status.

**Validation rules:** Reject plaintext secrets in ordinary config, unapproved URL schemes/hosts, private/metadata targets unless explicitly approved and unsafe redirects.

**Authorization requirements:** Manage-secret privilege separate from ordinary connection read; workload access scoped to needed references.

**Error scenarios:** Secret unavailable => no dispatch; verification fails => retain known active version or disable; never log the failing credential.

**Dependencies:** Q06/Q14; CT-01; connector/gateway runtime.

**Priority:** P0 PROPOSED

**Acceptance criteria:** AC-SEC-001.a: canary secret is absent from API/log/prompt/storage JSON. .b: denied destination cannot be contacted. .c: rotation rollback and disconnected-job checks succeed.

**Verification method:** TC-SEC-001: canary scanning, SSRF target/redirect fixtures, secret permission and rotation-failure rehearsal.

**Source reference:** PROPOSED security elaboration of S06 pp6,9,11,20; S12 credential-bearing config risk.

**Status:** PROPOSED

### FR-SEC-002 - Verified webhook admission

**Requirement ID:** FR-SEC-002

**Requirement name:** Verified webhook admission

**Description:** Verify provider authenticity and tenant binding before accepting webhook data for processing.

**Rationale:** Prevent forged events, cross-tenant injection and duplicate work.

**Actor:** External webhook sender; ingress service.

**Preconditions:** Provider-specific verification and connection binding configured; agreed size and delivery-retention limits.

**Trigger:** Inbound webhook request.

**Expected behavior:** Enforce body limit; preserve raw bytes; authenticate using adapter rule; resolve trusted installation/connection; validate envelope; persist unique delivery receipt before acknowledgment. GitHub verification uses HMAC-SHA256 with constant-time comparison. Signature alone does not prevent replay; use delivery dedupe and provider-state reconciliation.

**Inputs:** Raw bytes, signature/delivery headers and connection route hint.

**Outputs:** Accepted/already accepted receipt or sanitized rejection; no unauthenticated event side effect.

**Validation rules:** Reject missing/invalid signature, wrong installation, unsupported event/version and oversized body. Do not assume GitHub has a signed freshness timestamp.

**Authorization requirements:** Webhook secret authenticates provider, not user permission; worker still checks connection grant and tenant.

**Error scenarios:** Database failure => no successful durable acknowledgment; invalid signature => rejection; duplicate => prior acknowledgment.

**Dependencies:** Q06/Q09/Q10; FR-REL-001; provider-specific contract.

**Priority:** P0 PROPOSED

**Acceptance criteria:** AC-SEC-002.a: valid raw body verifies; one-byte mutation fails. .b: duplicate delivery causes no additional domain action. .c: payload organization cannot override bound tenant. .d: oversized/unverified payload cannot enqueue work.

**Verification method:** TC-SEC-002: signature known-answer fixture, mutation, replay, wrong-installation and storage-failure tests.

**Source reference:** PROPOSED elaboration of S06 pp9-10; technical reference: GitHub validating webhook deliveries (architecture references).

**Status:** PROPOSED

### FR-SEC-003 - Untrusted AI input and executable boundary

**Requirement ID:** FR-SEC-003

**Requirement name:** Untrusted AI input and executable boundary

**Description:** Treat retrieved content and model output as untrusted data that cannot change permissions, policies or executable code.

**Rationale:** Prevent indirect prompt injection, data exfiltration and model-driven privilege escalation.

**Actor:** Gateway; context builder; executor; domain agent.

**Preconditions:** Reviewed tool schemas and code adapters; data classification and output handling policy.

**Trigger:** Context ingestion, model response or tool proposal.

**Expected behavior:** Separate trusted instructions from source content and retain provenance. Validate tool name/version/arguments against registry and current grants outside the model. Allow only reviewed operations and destinations. Escape generated content at consuming UI; retain evidence/inference/unknown labels under domain rules.

**Inputs:** Retrieved code/log/ticket content; model response and proposed tool arguments.

**Outputs:** Validated inert result or authorized typed call; blocked-action audit on unsafe proposal.

**Validation rules:** Reject unknown tools, unauthorized resource selectors, injected URLs/code and malformed outputs. Prompt filters are defense in depth, not authorization.

**Authorization requirements:** Server-side checks always apply even if model claims admin role or approval.

**Error scenarios:** Injection detection may mark content unsafe/partial; schema or permission failure prevents execution; cannot claim perfect detection.

**Dependencies:** FR-PLAT-003/011/012/013; Q08/Q10; domain consumers.

**Priority:** P0 PROPOSED

**Acceptance criteria:** AC-SEC-003.a: malicious source text asking to reveal secrets or call another tenant tool causes no such action. .b: forged approval text fails. .c: malformed/unknown tool calls fail outside the model.

**Verification method:** TC-SEC-003: adversarial corpus across code, logs, tickets and tool output; assert provider/tool call logs contain no prohibited dispatch.

**Source reference:** PROPOSED implementation controls for S01 p15 and S06 pp12,20.

**Status:** PROPOSED

### FR-REL-001 - Durable retries, deduplication and recovery

**Requirement ID:** FR-REL-001

**Requirement name:** Durable retries, deduplication and recovery

**Description:** Use durable job/delivery state with bounded retry, safe idempotency and explicit unknown outcomes.

**Rationale:** Avoid lost acknowledged work and duplicated external/domain side effects.

**Actor:** Worker; consumer; authorized operator.

**Preconditions:** Accepted idempotency scope, attempt budget, retention and consumer acknowledgment semantics.

**Trigger:** Job admission, retryable failure, worker restart or manual replay.

**Expected behavior:** Commit receipt/job before success response; use unique scoped identity; claim with lease/fencing; record attempts; retry eligible failures with backoff and jitter; respect provider Retry-After; stop at accepted budget. Quarantine permanent failures. Reconcile uncertain writes instead of blind retry; advance sync cursor only after accepted delivery.

**Inputs:** Idempotency/event key, payload fingerprint, connection/tenant, checkpoint and failure category.

**Outputs:** Stable job ID, attempt history and terminal/retry/unknown state; audited replay.

**Validation rules:** Same key/different fingerprint => conflict; expired lease cannot overwrite new owner state; no unsupported exactly-once guarantee.

**Authorization requirements:** Recheck connection, tenant and initiating authority at dispatch; replay needs explicit operator grant.

**Error scenarios:** Crash after external effect => unknown pending reconciliation; DB failure => no acknowledge; exhausted retry => failed/dead-letter.

**Dependencies:** CT-02/03/04/06/07; Q04/Q09/Q10/Q14.

**Priority:** P0 PROPOSED

**Acceptance criteria:** AC-REL-001.a: crash before/after receipt, dispatch and acknowledgment loses no acknowledged work. .b: duplicate concurrent claims do not duplicate logical domain action. .c: mismatched idempotency payload conflicts. .d: unknown external effect is not auto-repeated.

**Verification method:** TC-REL-001: crash-point and concurrency tests with idempotent consumer fake; lease-expiry and replay audit checks.

**Source reference:** PROPOSED reliability implementation for S06 pp9-11,22 and S12 sync/event history.

**Status:** PROPOSED

### FR-DATA-001 - Owner references and mapping integrity

**Requirement ID:** FR-DATA-001

**Requirement name:** Owner references and mapping integrity

**Description:** Store Team 5 integration/runtime data and scoped logical references without duplicating another team system of record.

**Rationale:** Reconcile ERD overlap and keep cross-team provenance consistent.

**Actor:** Adapter; platform persistence; domain owner.

**Preconditions:** Q02/Q04/Q15 identifier, ownership and deletion semantics accepted.

**Trigger:** Mapping creation/update, domain acknowledgment, reference resolution or deletion event.

**Expected behavior:** Persist external mapping scoped by tenant, connection/provider account and entity type; use owner-returned canonical ID. Validate referenced tenant through owner contract; retain unresolved status until checked. Domain deletion invalidates use without deleting required audit provenance. Cross-team relationships are logical unless shared physical FK governance is explicitly approved.

**Inputs:** Owner type/ID, external identity, tenant, connection, version and resolution evidence.

**Outputs:** Validated mapping or explicit unresolved/conflict/tombstoned state.

**Validation rules:** Uniqueness includes scope; IDs remain opaque until Q02; user_id is not employee_id; tenant equality enforced on local child-parent relationships.

**Authorization requirements:** Only trusted ingestion/acknowledgment may bind canonical IDs; owner authorizes lookup and change.

**Error scenarios:** Unknown/deleted/moved resource blocks use or quarantines mapping; never synthesize a canonical record to repair it.

**Dependencies:** CT-01/02/03/04; Q02/Q04/Q15.

**Priority:** P0 PROPOSED

**Acceptance criteria:** AC-DATA-001.a: duplicate mappings scoped to different tenants remain distinct. .b: same-scope conflicting mapping is rejected. .c: cross-tenant local relationship and user/employee substitution fail. .d: schema has no competing core domain tables.

**Verification method:** TC-DATA-001: schema/constraint review and two-tenant mapping, deletion and identity fixtures.

**Source reference:** S00 ownership is CONFIRMED; mapping/constraint design PROPOSED from S12 panels1-4 and all team ERDs.

**Status:** PROPOSED

### FR-OPS-001 - Controlled deployment and recovery

**Requirement ID:** FR-OPS-001

**Requirement name:** Controlled deployment and recovery

**Description:** Provide reproducible configuration, reviewed migrations, health checks, rollback/recovery and operational runbooks.

**Rationale:** Make a small team able to deploy and recover the shared platform without undocumented procedures.

**Actor:** Authorized release operator; developer; QA.

**Preconditions:** Q03/Q14 environment, hosting, secret, backup and operational ownership decisions accepted.

**Trigger:** Deployment, migration, incident recovery or rollback.

**Expected behavior:** Validate release/config; apply explicit reviewed migration once; start API/workers only with compatible schema; smoke-test access/integration/AI paths; monitor; roll back compatible application or forward-fix incompatible migration. Restore in isolated environment and reconcile unfinished jobs before enabling side effects.

**Inputs:** Versioned release, config/secret references, migration plan and backup.

**Outputs:** Verified deployment/recovery record, version/health results and runbook evidence.

**Validation rules:** No development credentials in shared environments; no destructive automatic rollback; verify restore tenant and dedupe integrity.

**Authorization requirements:** Separate deployment/migration/backup permissions from runtime service grants; audit operational changes.

**Error scenarios:** Migration failure halts rollout; readiness failure stops traffic; uncertain jobs remain disabled pending reconciliation.

**Dependencies:** Q03/Q09/Q10/Q14; all release-scope contracts.

**Priority:** P0 PROPOSED release gate

**Acceptance criteria:** AC-OPS-001.a: clean environment is deployable from documented inputs. .b: failed migration does not receive traffic. .c: restore rehearsal preserves mappings/audit and does not blindly repeat side effects. .d: agreed RPO/RTO evidence is recorded after targets exist.

**Verification method:** TC-OPS-001: deployment smoke, migration compatibility, rollback and isolated restore/replay rehearsal.

**Source reference:** PROPOSED operational elaboration of S06 pp5,21-22; no hosting/RPO/RTO commitment supplied.

**Status:** PROPOSED

## 7. User stories and workflows

### W01 - Authorized access

As a domain developer, I want shared access checks so that the same identity and resource policy apply to APIs and agents. Entry: CT-01 agreed and tenant service enabled. Main flow: authenticate through Team 1; validate subject and organization membership; load resource in its tenant; ask the authorized policy/resource authority; execute only on allow; emit the required outcome audit. Alternative: a scoped workload acts as itself with its own explicit grant. Failures: invalid identity, revoked membership, resource mismatch and unavailable decision service deny access. State: no domain mutation on deny. Audit: authorization denial and approved sensitive action metadata, no token. [S00; S06 pp6-8,20]

### W02 - Connect, synchronize and recover

As an integration administrator, I want an observable connection lifecycle so that provider data reaches the owning Nexora team reliably. Entry: approved adapter, CT-01 and domain contract, credential reference and provider grant. Main flow: authorize create; validate non-secret config and provider installation; persist connection and audit; accept an authenticated webhook durably or enqueue sync; fetch pages; transform to agreed envelope; deliver to domain owner; record acknowledgment and checkpoint. Alternative: poll provider when its adapter supports it; unsupported capabilities return an explicit unsupported result. Failure: provider rate limit defers work; expired credential blocks work; receiver timeout retains work for retry/reconciliation; disconnect stops future execution and invalidates queued work at execution time. State: connection/job/delivery history only in Team 5; canonical record in owning team. Audit: connect, disconnect, credential change and operator replay. [S06 pp9-10; proposed mechanics FR-REL-001]

```mermaid
sequenceDiagram
    participant Provider
    participant Ingress as Team 5 ingress (proposed)
    participant DB as Durable inbox (proposed)
    participant Worker as Team 5 worker (proposed)
    participant Domain as Team 3 canonical API (contract pending)
    Provider->>Ingress: Signed delivery
    Ingress->>Ingress: Verify raw payload and connection binding
    Ingress->>DB: Commit receipt and unique delivery identity
    DB-->>Ingress: Durable acknowledgment
    Ingress-->>Provider: Accepted or already accepted
    Worker->>DB: Claim eligible delivery
    Worker->>Worker: Recheck connection and authority
    Worker->>Domain: Idempotent canonical ingest
    Domain-->>Worker: Accepted record ID or conflict
    Worker->>DB: Record outcome; advance checkpoint only on acceptance
```

### W03 - Advisory AI with permitted evidence

As an investigator, I want AI assistance grounded in accessible evidence so that I can review its reasoning. Entry: Team 4 owns incident and context policy; allowed model/agent/tool versions exist. Main flow: receive delegated request; check resource grants and policy; assemble permitted references via registered tools; label retrieved content untrusted; invoke gateway with bounded context; validate model output; persist execution metadata and metering; return draft result to Team 4. Alternatives: missing evidence is returned as missing/partial, not fabricated; model failure returns a typed failure with attempt state. Failure: access revoked mid-run stops later tool calls; budget failure blocks dispatch; invalid tool proposal is rejected. State: Team 5 execution/usage metadata; Team 4 alone creates RCA evidence/findings. Audit: request and tool outcomes correlated. [S01 pp13-15; S06 pp11-15,20]

### W04 - Human-controlled proposed action

As a reviewer, I want to inspect the exact proposed operation before execution so that approval applies only to what I reviewed. Entry: assisted action explicitly included in release, CT-04 approval contract agreed. Proposed flow: agent produces inert proposal; Team 4 obtains human decision; platform validates approval issuer, tenant, actor, resource, tool/version, argument digest and expiry; rechecks current permission; atomically claims execution; invokes registered action; records outcome. Changed arguments, expired/revoked approval or deny result stop execution. Unknown external side-effect outcome enters reconciliation, never blind re-execution. Approval is not inferred from model text or a client boolean. No default merge/deploy tool. [S01 pp14-15; S05 pp12,14; S06 pp14,20; binding details proposed]

### W05 - Investigate a failure

As an operator or auditor, I want redacted, correlated records so that I can explain a failed integration or AI call. Entry: permitted tenant and audit/operational grant. Main flow: query request or execution ID; inspect status, attempts, decisions and provider error category; trace delivery; request authorized replay only after side-effect safety review. Alternative: expired payload retention returns metadata and explicit unavailable content. Failure: audit access denial is recorded; infrastructure unavailability returns unavailable, not empty success. State: append-only diagnostic/replay audit. No secret reveal workflow. [S06 pp5,8,11,15; proposed recovery]

### W06 - Evaluate a prompt/model change

As a domain evaluator, I want a versioned comparison against reviewed examples so that a changed prompt or model can be assessed before promotion. Entry: approved dataset access and Team 3/4 rubric. Main flow: execute approved cases through the same gateway/policy path; retain safe expected/actual result references, versions, latency/cost and rubric scores; report failures/unknowns. Alternative: synthetic-only evaluation while real data permission is pending. Failure: incomplete provider run is not a quality pass; no automatic promotion from a single score. State: versioned evaluation results, no modification of production incidents. [S06 p15; specific process proposed]

## 8. Non-functional requirements

These are testable proposed release controls except where the source capability is cited. No numerical SLO is silently introduced.

| ID / area | Required behavior and status | Verification / unresolved target |
|---|---|---|
| NFR-01 Performance | PROPOSED: bounded request body, pagination, concurrency, timeouts and queue admission; expose observed latency | Load test approved workload including provider latency; Q09 sets p95/p99, load, dataset and thresholds before release |
| NFR-02 Reliability | PROPOSED: durable acceptance before acknowledgment, bounded retries, duplicate safety and reconciliation | Crash at every delivery boundary; TC-REL-001; no exactly-once promise |
| NFR-03 Availability | PROPOSED: fail health/readiness accurately; isolate external provider degradation from local liveness | Disable DB/provider/identity independently; Q09 sets service SLO and maintenance treatment |
| NFR-04 Scalability | PROPOSED: tenant quotas, bounded parallel workers, indexed tenant queries and backpressure | Concurrent tenant and backlog tests; Q09 establishes capacity and noisy-neighbor thresholds |
| NFR-05 Security | CONFIRMED least privilege/no AI bypass S06 pp6,20; proposed tests enforce all entry paths | Cross-tenant reads/writes, forged context, revoked permission, malicious tool result and webhook matrix |
| NFR-06 Privacy | PROPOSED: minimize stored and transmitted content; redact telemetry; retention by class | Seed canary secrets/PII; inspect API, logs, traces and backups; Q10 determines retention/residency and deletion obligations |
| NFR-07 Maintainability | CONFIRMED common standards S06 p5; proposed module boundaries and versioned contracts | Review dependency direction; add fake provider using shared interface without modifying domain logic |
| NFR-08 Testability | PROPOSED: deterministic clocks/provider fakes, contract fixtures and fault injection | Reproducible permission, retry, lease and billing tests without paid provider calls |
| NFR-09 Observability | CONFIRMED logging/correlation S06 p5; proposed metrics/traces and alerts | Trace one request across ingress/job/domain acknowledgment; verify sanitized logs and alert route |
| NFR-10 Accessibility | OPEN DECISION: Team 5 UI scope/owner unknown; proposed admin UI must support keyboard access, labels and readable status/errors | Q13 agrees UI scope and accessibility standard; API-only release documents accessible integration examples |
| NFR-11 Deployment | PROPOSED: validated config, explicit migrations, immutable release identity and controlled rollback | Clean environment deployment; missing-secret startup failure; forward/backward compatibility test |
| NFR-12 Recovery/support | PROPOSED: restore rehearsal and replay runbook preserve tenant and deduplication boundaries | Restore isolated backup and reconcile queued/unknown work; Q14 sets RPO/RTO, backup retention and operational owner |

## 9. Security and governance requirements

See [security.md](security.md) for threat cases and implementation checklist. Team 1 establishes identity and permission policy; platform enforcement and each resource owner validate scope. A caller-supplied organization identifier is a selector, never proof of membership. Background execution retains the initiating subject or an explicit service grant and revalidates current authority before external or domain side effects.

Integration and model credentials use restricted secret references, not database JSON, logs or AI prompts. Rotation must support verification before switching and revocation after cutover; disconnect disables pending work. Webhooks are authenticated using the adapter's verified mechanism, then deduplicated and bound to the connection tenant. Rate limits and body limits protect ingress before expensive parsing/model work; identity/resource quotas apply after authentication. Thresholds require Q09 agreement.

AI reads untrusted code, tickets, logs and tool results. Those inputs cannot alter authorization, tool definitions, egress allowlists or approvals. Tool arguments and output are schema checked; registered executable code is selected by server configuration, never by model-supplied code or URL. Higher-risk actions require policy and the agreed human approval evidence. Provider fallback must remain inside approved data/tenant/model policy; no silent cross-provider transfer. Costs distinguish estimates from actual provider-reported usage and unknown outcomes. [S01 p15; S06 pp11-15,20; enforcement details proposed]

Audit records retain actor type, tenant, resource reference, decision/outcome, time and correlation. Sensitive successful mutations require durable audit intent within the local transaction or pre-dispatch record; loss of an observability exporter must not erase the business audit trail. Retention, deletion exceptions and raw-content capture are unresolved Q10 decisions, not an assumed compliance certification.

## 10. Dependencies and contracts

All detailed payloads and new interfaces in [api-contracts.md](api-contracts.md) are proposed. Paths printed in source PDFs are source-specified only; implementation and adoption are unverified.

| Provider | Consumer / required data | Contract and trust | Failure behavior proposed | Status / agreement needed |
|---|---|---|---|---|
| Team 1 / Avinash | All platform operations: user/service identity, organization membership/status, grants, user-to-employee mapping | CT-01; authenticated service connection; issuer/audience/revocation and resource checks agreed | Invalid credentials denied; unavailable validation fails closed; never use email as identity | BLOCKER Q01-Q02; coordinator must record handoff; Team 1 and Sagar agree semantics |
| Team 2 / Abhishek | Work integrations and context: project/task IDs, tenant, resource access, native/external precedence | CT-02; scoped service plus delegated subject; accepted canonical upsert or read contract | Queue retryable delivery; quarantine mapping conflicts; no local task replica to bypass outage | BLOCKER Q04 for live work sync; project membership boundary unresolved |
| Team 3 / Srushti | GitHub data destination and AI context: repository/branch/commit/PR/build/deployment IDs and schemas | CT-03; Team 3 owns canonical data and engineering semantics | Acknowledge ingest before checkpoint; duplicate replay safe; unauthorized resources denied | BLOCKER Q04-Q05 for live GitHub flow; source read paths exist on paper |
| Team 4 / Poonam | Telemetry recipient, incident/evidence references, domain agent inputs, human approval decisions | CT-04; resource authority and approval issuer checked | Preserve partial/unknown evidence; no fabricated RCA; block write on missing approval | BLOCKER Q05/Q08 for affected flows; Team 4 owns normalization/approval |
| All domain teams | Audit and event producers/consumers; trustworthy resource provenance and event versions | CT-06; producer authenticated and allowed event types/tenant scope | Durable local outbox or explicit producer failure; retries with dedupe | Q10-Q11; delivery/retention/notification subscriptions pending |
| Team 5 configuration owners | Gateway provider/model grants, tool/agent versions, costs and policies | CT-07; administration subject to CT-01 | Reject unconfigured provider/model/tool; unknown cost remains unknown | Q06-Q08/Q12; model and provider choices not selected |

External providers require account access, scope approval, quotas, network egress and test fixtures. GitHub is an initial target; other source-listed providers are candidates, not claims of available credentials or implemented adapters.

## 11. Acceptance and definition of done

### 11.1 Feature gate

A feature is done only when its accepted behavior version, requirement IDs and AC/TC bundles are linked to reviewed changes; required provider and consumer contracts are accepted; positive, negative, tenant-isolation and relevant replay/failure tests pass; schema migrations and compatibility are reviewed; secrets and logs are checked; operational configuration and runbooks are documented; the feature is demonstrated in an agreed environment; and remaining risks have explicit disposition by the responsible reviewer. Code compilation alone does not satisfy completion.

Mock-based completion is labelled **component verified with fixtures**. It is not **cross-team integrated**. A blocked security or ownership dependency cannot be waived by changing a task label. A release exclusion requires a recorded scope decision and disabled routes/jobs/tools for the excluded capability.

### 11.2 Release acceptance chains

| Chain / test ID | Demonstration | Required negative test | Sources |
|---|---|---|---|
| E2E-01 Access | Team 1 authenticates; Team 5 enforces tenant/resource authorization; a domain request has correlated audit | User/agent cannot read another organization's resource; dependency failure denies | S06 p22 access chain revised by S00 |
| E2E-02 Integration | Approved external delivery traverses connector to owning canonical service with visible sync history | Duplicate, out-of-order delivery, consumer timeout, restart and disconnect do not create duplicate or unauthorized data | S06 p22; resilience proposed |
| E2E-03 AI | Approved domain agent uses gateway, registered tool, authorization, policy, result and audit | Injection, denied tool, revoked permission, provider timeout and missing approval stop unsafe execution | S06 pp20,22 |
| E2E-04 Operations | Deployed version survives agreed fault/recovery rehearsal, with runbook and usage reconciliation | Unknown side-effect or billable outcome remains visible for reconciliation | PROPOSED FR-OPS-001 |

QA review is required as a proposed process; the resource plan inconsistently labels Megha/Meghana, so do not assume a personal commitment (Q16). No deployment, coding, commit or push is part of this documentation work.

## 12. Risks, assumptions and open questions

The authoritative decision register is [open-questions.md](open-questions.md). Likelihood below is not quantified without operational evidence.

| ID | Description / impact | Likelihood | Mitigation and required decision | Responsible stakeholder | Resolution gate |
|---|---|---|---|---|---|
| R01 | Identity ownership conflict can produce duplicate IAM and incompatible clients | Conflict observed | Adopt S00 boundary; explicitly transfer legacy auth paths and assignments (Q01) | Coordinator, Team 1 lead, Sagar | Before access integration |
| R02 | Proposed ERDs duplicate organization/repository/work items and omit tenant scope | Conflict observed | Reference domain owners; approve revised constraints (Q02/Q15) | Sagar and Teams 1-4 | Before migrations |
| R03 | Approx. six gross person-hours/day across 16 source modules creates overload | High planning concern, not measured | Small vertical slices; review capacity and source priority inconsistency (Q13/Q16) | Sagar/coordinator | Before release commitment |
| R04 | No agreed service identity, model provider, budget or egress policy | Open dependency | Fail closed; synthetic providers until approved (Q06/Q07) | Sagar, technical lead, coordinator | Before live provider access |
| R05 | AI-generated operation may exceed user permission or approval | Severity high; likelihood unmeasured | Policy intersection, bound approvals and adversarial tests (Q08) | Sagar, Team 1/4 leads | Before any write tool |
| R06 | Retries may duplicate domain changes or billable model calls | Design risk | Durable dedupe and per-attempt accounting; reconcile unknown outcomes | Sagar, consumer leads | Before integration/AI acceptance |
| R07 | Retained telemetry/evidence may expose sensitive data | Data categories not classified | Default minimization; approve retention/residency and dataset handling (Q10) | Coordinator and domain data owners | Before production data |
| R08 | SLO/support/backup ownership absent | Unknown | Benchmark, agree targets and restore drill (Q09/Q14) | Technical lead and coordinator | Before deployment acceptance |
| A01 | ASSUMPTION: a modular FastAPI backend can support the first slice | Provisional | Source specifies FastAPI; exact repository/deployment topology Q03; split worker process only as needed | Sagar/technical lead | Architecture review |
| A02 | ASSUMPTION: integration starts read-only into owner-approved ingest APIs | Provisional | Limits conflict risk; bidirectional sync and write-back deferred until Q04 | Teams 2/3/4 and Sagar | Connector contract review |
| A03 | ASSUMPTION: no general user-facing Team 5 console is required in first slice | Provisional | UI endpoints/personas remain documented; Q13 confirms interface owner and accessibility needs | Coordinator/Sagar | MVP scope review |
| A04 | ASSUMPTION: all ERD UUIDs and human-readable spec IDs are illustrative | Explicitly cautious | Treat cross-team IDs as opaque until Q02; cannot finalize external-reference SQL types yet | All leads | Schema/contract review |

## 13. Traceability matrix

The source key resolves exact filenames in section 1.2. Components are defined in architecture section 3; contracts in api-contracts.md; tasks in implementation-plan.md. Test bundles below describe planned tests, not executed application tests. Each AC identifier resolves to its requirement card.

| Requirement | Source | Component | Contract | Tasks | Test bundle | Acceptance bundle |
|---|---|---|---|---|---|---|
| FR-PLAT-001 | S06 p5 §03; S01 p18 §15. | M01 | CT-05 | T04, T05 | TC-PLAT-001 | AC-PLAT-001 |
| FR-PLAT-002 | S00 coordinator boundary; conflicting S06 pp5,16,18; S02 p14. | M02 | CT-01 | T06 | TC-PLAT-002 | AC-PLAT-002 |
| FR-PLAT-003 | S00; S06 pp6,12,20; S01 p15. | M02, M10 | CT-01 | T07, T24 | TC-PLAT-003 | AC-PLAT-003 |
| FR-PLAT-004 | S00; S06 p7 §06; S12 panel1 is proposed and conflicts with ownership. | M02 | CT-01 | T08 | TC-PLAT-004 | AC-PLAT-004 |
| FR-PLAT-005 | S06 p8 §07; S12 panel10. | M03 | CT-06 | T09, T10 | TC-PLAT-005 | AC-PLAT-005 |
| FR-PLAT-006 | S06 p9 §08 and p16 integration API list. | M04 | CT-05 | T11, T13 | TC-PLAT-006 | AC-PLAT-006 |
| FR-PLAT-007 | S06 p10 §09; S04 pp6,15,20; S12 panel3 is not canonical ownership approval. | M05 | CT-03 | T14, T15 | TC-PLAT-007 | AC-PLAT-007 |
| FR-PLAT-008 | S06 p10 §09; S03; S12 panel4 proposes external projections only. | M06 | CT-02 | T27 | TC-PLAT-008 | AC-PLAT-008 |
| FR-PLAT-009 | S06 p10 §09; S05 p6 §04; S12 panel5 unresolved catalog ownership. | M07 | CT-04 | T28 | TC-PLAT-009 | AC-PLAT-009 |
| FR-PLAT-010 | S06 p11 §10; S01 p18. | M08 | CT-07 | T17, T18, T19 | TC-PLAT-010 | AC-PLAT-010 |
| FR-PLAT-011 | S06 p12 §11; S01 p15 §12; S12 panel7. | M09 | CT-07 | T20 | TC-PLAT-011 | AC-PLAT-011 |
| FR-PLAT-012 | S06 p13 §12; S01 pp13-15. | M09 | CT-07 | T22, T23 | TC-PLAT-012 | AC-PLAT-012 |
| FR-PLAT-013 | S06 pp14,20,23; S01 pp14-15; S05 pp12,14. | M10 | CT-04, CT-07 | T21, T24 | TC-PLAT-013 | AC-PLAT-013 |
| FR-PLAT-014 | S06 pp11,15 §14; S12 panels6,9. | M11 | CT-07 | T19, T25 | TC-PLAT-014 | AC-PLAT-014 |
| FR-PLAT-015 | S06 p15 §14; S12 evaluation_result lacks full dataset model. | M12 | CT-07 | T29 | TC-PLAT-015 | AC-PLAT-015 |
| FR-PLAT-016 | S06 pp8,23; S12 platform_event/event_delivery proposed. | M03 | CT-06 | T26, T30 | TC-PLAT-016 | AC-PLAT-016 |
| FR-SEC-001 | PROPOSED security elaboration of S06 pp6,9,11,20; S12 credential-bearing config risk. | M04, M08 | CT-05, CT-07 | T12 | TC-SEC-001 | AC-SEC-001 |
| FR-SEC-002 | PROPOSED elaboration of S06 pp9-10; technical reference: GitHub validating webhook deliveries (architecture references). | M04, M05 | CT-03, CT-05 | T16 | TC-SEC-002 | AC-SEC-002 |
| FR-SEC-003 | PROPOSED implementation controls for S01 p15 and S06 pp12,20. | M08, M09, M10 | CT-07 | T23 | TC-SEC-003 | AC-SEC-003 |
| FR-REL-001 | PROPOSED reliability implementation for S06 pp9-11,22 and S12 sync/event history. | M03, M04, M09 | CT-02, CT-03, CT-04, CT-06, CT-07 | T13, T26, T31 | TC-REL-001 | AC-REL-001 |
| FR-DATA-001 | S00 ownership is CONFIRMED; mapping/constraint design PROPOSED from S12 panels1-4 and all team ERDs. | M02, M04 | CT-01, CT-02, CT-03, CT-04 | T08, T15, T32 | TC-DATA-001 | AC-DATA-001 |
| FR-OPS-001 | PROPOSED operational elaboration of S06 pp5,21-22; no hosting/RPO/RTO commitment supplied. | M01 | CT-05 | T33, T34 | TC-OPS-001 | AC-OPS-001 |
