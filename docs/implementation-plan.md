# Team 5 implementation and readiness plan

Version 0.1 | 2026-10-27 | **PROPOSED task breakdown, not assigned commitments or release approval**

This plan implements the capability requirements in [PRD.md](PRD.md). No application work was performed for this documentation task. A source-confirmed capability is not an approved design or proof that its prerequisites exist. All implementation tasks below remain proposed until their design and dependency gates are accepted. Readiness labels describe what prevents work, not stakeholder signoff.

## 1. Capacity and working rules

Sagar, Varshini and Sharanbasava have approximately two hours each per day (S00): approximately six gross person-hours, before review, coordination and interruptions. No delivery date or velocity is inferred. S06 p17 assigns platform/security work to Sagar/Varshini and a broad integrations/AI scope to Sharanbasva (spelling differs); the suggested owners below follow that pattern while making review and pairing explicit. Q16 confirms assignments and QA identity.

**PROPOSED working cadence:** one active small change per person; reserve time for review and cross-team questions; keep each review about one behavior. A card is a bounded outcome, not a promise it fits in one daily session. For larger cards, use the increments listed in Required behavior; each increment gets its own review and tests. If an increment cannot be reviewed after a few focused sessions, split by operation or failure boundary before coding. Sagar coordinates dependencies and security review rather than leaving the entire AI surface to one developer.

Varshini's initial path is T03, then T05 after its gate, followed by paired T06/T08 and bounded T09/T10 or T20 schema work. Production authorization, webhook verification and migrations require experienced review. This is a proposed onboarding sequence, not an assessment of her ability or an individual commitment.

## 2. Readiness classes and controlled sequence

| Class | Meaning | Current examples |
|---|---|---|
| READY | Can start now as documentation/review/test-design work, without approving an API or coding a feature | T01-T03 |
| INTERNAL DECISION | Sagar/technical lead must accept local design, selected schema/library/config conventions; other listed dependencies still apply | T04-T05, T11, T16-T17, T23; T13/T19/T20 are fixture-ready only until their listed external gates clear |
| OTHER TEAM | A provider/consumer lead must accept identity, domain schema, permissions, normalization, context or approval contract | T06-T10, T14-T15, T22, T26, T29, T31; T13/T19/T20 require these for a live slice |
| COORDINATOR DECISION | Product scope, infrastructure/data policy, provider/budget/autonomy or operations ownership must be agreed | T12, T18, T21, T25, T30, T33-T34 |
| Combined gates | All named classes must clear; clearing one is insufficient | T24, T27-T28, T32 |

1. Prepare T01-T03 and record actual decisions with date, approver, affected contract/version and task IDs.
2. After Q03, implement T04-T05 locally; after CT-01/identifiers, T06-T10 establish access and audit.
3. Approve a schema slice and secret/worker design, then T11-T16/T32 prove one GitHub-to-Team 3 path.
4. Build fake provider/registry/policy contracts, then enable T18/T22 only after metering, policy, identity and data gates are satisfied. Run adversarial T23 before live advisory AI acceptance.
5. Demonstrate T31 chains and T33-T34 operations for the agreed first slice. Treat assisted writes T24 and P1 connectors/reporting/evaluation/notifications as separate accepted scope.

The source cycles in S06 p21 are sequence guidance, not deadlines. Policy and minimum usage/audit controls accompany the first executable AI call even though the source diagram places broad governance in a later cycle.

## 3. Task cards

Every implementation card inherits the relevant feature-level PRD definition of done: reviewed behavior, accepted contracts, negative/security tests, safe logs, documented errors, deployment compatibility and explicit dependency disposition. T01-T03 are preparation tasks: completing their stated documentation outputs does not close an AC bundle, obtain stakeholder approval, or mark a feature integrated. Each implementation task closes only the AC subcases its specific output can demonstrate; the linked full AC/TC bundle remains feature-level until all contributing tasks and integration gates pass. Suggested filenames are illustrative until Q03 accepts a repository layout; module IDs are the stable placement contract.



### T01 - Resolve source conflicts and release boundary

**Task ID:** T01

**Requirement IDs:** FR-PLAT-002, FR-PLAT-003, FR-DATA-001

**Readiness / approval gate:** READY: documentation review only

**Description and rationale:** Preserve the coordinator boundary and one authentication authority despite older Team 5 auth ownership text. A model or background process must not bypass the permissions of the principal it represents. Reconcile ERD overlap and keep cross-team provenance consistent.

**Expected files or components:** docs/source-inventory.md; docs/open-questions.md

**Inputs:** Source hierarchy and C01-C10 discrepancies

**Outputs:** Decision agenda, proposed ownership handoff and release-scope checklist

**Required behavior:** Prepare exact alternatives and impacts; record actual reviewer decisions only when received. Coordinator response, not preparation of the agenda, closes Q01/Q13.

**Error handling:** Unanswered item stays OPEN DECISION with owner and blocked tasks.

**Security checks:** Do not assume identity or data ownership from an ERD.

**Dependencies:** None; uses supplied sources

**Acceptance criteria:** Task completion: the agenda identifies every C01-C10 conflict, affected requirement/task and accountable decision owner; the register preserves all unresolved items. This task does not satisfy AC-PLAT-002, AC-PLAT-003 or AC-DATA-001 and cannot close Q01/Q13.

**Tests:** Source citation spot-check and ownership matrix review

**Priority:** P0

**Suggested owner:** Sagar

**Review requirements:** Coordinator, Vignesh and affected leads review conflict disposition

**Reviewer completion evidence:** source citations, conflict matrix, open-question links and a review agenda; no external approval is implied.

### T02 - Prepare cross-team contract review fixtures

**Task ID:** T02

**Requirement IDs:** FR-PLAT-004, FR-PLAT-006, FR-PLAT-007, FR-PLAT-012

**Readiness / approval gate:** READY: proposed schemas/examples only

**Description and rationale:** Prevent cross-organization data disclosure or mutation while retaining Team 1 organizational ownership. Share credential handling, status and delivery mechanics while keeping provider-specific behavior explicit. Give Team 3 normalized provider data and Team 4 approved change/deployment context. Reuse safe execution infrastructure without centralizing domain intelligence in Team 5.

**Expected files or components:** docs/api-contracts.md; later contracts/ fixtures (proposed)

**Inputs:** CT-01 through CT-07 draft contracts

**Outputs:** Positive, invalid, cross-tenant, duplicate and partial-response example set

**Required behavior:** Define version, identity provenance and consumer acknowledgment; list undefined fields rather than inventing approved values.

**Error handling:** An unresolved contract remains fixture-only, not integrated.

**Security checks:** Use synthetic IDs/content and no real tokens or customer data.

**Dependencies:** T01 inventory; no live service assumed

**Acceptance criteria:** Task completion: each CT draft has positive, invalid, cross-tenant, duplicate and partial/timeout examples; every undefined field is labelled open. This task prepares fixtures only and does not satisfy the linked feature AC bundles or accept a contract.

**Tests:** Parse JSON examples; provider/consumer walkthrough

**Priority:** P0

**Suggested owner:** Sagar with Sharanbasava

**Review requirements:** Each provider and consumer lead accepts their own contract; Team 1 reviews trust envelope

**Reviewer completion evidence:** parseable synthetic examples, source references, known gaps and provider/consumer review agenda; no contract acceptance is implied.

### T03 - Prepare acceptance and adversarial case specifications

**Task ID:** T03

**Requirement IDs:** FR-PLAT-005, FR-SEC-003, FR-REL-001, FR-OPS-001

**Readiness / approval gate:** READY: test-design documentation only

**Description and rationale:** Explain access decisions, connector changes and AI operations across services. Prevent indirect prompt injection, data exfiltration and model-driven privilege escalation. Avoid lost acknowledged work and duplicated external/domain side effects. Make a small team able to deploy and recover the shared platform without undocumented procedures.

**Expected files or components:** docs/test-cases.md (future optional); tests/ plan

**Inputs:** AC/TC bundles, source examples and synthetic tenants

**Outputs:** Test case descriptions with setup, stimulus and expected state/effect

**Required behavior:** Start with health/error and two-tenant access cases; then duplicate webhook and injection fixtures. No application feature code in current documentation task.

**Error handling:** Missing expected behavior becomes an open question instead of a passing placeholder.

**Security checks:** Use fake credentials and safe malicious text; do not contact providers.

**Dependencies:** Requirement cards; Q16 QA reviewer identity can be resolved later

**Acceptance criteria:** Task completion: planned cases state setup, stimulus, expected result, expected side-effect state and unresolved behavior; at least one two-tenant, duplicate-delivery and injection case is included. This task does not execute or satisfy the linked feature AC bundles.

**Tests:** Reviewer can execute each test narrative mentally with unambiguous expected result

**Priority:** P0

**Suggested owner:** Varshini paired with Sagar

**Review requirements:** Sagar and shared QA review; bounded onboarding task

**Reviewer completion evidence:** reviewed case design, source/reasoning references and clearly labelled fixture-only status.

### T04 - Create minimal foundation skeleton

**Task ID:** T04

**Requirement IDs:** FR-PLAT-001

**Readiness / approval gate:** INTERNAL DECISION

**Description and rationale:** Reduce inconsistent service behavior and make deployment failures diagnosable.

**Expected files or components:** M01; proposed app/main.py, core/config.py, pyproject.toml

**Inputs:** Accepted repository placement and framework configuration

**Outputs:** Minimal application composition and validated config interface

**Required behavior:** Keep module dependencies explicit; add only required dependencies and lock versions after review.

**Error handling:** Invalid required config prevents readiness; no silent defaults for secrets.

**Security checks:** Separate runtime/migration identities; no credentials committed.

**Dependencies:** Q03 repository/packaging; T01; accepted ADR for topology

**Acceptance criteria:** AC-PLAT-001; Minimal application composition and validated config interface must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-001 config/import smoke

**Priority:** P0

**Suggested owner:** Sagar

**Review requirements:** Technical lead reviews topology and dependency selection

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T05 - Implement health, version and safe errors

**Task ID:** T05

**Requirement IDs:** FR-PLAT-001

**Readiness / approval gate:** INTERNAL DECISION

**Description and rationale:** Reduce inconsistent service behavior and make deployment failures diagnosable.

**Expected files or components:** M01; proposed health routes, error handlers, logging context

**Inputs:** Validated config, DB probe result, release ID, incoming request

**Outputs:** Health/readiness/version responses and request-correlated error/log

**Required behavior:** Implement one endpoint/handler per review; keep process liveness separate from external provider status.

**Error handling:** DB unavailable reports not ready; unexpected exception sanitized.

**Security checks:** Probe responses omit secrets and internal topology; reject malformed request IDs.

**Dependencies:** T04; CT-05 health/error schema; Q14 exposure policy

**Acceptance criteria:** AC-PLAT-001; Health/readiness/version responses and request-correlated error/log must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-001 endpoint/fault/log-canary cases

**Priority:** P0

**Suggested owner:** Varshini

**Review requirements:** Sagar reviews exception and redaction path; QA checks statuses

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T06 - Implement Team 1 authentication adapter

**Task ID:** T06

**Requirement IDs:** FR-PLAT-002

**Readiness / approval gate:** OTHER TEAM

**Description and rationale:** Preserve the coordinator boundary and one authentication authority despite older Team 5 auth ownership text.

**Expected files or components:** M02; proposed access/principal.py and identity_adapter.py

**Inputs:** Team 1 validation protocol and fixtures

**Outputs:** Validated principal dependency with categorized failures

**Required behavior:** Use one selected protocol; no token issuer, password or session schema.

**Error handling:** Invalid/expired/revoked identity denied; validation outage unavailable and denied.

**Security checks:** Verify all protocol trust properties; service identity cannot invent delegation.

**Dependencies:** Q01/Q02; accepted CT-01; T04

**Acceptance criteria:** AC-PLAT-002; Validated principal dependency with categorized failures must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-002 contract and live integration

**Priority:** P0

**Suggested owner:** Varshini paired with Sagar

**Review requirements:** Team 1 lead reviews protocol; Sagar performs security review

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T07 - Implement resource authorization adapter

**Task ID:** T07

**Requirement IDs:** FR-PLAT-003

**Readiness / approval gate:** OTHER TEAM

**Description and rationale:** A model or background process must not bypass the permissions of the principal it represents.

**Expected files or components:** M02; proposed authorization.py and policy context

**Inputs:** Principal, tenant, action, resource and delegated scope

**Outputs:** Allow/deny/unavailable decision; audit metadata

**Required behavior:** Centralize enforcement dependency; recheck on queued side-effect dispatch.

**Error handling:** Unknown permission/resource or unavailable decision denies.

**Security checks:** No role copying or permission derived solely from assignment.

**Dependencies:** T06; Team 1 permission vocabulary and resource-owner rules CT-01/02/03/04

**Acceptance criteria:** AC-PLAT-003; Allow/deny/unavailable decision; audit metadata must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-003 user/agent parity and revocation tests

**Priority:** P0

**Suggested owner:** Sagar with Varshini

**Review requirements:** Team 1 and relevant domain lead review authorization contract

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T08 - Implement tenant and reference guards

**Task ID:** T08

**Requirement IDs:** FR-PLAT-004, FR-DATA-001

**Readiness / approval gate:** OTHER TEAM

**Description and rationale:** Prevent cross-organization data disclosure or mutation while retaining Team 1 organizational ownership. Reconcile ERD overlap and keep cross-team provenance consistent.

**Expected files or components:** M02/M04; proposed tenant-scoped query helpers and reference validator

**Inputs:** Trusted membership/connection binding and owner references

**Outputs:** Tenant-bound operations and explicit unresolved reference results

**Required behavior:** Scope API, worker, mapping, cache and export paths; validate child-parent tenant equality.

**Error handling:** Unknown/mismatched reference blocks or quarantines; never repair by inventing entity.

**Security checks:** No user_id/employee_id substitution; enforce two-tenant constraints.

**Dependencies:** T06/T07; Q02/Q15 identifier and tenant semantics

**Acceptance criteria:** AC-PLAT-004, AC-DATA-001; Tenant-bound operations and explicit unresolved reference results must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-004 and TC-DATA-001 negative matrix

**Priority:** P0

**Suggested owner:** Varshini paired with Sagar

**Review requirements:** Sagar and owner teams verify query/reference boundaries

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T09 - Implement durable audit intake

**Task ID:** T09

**Requirement IDs:** FR-PLAT-005

**Readiness / approval gate:** OTHER TEAM

**Description and rationale:** Explain access decisions, connector changes and AI operations across services.

**Expected files or components:** M03; proposed audit ingestion/repository and migration

**Inputs:** Authenticated versioned audit envelope

**Outputs:** Durable deduplicated acknowledgment and append-only record

**Required behavior:** Validate allowlisted metadata and producer authority; local sensitive mutations use same-transaction audit intent.

**Error handling:** DB unavailable fails acceptance; duplicate returns original receipt.

**Security checks:** Redact secrets/content; no ordinary audit mutation API.

**Dependencies:** CT-06 producer schema; Q10/Q11; T06/T08; Q15 schema

**Acceptance criteria:** AC-PLAT-005; Durable deduplicated acknowledgment and append-only record must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-005 ingest/dedupe/redaction/audit-failure cases

**Priority:** P0

**Suggested owner:** Varshini

**Review requirements:** Sagar reviews integrity; producing teams review semantics

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T10 - Implement scoped audit query

**Task ID:** T10

**Requirement IDs:** FR-PLAT-005

**Readiness / approval gate:** OTHER TEAM

**Description and rationale:** Explain access decisions, connector changes and AI operations across services.

**Expected files or components:** M03; proposed audit query route/service

**Inputs:** Tenant, authorized filters and cursor

**Outputs:** Bounded audit page and next cursor

**Required behavior:** Only permit agreed filters; stable ordering; field visibility tied to permission.

**Error handling:** Malformed cursor/filter rejected; outage distinct from empty results.

**Security checks:** Prevent cross-tenant enumeration and metadata leakage.

**Dependencies:** T07/T09; CT-05 pagination/filter and CT-01 audit grants

**Acceptance criteria:** AC-PLAT-005; Bounded audit page and next cursor must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-005 audit read/access/pagination cases

**Priority:** P0

**Suggested owner:** Varshini

**Review requirements:** Sagar and QA inspect negative cases

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T11 - Implement adapter interface and connection lifecycle

**Task ID:** T11

**Requirement IDs:** FR-PLAT-006

**Readiness / approval gate:** INTERNAL DECISION

**Description and rationale:** Share credential handling, status and delivery mechanics while keeping provider-specific behavior explicit.

**Expected files or components:** M04; proposed connectors/base.py, registry.py, connections.py

**Inputs:** Accepted capability/config schema and fake adapter

**Outputs:** Typed adapter contract, fake implementation and lifecycle service

**Required behavior:** Implement one lifecycle operation per review; unsupported operations explicit.

**Error handling:** Configuration/credential/provider errors map to typed categories.

**Security checks:** Server allowlist selects adapters; no arbitrary Python imports or client authority.

**Dependencies:** Q06 provider/config decision; CT-05; T04; live API waits T06/T08

**Acceptance criteria:** AC-PLAT-006; Typed adapter contract, fake implementation and lifecycle service must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-006 conformance with fake adapter

**Priority:** P0

**Suggested owner:** Sharanbasava

**Review requirements:** Sagar reviews boundaries and lifecycle transitions

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T12 - Implement secret references and outbound policy

**Task ID:** T12

**Requirement IDs:** FR-SEC-001

**Readiness / approval gate:** COORDINATOR DECISION

**Description and rationale:** Limit credential leakage and server-side request forgery risk introduced by integrations.

**Expected files or components:** M04/M08; proposed secrets adapter and outbound transport

**Inputs:** Approved secret reference and provider endpoint policy

**Outputs:** Scoped credential resolution and safe provider HTTP transport

**Required behavior:** Separate retrieve/use from config storage; stage/verify/cutover rotation; restrict redirect and resolved destination.

**Error handling:** Secret unavailable or bad target stops dispatch; failed rotation preserves known state.

**Security checks:** No raw secret persistence/logging; least-privilege workload access.

**Dependencies:** Q06/Q14 secret/hosting/egress choice; T11

**Acceptance criteria:** AC-SEC-001; Scoped credential resolution and safe provider HTTP transport must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-SEC-001 leak, SSRF and rotation-failure cases

**Priority:** P0

**Suggested owner:** Sagar with Sharanbasava

**Review requirements:** Technical lead security review; operations owner approves lifecycle

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T13 - Implement durable sync job core

**Task ID:** T13

**Requirement IDs:** FR-PLAT-006, FR-REL-001

**Readiness / approval gate:** INTERNAL DECISION

**Description and rationale:** Share credential handling, status and delivery mechanics while keeping provider-specific behavior explicit. Avoid lost acknowledged work and duplicated external/domain side effects.

**Expected files or components:** M04; proposed jobs repository, lease worker, checkpoints and migrations

**Inputs:** Sync request with tenant/connection/key and durable storage

**Outputs:** Stable job ID, attempt state and safe checkpoint

**Required behavior:** Split admission/dedupe, lease claim, retry scheduling and status query into independent reviews. No checkpoint advance before consumer acceptance.

**Error handling:** Expired lease/retry exhaustion/ambiguous side effect are distinct states.

**Security checks:** Recheck connection and subject at dispatch; replay is separately authorized.

**Dependencies:** Q03/Q09/Q15 worker/limits/schema; T11; T12 for live provider; CT-06/T09 for durable audit; T08/T32 for approved tenant persistence; owner contract before live handoff. Fixture-only queue tests may begin after local design approval.

**Acceptance criteria:** AC-PLAT-006, AC-REL-001; Stable job ID, attempt state and safe checkpoint must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-REL-001 crash/concurrency suite; TC-PLAT-006 lifecycle suite

**Priority:** P0

**Suggested owner:** Sharanbasava

**Review requirements:** Sagar reviews transaction boundaries and crash windows

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T14 - Implement GitHub fetch adapters

**Task ID:** T14

**Requirement IDs:** FR-PLAT-007

**Readiness / approval gate:** OTHER TEAM

**Description and rationale:** Give Team 3 normalized provider data and Team 4 approved change/deployment context.

**Expected files or components:** M05; proposed github adapter and fixtures

**Inputs:** Allowed repository/PR identifiers, cursor and provider response

**Outputs:** Typed engineering envelope with provenance and explicit missing data

**Required behavior:** Review increments: repository/branches; commits; PR/diff/files; build/workflow; deployment where available. Each increment includes pagination/rate-limit handling.

**Error handling:** Provider deny/revoke/limit and unavailable record kinds remain distinct.

**Security checks:** Enforce installation repository access and resource grant for user-triggered reads.

**Dependencies:** T11/T12; CT-03; Q04/Q06 GitHub grant/scopes/test account

**Acceptance criteria:** AC-PLAT-007; Typed engineering envelope with provenance and explicit missing data must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-007 per-record fixtures and provider integration

**Priority:** P0

**Suggested owner:** Sharanbasava

**Review requirements:** Team 3 reviews canonical semantics; Sagar reviews credential scope

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T15 - Implement canonical delivery and mapping

**Task ID:** T15

**Requirement IDs:** FR-PLAT-007, FR-DATA-001

**Readiness / approval gate:** OTHER TEAM

**Description and rationale:** Give Team 3 normalized provider data and Team 4 approved change/deployment context. Reconcile ERD overlap and keep cross-team provenance consistent.

**Expected files or components:** M04/M05; proposed canonical delivery and external mapping repository

**Inputs:** Engineering envelope, delivery key and Team 3 response

**Outputs:** Owner-returned canonical ID, durable mapping and acknowledgment history

**Required behavior:** Use scoped mapping uniqueness and owner revisions; keep canonical data with Team 3.

**Error handling:** Conflict or failed acknowledgment quarantines/retries without cursor advance.

**Security checks:** Validate owner/tenant and trusted receiver; no direct domain DB writes.

**Dependencies:** T13/T14; accepted CT-03 ingest/idempotency and Q02/Q04

**Acceptance criteria:** AC-PLAT-007, AC-DATA-001; Owner-returned canonical ID, durable mapping and acknowledgment history must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-007 replay/out-of-order/rename and TC-DATA-001 mappings

**Priority:** P0

**Suggested owner:** Sharanbasava

**Review requirements:** Team 3 consumer-contract review and Sagar transaction review

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T16 - Implement GitHub webhook admission

**Task ID:** T16

**Requirement IDs:** FR-SEC-002

**Readiness / approval gate:** INTERNAL DECISION

**Description and rationale:** Prevent forged events, cross-tenant injection and duplicate work.

**Expected files or components:** M04/M05; proposed webhook route, verifier and receipt repository

**Inputs:** Raw signed bytes and connection binding

**Outputs:** Durable validated delivery receipt or rejection

**Required behavior:** Validate before enqueue; signature uses exact bytes; delivery ID dedupe is separate from authenticity.

**Error handling:** Invalid signature/unknown binding reject; durable store failure not success.

**Security checks:** Never trust organization from payload; no full payload logs.

**Dependencies:** T12/T13; Q06/Q09 verification and body/retention limits; live flow T15

**Acceptance criteria:** AC-SEC-002; Durable validated delivery receipt or rejection must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-SEC-002 known-answer/mutation/replay/tenant tests

**Priority:** P0

**Suggested owner:** Varshini paired with Sharanbasava

**Review requirements:** Sagar security review; Team 3 verifies downstream fixture

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T17 - Implement AI provider abstraction

**Task ID:** T17

**Requirement IDs:** FR-PLAT-010

**Readiness / approval gate:** INTERNAL DECISION

**Description and rationale:** Avoid independent domain provider clients with inconsistent governance and accounting.

**Expected files or components:** M08; proposed providers/base.py and fake provider

**Inputs:** Normalized request and fake provider outcome

**Outputs:** Provider-agnostic response and typed error contract

**Required behavior:** Implement fake and approved provider adapter separately; support no unreviewed provider SDK behavior.

**Error handling:** Normalize timeout, limit, malformed result and provider denial.

**Security checks:** No provider secret in model context or returned metadata.

**Dependencies:** CT-07; T04; Q07 requested response/usage semantics

**Acceptance criteria:** AC-PLAT-010; Provider-agnostic response and typed error contract must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-010 fake adapter conformance

**Priority:** P0

**Suggested owner:** Sharanbasava

**Review requirements:** Sagar and Team 3/4 consumers review normalized shape

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T18 - Implement gateway routing and dispatch

**Task ID:** T18

**Requirement IDs:** FR-PLAT-010

**Readiness / approval gate:** COORDINATOR DECISION

**Description and rationale:** Avoid independent domain provider clients with inconsistent governance and accounting.

**Expected files or components:** M08; proposed gateway route/service

**Inputs:** Authorized request, model route, limits and policy

**Outputs:** Recorded model attempt and validated normalized result

**Required behavior:** Persist dispatch intent; apply approved timeout/retry/fallback rules; no silent provider transfer.

**Error handling:** Timeout keeps ambiguous usage visible; disabled/unapproved model never called.

**Security checks:** Authorize before dispatch; redact prompt/result telemetry and enforce provider egress.

**Dependencies:** Q06/Q07/Q10 provider/model/data policy; T07/T08/T09/T12/T17/T19/T21/T32; CT-01/CT-07 and approved tenant persistence before any live provider dispatch.

**Acceptance criteria:** AC-PLAT-010; Recorded model attempt and validated normalized result must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-010 deny/timeout/retry/fallback tests

**Priority:** P0

**Suggested owner:** Sharanbasava

**Review requirements:** Sagar security review; domain lead verifies consumer result

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T19 - Implement minimum per-attempt usage ledger

**Task ID:** T19

**Requirement IDs:** FR-PLAT-010, FR-PLAT-014

**Readiness / approval gate:** INTERNAL DECISION

**Description and rationale:** Avoid independent domain provider clients with inconsistent governance and accounting. Explain consumption and make provider charges and retries observable.

**Expected files or components:** M11; proposed attempt usage recorder and migration

**Inputs:** Dispatch/completion observations and provider attempt ID

**Outputs:** Deduplicated usage with reported/estimated/unknown provenance

**Required behavior:** Separate logical requests and physical attempts; record unknown rather than zero; make aggregates rebuildable.

**Error handling:** Repeated completion idempotent; missing result remains pending/unknown.

**Security checks:** Tenant-scoped writes only by trusted gateway; no raw prompt storage.

**Dependencies:** Q07 accounting semantics; Q15 schema; T17; T08/T09/T32 for a live ledger and audit correlation. Pure arithmetic fixtures may begin after internal design review.

**Acceptance criteria:** AC-PLAT-010, AC-PLAT-014; Deduplicated usage with reported/estimated/unknown provenance must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-014 duplicate/retry/unknown cases

**Priority:** P0

**Suggested owner:** Sharanbasava

**Review requirements:** Sagar checks billing and retry invariants

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T20 - Implement registry metadata and versioning

**Task ID:** T20

**Requirement IDs:** FR-PLAT-011

**Readiness / approval gate:** INTERNAL DECISION

**Description and rationale:** Make capabilities reviewable and remove unrestricted model access.

**Expected files or components:** M09; proposed tool/agent registry and schema validators

**Inputs:** Reviewed metadata, schema and implementation key

**Outputs:** Immutable versions, allowed tool bindings and read manifest

**Required behavior:** Start with inert/fake read tool; reject incomplete metadata; revocation blocks queued use.

**Error handling:** Duplicate version with changed content rejected; missing/disabled tools unavailable.

**Security checks:** No dynamic code from model/config; management separate from execution grant.

**Dependencies:** Q08 permissions/risk/admin rules; CT-01/CT-07; T07/T08/T09/T32 for live registry use. Schema validation against inert tools may begin after internal design review.

**Acceptance criteria:** AC-PLAT-011; Immutable versions, allowed tool bindings and read manifest must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-011 schema/version/permission/revocation cases

**Priority:** P0

**Suggested owner:** Varshini paired with Sharanbasava

**Review requirements:** Sagar reviews execution adapter registration and permission meanings

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T21 - Implement policy decision core

**Task ID:** T21

**Requirement IDs:** FR-PLAT-013

**Readiness / approval gate:** COORDINATOR DECISION

**Description and rationale:** Keep executable action under human and organizational authority.

**Expected files or components:** M10; proposed policy evaluator and decision record

**Inputs:** Principal/resource/tool/model context and versioned policy

**Outputs:** Allow/deny/approval-required with reason

**Required behavior:** Begin advisory-only; deny unknown combinations; policies only narrow existing grants.

**Error handling:** Unavailable or ambiguous policy fails closed.

**Security checks:** No client/model boolean grants approval; audit decisions.

**Dependencies:** Q08/Q13 autonomy scope; T07/T20; CT-07

**Acceptance criteria:** AC-PLAT-013; Allow/deny/approval-required with reason must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-013 advisory/deny/precedence cases

**Priority:** P0

**Suggested owner:** Sagar

**Review requirements:** Coordinator accepts autonomy scope; Team 1/4 and technical lead review

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T22 - Implement bounded advisory executor

**Task ID:** T22

**Requirement IDs:** FR-PLAT-012

**Readiness / approval gate:** OTHER TEAM

**Description and rationale:** Reuse safe execution infrastructure without centralizing domain intelligence in Team 5.

**Expected files or components:** M09; proposed execution state machine and context adapters

**Inputs:** Approved agent version, delegated context and authorized references

**Outputs:** Execution/step status, permitted result and provenance

**Required behavior:** Split create/status; one-model one-read-tool loop; bounded continuation; cancellation into reviews. Domain prompt/interpretation supplied by owner.

**Error handling:** Partial context/failed tool/timeout remains explicit; cancellation prevents new effects.

**Security checks:** Reauthorize each tool and continuation; freeze recorded versions and enforce revocation.

**Dependencies:** T07/T08/T09/T18/T19/T20/T21/T32; Q06/Q07/Q09/Q10 limits/provider/data policy; CT-01/02/03/04/07 context and authority contracts. No live execution without durable audit, tenant persistence and metering.

**Acceptance criteria:** AC-PLAT-012; Execution/step status, permitted result and provenance must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-012 deterministic lifecycle/restart/limit tests

**Priority:** P0

**Suggested owner:** Sharanbasava

**Review requirements:** Team 3/4 review domain interfaces; Sagar security review

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T23 - Implement injection-resistant dispatch validation

**Task ID:** T23

**Requirement IDs:** FR-SEC-003, FR-PLAT-012

**Readiness / approval gate:** INTERNAL DECISION

**Description and rationale:** Prevent indirect prompt injection, data exfiltration and model-driven privilege escalation. Reuse safe execution infrastructure without centralizing domain intelligence in Team 5.

**Expected files or components:** M08/M09/M10; proposed input provenance and typed dispatcher

**Inputs:** Untrusted context/model proposals

**Outputs:** Validated typed operation or denial record

**Required behavior:** Maintain instruction/data separation; validate schemas and authority outside model; no arbitrary command/URL execution.

**Error handling:** Invalid tool proposal halts step with safe reason; no fabricated evidence.

**Security checks:** Assert no forbidden tool/network dispatch even when model output looks plausible.

**Dependencies:** T20/T21/T22; reviewed adversarial fixtures T03

**Acceptance criteria:** AC-SEC-003, AC-PLAT-012; Validated typed operation or denial record must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-SEC-003 injection corpus and TC-PLAT-012 partial context

**Priority:** P0

**Suggested owner:** Sagar with Varshini

**Review requirements:** Sagar plus independent domain reviewer; QA checks side-effect assertions

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T24 - Implement approval-bound assisted execution

**Task ID:** T24

**Requirement IDs:** FR-PLAT-003, FR-PLAT-013

**Readiness / approval gate:** OTHER TEAM AND COORDINATOR DECISION

**Description and rationale:** A model or background process must not bypass the permissions of the principal it represents. Keep executable action under human and organizational authority.

**Expected files or components:** M09/M10; proposed approval verifier and execution claim

**Inputs:** Trusted Team 4 approval and exact operation digest

**Outputs:** Validated single operation claim and auditable outcome

**Required behavior:** Bind approval to tenant/resource/tool/version/arguments/actor/expiry; reauthorize immediately before dispatch; reconcile uncertain effects.

**Error handling:** Expired/revoked/mismatched approval denies; unknown outcome is not replayed blindly.

**Security checks:** No merge/deploy by default; durable pre-effect audit; reviewer authority validated.

**Dependencies:** Q08/Q13 explicit assisted scope; CT-04 approval proof; T21/T22/T23

**Acceptance criteria:** AC-PLAT-003, AC-PLAT-013; Validated single operation claim and auditable outcome must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-013 binding/revocation/race cases; TC-REL-001 uncertain write

**Priority:** P1 PROPOSED deferred; policy core remains P0

**Suggested owner:** Sagar with Sharanbasava

**Review requirements:** Team 4 and Team 1 sign contract; coordinator accepts scope; technical lead security review

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T25 - Implement usage reporting and pricing

**Task ID:** T25

**Requirement IDs:** FR-PLAT-014

**Readiness / approval gate:** COORDINATOR DECISION

**Description and rationale:** Explain consumption and make provider charges and retries observable.

**Expected files or components:** M11; proposed price versions and usage query

**Inputs:** Ledger, effective prices and authorized reporting window

**Outputs:** Decimal estimated cost, counts and completeness-aware summary

**Required behavior:** Separate price calculator then tenant query; rebuild aggregate from ledger; hard budgets require approved atomic reservation rules.

**Error handling:** Missing price/usage unknown; mixed currencies separate; cannot claim provider invoice total.

**Security checks:** Usage query tenant/subject visibility; no prompt exposure.

**Dependencies:** T19; Q07 pricing/units/currency/budget and CT-01 read grants

**Acceptance criteria:** AC-PLAT-014; Decimal estimated cost, counts and completeness-aware summary must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-014 effective-price/unknown/aggregate reconciliation

**Priority:** P1

**Suggested owner:** Varshini paired with Sharanbasava

**Review requirements:** Sagar reviews arithmetic and authorization; coordinator accepts budget policy

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T26 - Implement durable event publication/subscription

**Task ID:** T26

**Requirement IDs:** FR-PLAT-016, FR-REL-001

**Readiness / approval gate:** OTHER TEAM

**Description and rationale:** Decouple domain workflows and expose important changes without duplicating business logic. Avoid lost acknowledged work and duplicated external/domain side effects.

**Expected files or components:** M03; proposed outbox/delivery worker and subscription config

**Inputs:** Authenticated event and approved subscriber

**Outputs:** Durable event/delivery status and acknowledgment

**Required behavior:** Split publish, delivery claim/retry and consumer fixture; at-least-once delivery with dedupe.

**Error handling:** Bad version quarantines; consumer outage retries boundedly; no false exactly-once claim.

**Security checks:** Validate producer event/tenant scope and subscriber destination; no arbitrary callbacks.

**Dependencies:** CT-06 accepted producer/consumer events; Q11; T09/T13

**Acceptance criteria:** AC-PLAT-016, AC-REL-001; Durable event/delivery status and acknowledgment must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-016 and TC-REL-001 crash/replay cases

**Priority:** P1

**Suggested owner:** Varshini paired with Sagar

**Review requirements:** All affected producers/consumers review events; Sagar reliability review

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T27 - Implement first approved work-tool adapter

**Task ID:** T27

**Requirement IDs:** FR-PLAT-008

**Readiness / approval gate:** OTHER TEAM AND COORDINATOR DECISION

**Description and rationale:** Link external work intent to engineering without a separate Team 5 task system.

**Expected files or components:** M06; proposed selected provider adapter and mapping

**Inputs:** Provider work records and Team 2 mapping rules

**Outputs:** Canonical Team 2 envelopes and sync history

**Required behavior:** Slice project lookup, work-item page and conflict cases; other providers are separate future tasks after scope choice.

**Error handling:** Unknown user/parent/conflicting revision quarantines; no silent overwrite.

**Security checks:** Provider read grant and Team 2 authorized ingest; no local task source of truth.

**Dependencies:** Q04/Q06/Q13 selected provider/direction; CT-02; T11/T12/T13

**Acceptance criteria:** AC-PLAT-008; Canonical Team 2 envelopes and sync history must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-008 selected provider fixtures and live consumer integration

**Priority:** P1

**Suggested owner:** Sharanbasava

**Review requirements:** Team 2 reviews mapping/ownership; Sagar security review

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T28 - Implement first approved observability adapter

**Task ID:** T28

**Requirement IDs:** FR-PLAT-009

**Readiness / approval gate:** OTHER TEAM AND COORDINATOR DECISION

**Description and rationale:** Make authorized runtime information available for Team 4 investigation.

**Expected files or components:** M07; proposed selected telemetry adapter

**Inputs:** Approved service/time scope and source query/event

**Outputs:** Bounded provenance-bearing telemetry envelope

**Required behavior:** Implement only selected provider capability; Team 4 interprets/normalizes; no generic arbitrary query interface.

**Error handling:** Empty, partial, failed and unknown mapping states distinct.

**Security checks:** Check data/resource permission before fetch; enforce egress and redaction.

**Dependencies:** Q05/Q06/Q10/Q13; CT-04; T11/T12/T13

**Acceptance criteria:** AC-PLAT-009; Bounded provenance-bearing telemetry envelope must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-009 query bounds and Team 4 contract

**Priority:** P1

**Suggested owner:** Sharanbasava

**Review requirements:** Team 4 lead reviews evidence meaning; coordinator resolves service owner

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T29 - Implement synthetic evaluation runner

**Task ID:** T29

**Requirement IDs:** FR-PLAT-015

**Readiness / approval gate:** OTHER TEAM

**Description and rationale:** Make domain quality changes assessable, especially RCA grounding and change intelligence.

**Expected files or components:** M12; proposed case runner/result schema

**Inputs:** Versioned synthetic cases and domain scoring rubric

**Outputs:** Case/run outcomes with versions, latency, cost and incomplete flags

**Required behavior:** Start one deterministic case; expand reviewed corpus; no automatic promotion.

**Error handling:** Provider failure unevaluated/failed, never passed.

**Security checks:** Dataset authorization and synthetic data by default; no unapproved production samples.

**Dependencies:** Q12 domain rubric and dataset; Q10 retention; T18/T19/T22

**Acceptance criteria:** AC-PLAT-015; Case/run outcomes with versions, latency, cost and incomplete flags must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-015 reproducibility/partial-run/dataset access

**Priority:** P1

**Suggested owner:** Sharanbasava with domain evaluator

**Review requirements:** Team 3/4 owns expected results and rubric; Sagar reviews framework

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T30 - Specify and implement selected notification delivery

**Task ID:** T30

**Requirement IDs:** FR-PLAT-016

**Readiness / approval gate:** COORDINATOR DECISION

**Description and rationale:** Decouple domain workflows and expose important changes without duplicating business logic.

**Expected files or components:** M03; proposed notification adapter only after channel selection

**Inputs:** Authorized event, eligible recipient and delivery preferences

**Outputs:** Notification delivery state and safe content

**Required behavior:** First review must define channel and recipient authorization; implementation limited to accepted channel.

**Error handling:** Recipient invalid/ineligible means no send; retry boundedly for transient delivery failure.

**Security checks:** Recheck tenant and resource visibility; suppress sensitive raw payloads.

**Dependencies:** Q11/Q13 channel/recipients/preferences/ownership; T26

**Acceptance criteria:** AC-PLAT-016; Notification delivery state and safe content must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-PLAT-016 recipient/tenant/preference/retry cases

**Priority:** P1

**Suggested owner:** Varshini

**Review requirements:** Coordinator accepts product behavior; Team 1/2/4 affected owner and Sagar review

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T31 - Run integration and AI failure acceptance

**Task ID:** T31

**Requirement IDs:** FR-REL-001, FR-PLAT-007, FR-PLAT-012

**Readiness / approval gate:** OTHER TEAM

**Description and rationale:** Avoid lost acknowledged work and duplicated external/domain side effects. Give Team 3 normalized provider data and Team 4 approved change/deployment context. Reuse safe execution infrastructure without centralizing domain intelligence in Team 5.

**Expected files or components:** tests/integration and runbook evidence (proposed)

**Inputs:** Real agreed test environment plus provider/domain fault controls

**Outputs:** E2E-01/02/03 results and defect list

**Required behavior:** Test crash/retry/revoke/disconnect and injection across actual service boundaries; fixture-only results remain labeled.

**Error handling:** Open defect or unavailable real dependency blocks integrated completion.

**Security checks:** Cross-tenant and approval bypass failures are release blockers.

**Dependencies:** Release-scope implementations; accepted CT-01/03/04/06/07; Q09 limits

**Acceptance criteria:** AC-REL-001, AC-PLAT-007, AC-PLAT-012; E2E-01/02/03 results and defect list must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** E2E-01/02/03 and TC-REL-001

**Priority:** P0

**Suggested owner:** Sagar with shared QA

**Review requirements:** Each consumer lead witnesses relevant chain; QA and Sagar review evidence

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T32 - Review and implement approved schema slice

**Task ID:** T32

**Requirement IDs:** FR-DATA-001

**Readiness / approval gate:** OTHER TEAM AND INTERNAL DECISION

**Description and rationale:** Reconcile ERD overlap and keep cross-team provenance consistent.

**Expected files or components:** M02/M04; proposed models/migrations for selected slice

**Inputs:** Approved entity/constraint subset and logical references

**Outputs:** Reviewed migration plus integrity tests

**Required behavior:** Approve and migrate one bounded slice at a time; do not create every proposed table or cross-team FK automatically.

**Error handling:** Migration/reference conflicts halt; no silent data coercion.

**Security checks:** Tenant composite constraints and least-privilege DB role; no duplicated core entities.

**Dependencies:** Q02/Q03/Q04/Q15; relevant domain contract; no blanket ERD approval

**Acceptance criteria:** AC-DATA-001; Reviewed migration plus integrity tests must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-DATA-001 uniqueness/reference/deletion/migration tests

**Priority:** P0

**Suggested owner:** Sagar with Varshini

**Review requirements:** Technical lead and affected owner lead review; Sagar signs schema proposal

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T33 - Prepare deployment and operational runbook

**Task ID:** T33

**Requirement IDs:** FR-OPS-001

**Readiness / approval gate:** COORDINATOR DECISION

**Description and rationale:** Make a small team able to deploy and recover the shared platform without undocumented procedures.

**Expected files or components:** M01; proposed deploy configuration and docs/runbook.md

**Inputs:** Accepted hosting/config/secrets/limits and release artifact

**Outputs:** Reproducible deployment, migration and rollback instructions

**Required behavior:** Separate dev/test/shared environments; migration precedes readiness; document alert owner and response for backlog/credential/AI failure.

**Error handling:** Failed migration/readiness halts traffic; no destructive rollback assumption.

**Security checks:** Restricted deployment identity, TLS/secrets and redacted health checks.

**Dependencies:** Q03/Q09/Q10/Q14 environment/support/backup decisions; T04/T05

**Acceptance criteria:** AC-OPS-001; Reproducible deployment, migration and rollback instructions must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** TC-OPS-001 clean deployment and migration-failure rehearsal

**Priority:** P0

**Suggested owner:** Sagar

**Review requirements:** Technical lead and operational owner review; coordinator accepts support responsibility

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

### T34 - Rehearse restore and release acceptance

**Task ID:** T34

**Requirement IDs:** FR-OPS-001

**Readiness / approval gate:** COORDINATOR DECISION

**Description and rationale:** Make a small team able to deploy and recover the shared platform without undocumented procedures.

**Expected files or components:** M01; proposed recovery evidence and release checklist

**Inputs:** Isolated backup, compatible release and queued/unknown jobs

**Outputs:** Restore/reconciliation evidence and release decision packet

**Required behavior:** Measure restore against accepted targets; prevent external dispatch until reconciliation; verify all release requirements and exclusions.

**Error handling:** Missing target or unresolved critical dependency remains release-blocking, not passed.

**Security checks:** Verify tenant/access/audit integrity after restore; secrets restored through approved process.

**Dependencies:** T31/T33; Q09/Q14 accepted SLO/RPO/RTO and release criteria

**Acceptance criteria:** AC-OPS-001; Restore/reconciliation evidence and release decision packet must be demonstrable with the named tests; unresolved prerequisites prevent integrated completion.

**Tests:** E2E-04; TC-OPS-001; relevant TC-REL-001 replay checks

**Priority:** P0

**Suggested owner:** Sagar with shared QA

**Review requirements:** Coordinator/release owner decides release; no approval claimed by this task

**Reviewer completion evidence:** accepted contract/design versions, focused diff, fixture and real-integration distinction, recorded test outcomes, sanitized diagnostic example and remaining-risk disposition.

## 4. Requirements-to-task coverage

The PRD traceability table is the master mapping. This index supports task selection; repeated requirements intentionally span small changes. No task completion is asserted.

| Requirement | Tasks | Verification |
|---|---|---|
| FR-PLAT-001 | T04, T05 | TC-PLAT-001 and AC-PLAT-001 |
| FR-PLAT-002 | T01, T06 | TC-PLAT-002 and AC-PLAT-002 |
| FR-PLAT-003 | T01, T07, T24 | TC-PLAT-003 and AC-PLAT-003 |
| FR-PLAT-004 | T02, T08 | TC-PLAT-004 and AC-PLAT-004 |
| FR-PLAT-005 | T03, T09, T10 | TC-PLAT-005 and AC-PLAT-005 |
| FR-PLAT-006 | T02, T11, T13 | TC-PLAT-006 and AC-PLAT-006 |
| FR-PLAT-007 | T02, T14, T15, T31 | TC-PLAT-007 and AC-PLAT-007 |
| FR-PLAT-008 | T27 | TC-PLAT-008 and AC-PLAT-008 |
| FR-PLAT-009 | T28 | TC-PLAT-009 and AC-PLAT-009 |
| FR-PLAT-010 | T17, T18, T19 | TC-PLAT-010 and AC-PLAT-010 |
| FR-PLAT-011 | T20 | TC-PLAT-011 and AC-PLAT-011 |
| FR-PLAT-012 | T02, T22, T23, T31 | TC-PLAT-012 and AC-PLAT-012 |
| FR-PLAT-013 | T21, T24 | TC-PLAT-013 and AC-PLAT-013 |
| FR-PLAT-014 | T19, T25 | TC-PLAT-014 and AC-PLAT-014 |
| FR-PLAT-015 | T29 | TC-PLAT-015 and AC-PLAT-015 |
| FR-PLAT-016 | T26, T30 | TC-PLAT-016 and AC-PLAT-016 |
| FR-SEC-001 | T12 | TC-SEC-001 and AC-SEC-001 |
| FR-SEC-002 | T16 | TC-SEC-002 and AC-SEC-002 |
| FR-SEC-003 | T03, T23 | TC-SEC-003 and AC-SEC-003 |
| FR-REL-001 | T03, T13, T26, T31 | TC-REL-001 and AC-REL-001 |
| FR-DATA-001 | T01, T08, T15, T32 | TC-DATA-001 and AC-DATA-001 |
| FR-OPS-001 | T03, T33, T34 | TC-OPS-001 and AC-OPS-001 |


## 5. Evidence required before marking a task ready or done

Gate record: question/ADR and contract version, actual decision, approving role/person, decision date, allowed scope, and impacted tasks. A proposed recommendation or an unanswered review request is not a gate record. Sagar should update the question register and linked requirements together after approval.

Completion record: task ID, requirement/acceptance IDs, review link, implementation/migration version, test command/results, relevant integration participant, runbook/config evidence and residual issue disposition. Component completion with fakes is useful progress but cannot satisfy E2E-01/02/03. Retain blocked status for live identity, canonical ingest, approval or provider configuration when those dependencies are missing.

Recommended next action for Sagar: use T01/T02 to resolve the Team 1 authentication handoff and CT-01 identity/tenant contract, then agree CT-03 canonical engineering ingest and the first read-only GitHub/AI slice. These choices unblock the largest number of tasks without approving every proposed ERD table or all 16 source modules at once.
