# Nexora Team 5 - API and cross-team contract proposals

Version 0.1 | Updated 2026-10-27 | Owner: Sagar | Status: **PROPOSED; no cross-team approval or deployed API is claimed**

Related: [PRD](PRD.md), [architecture](architecture.md), [database](database-schema.md), [security](security.md), [questions](open-questions.md), [implementation plan](implementation-plan.md).

This document separates **source-specified paths** from new **proposed interfaces**. A path in a PDF is an interface intention, not evidence of an implemented service, accepted payload schema or available environment. All JSON, permission names beyond source examples, status semantics, internal endpoints and version conventions below are proposed examples requiring provider/consumer agreement. The existing source filenames and sections are cited in each contract. Example IDs are opaque strings and illustrative; Q02 must resolve UUID versus display-code conventions.

## Contract register

| ID | Provider / consumers | Scope and requirements | Status / acceptance owners |
|---|---|---|---|
| CT-01 | Team 1 / Teams 2-5 | Identity, organization membership, permission/delegation and lifecycle; FR-PLAT-002..004, FR-DATA-001 | OPEN DECISION Q01/Q02; Avinash, Sagar, coordinator; current coordinator ownership supersedes older Team 5 authentication wording |
| CT-02 | Team 2 / Team 5, then Teams 3-4 | Canonical project/task context and external work import; FR-PLAT-008/012, FR-DATA-001 | PROPOSED Q02/Q04; Abhishek and Sagar |
| CT-03 | Team 3 / Team 5 and Team 4 | Engineering ingestion, identifiers and resource reads; FR-PLAT-007/011/012, FR-DATA-001 | PROPOSED Q02/Q04; Srushti and Sagar |
| CT-04 | Team 4 / Team 5 | Incident/evidence context, observability handoff, approval semantics; FR-PLAT-009/012/013 | PROPOSED Q04/Q05/Q08/Q10; Poonam and Sagar, coordinator for service ownership/autonomy |
| CT-05 | Team 5 / platform clients and teams | Health, connection management, sync status and common API conventions; FR-PLAT-001/006, FR-SEC-001/002, FR-REL-001 | PROPOSED payloads; source paths noted below; Sagar and consuming leads |
| CT-06 | All teams as producers; Team 5 infrastructure / subscribed teams | Audit intake/query and durable platform events; FR-PLAT-005/016, FR-REL-001 | PROPOSED Q10/Q11; Sagar plus producer/consumer leads |
| CT-07 | Team 5 / Teams 3-4 and authorized clients | Gateway, tool/agent registry, execution, policies, usage, evaluation hooks; FR-PLAT-010..015, FR-SEC-003 | PROPOSED Q07/Q08/Q12/Q13; Sagar, Srushti, Poonam |

## 1. Common wire conventions (PROPOSED)

- HTTPS only outside explicitly isolated local development. `Authorization: Bearer <credential>` represents the selected Team 1 identity protocol; it does not select JWT or permit trusting decoded claims. Internal calls also need verified workload identity and audience. User delegation and workload authority are independently checked.
- `/api/v1` is source-specified for listed public resources. Proposed internal paths use `/internal/v1`; network placement does not make a request trusted. Keep identity implementation with Team 1. Endpoint hosting/routing and service names require Q03.
- Tenant context is established by CT-01. `X-Organization-ID` may select among already-authorized organizations; it never grants membership. JSON organization_id must match validated context. Route IDs and resource ownership must also match. Webhooks derive tenant from verified connection binding, not this header.
- JSON UTF-8; timestamps use RFC 3339 with an explicit UTC offset. IDs are opaque strings; counters are nonnegative integers; costs are decimal strings with currency and provenance. Missing/unknown cost is null, never numeric zero. Boolean fields are actual booleans.
- Generate a request ID per hop and propagate a bounded validated correlation ID. Reject/replace invalid identifier input; log neither credentials nor sensitive request bodies. `traceparent` support is a tracing proposal requiring Q14.
- List response: `{items: [...], next_cursor: string|null}`. Cursor is opaque, bound to tenant/filter/sort. Stable ordering `(created_at,id)` proposed; page size defaults/maxima are Q09 decisions. Reject unrecognized filters and unbounded queries. Collections never leak cross-tenant counts.
- Request bodies reject unknown security-relevant fields and validate types, enum values, lengths, nested depth and total bytes. Document explicit extension fields rather than silently accepting arbitrary JSON. A model/tool result is validated again before use.
- Idempotent submission carries `Idempotency-Key`. Scope is tenant + authenticated actor type/ID + operation; hash the canonical request. Same key/body returns original receipt after current authorization, while different body returns 409. Retention horizon requires Q10; expired-key behavior must be explicit and clients must not blindly resubmit uncertain writes.
- PATCH operations use a revision precondition (`If-Match` proposed). Return 409 for an incompatible state or revision. Compatibility rules: additive optional response fields within version, no removal/meaning changes without major version or agreed migration; enum expansion is reviewed because exhaustive clients can break. Publish OpenAPI and event JSON schemas with fixtures in the repository; deprecation period is agreed, not invented.

### Error behavior

| HTTP status | Meaning | Caller behavior |
|---|---|---|
| 400 / 422 | Malformed request / semantically invalid schema | Correct input; no automatic retry |
| 401 | Identity missing/invalid/expired | Obtain valid Team 1 identity; no provider side effect |
| 403 | Authenticated but permission/policy denied | No retry until authority/policy changes |
| 404 | Missing or inaccessible scoped resource | Do not reveal a cross-tenant resource exists; audit reason privately |
| 409 | Idempotency collision, state or revision conflict | Re-read and explicitly reconcile; no blind overwrite |
| 413 | Body/context exceeds accepted limit | Reduce input |
| 429 | Rate, concurrency or approved budget limit | Use bounded retry only when safe, honoring Retry-After if supplied |
| 502 / 503 / 504 | Invalid provider response / dependency unavailable / deadline exceeded | Preserve request/receipt IDs; consult operation state before retrying possibly completed work |

An authorization dependency outage returns unavailable, never success and never a misleading permission denial. Network timeouts do not prove the provider did nothing. Proposed error response:

```json
{
  "error": {
    "code": "DEPENDENCY_UNAVAILABLE",
    "message": "Authorization could not be verified.",
    "request_id": "req-example-01",
    "correlation_id": "corr-example-01",
    "retryable": true
  }
}
```

`retryable` concerns the failed stage, not permission to repeat a side effect. Public responses omit raw provider errors, stack traces, secret references and sensitive metadata. Numeric timeout/retry/size/rate defaults require Q09; behavior must use finite configuration with startup validation.

## 2. CT-01 - Team 1 identity, tenant and authorization

**Evidence:** Coordinator context; `Detailed HRMS Organization ERD Schema.png` §§1-5; `Nexora_Team5_Platform_Integrations_AI_Spec.pdf` pp5-7,16,18,20; `Nexora_Team1_HRMS_Organization_Spec.pdf` pp5,14. These sources conflict on historical auth/RBAC ownership. Target ownership is Team 1; Team 5 provides consuming middleware and enforcement. No Team 5 login, password, token issuer, session, role or permission store is proposed.

**Source-specified paths requiring reassignment/routing agreement:** Team 5 PDF p16 lists POST `/api/v1/auth/login`, `/api/v1/auth/logout`, `/api/v1/auth/refresh`, GET `/api/v1/permissions` and `/api/v1/roles`; p18 gives abbreviated `/auth/login`, `/auth/refresh` and `check_permission(user_id, permission, resource)`. Team 1 PDF p5 specifies GET `/api/v1/organizations/{id}`. None is a finalized identity-validation contract. The two auth path forms must not become accidental parallel APIs.

### Required provider decisions

| Contract operation | Required data/behavior | Proposed boundary |
|---|---|---|
| Validate identity | Credential validity, issuer/audience, subject type/ID, organization membership, expiry/revocation and user status | Choose signed short-lived tokens with approved key discovery/revocation approach, or authoritative introspection. Team 1 owns choice and credentials. |
| Establish tenant | Requested organization is active and caller is an authorized member/delegate | No trust in organization_id supplied by the caller alone; no guessing org from employee prefix. |
| Authorize action | Exact subject, organization, action and owner-validated resource reference | Team 1 owns grants/RBAC; domain owner supplies resource existence/tenant/membership constraints. Effective authorization is intersection, not union. |
| Authenticate service | Issuer/trust root, workload principal, audience, allowed operation and tenant scope | A worker service token does not automatically inherit every user's access. |
| Delegate/background work | Initiating subject, delegation reference/expiry, permitted resource scope; revalidation on dispatch/resume | Store identity reference/decision provenance, never a bearer token in job rows. Scheduled connector authority is explicit service delegation, not a forgotten user's session. |
| Lifecycle | Organization/user deactivation, membership removal, permission revision and deletion | Authenticated events plus authoritative checks/invalidation; stale cached positive decisions cannot bypass revocation policy. |

Proposed normalized **server-side context**, produced by the trusted Team 1 adapter; this is not accepted verbatim from public JSON:

```json
{
  "principal": {"type": "user", "id": "user-example-01"},
  "organization_id": "org-example-01",
  "employee_id": "employee-example-09",
  "workload_id": "team5-api",
  "delegation_ref": null,
  "authorization_revision": "revision-example-3",
  "validated_at": "2026-10-27T08:00:00Z"
}
```

Proposed authorization operation: `authorize(subject, organization, action, resource, delegation)`; illustrative transport POST `/internal/v1/authorization/decisions` requires Team 1 agreement. Resource facts come from owning service, not a caller-provided assertion. Example request and response:

```json
{
  "subject": {"type": "user", "id": "user-example-01"},
  "organization_id": "org-example-01",
  "action": "integration.manage",
  "resource": {"owner_team": "team5", "type": "integration", "id": "connection-example-01"},
  "delegation_ref": null
}
```

```json
{
  "decision": "allow",
  "decision_id": "decision-example-01",
  "authorization_revision": "revision-example-3",
  "reason_code": "GRANT_AND_RESOURCE_SCOPE_MATCH"
}
```

The response schema also permits `deny`; transport failure is distinct and fails closed. No caching lifetime is implied. Service identity does not allow choosing arbitrary subject IDs; the endpoint authenticates that the caller may request/check that delegation. Cross-tenant resource discovery uses sanitized 404 or agreed non-disclosing failure. Health checks have separately approved exposure rules.

**Failure/retry/observability:** Retry a read-only validation only within the caller deadline and Q09 configuration; no protected business call proceeds on failure. Record decision ID/revision, tenant, action, request/correlation IDs and outcome without tokens. Revoked authority at execution causes cancellation/denial; do not continue using admission-time permission. Tests: forged/wrong-audience/expired identities; employee/user confusion; inactive tenant; missing delegation; membership removed between enqueue and dispatch; unavailable Team 1; shared-pool cross-tenant requests.

**Open decisions:** Q01/Q02/Q03/Q08/Q10. Avinash/Sagar/coordinator must sign the trust model, identifier semantics, permission vocabulary, workload/delegation protocol, revocation maximum and service routing before production integration. Contract fixtures may be written now.

## 3. CT-02 - Team 2 project/task context and imports

**Evidence:** `Nexora_Team2_Task_Project_Management_Spec.pdf` pp6,8,16; Team 2 ERD §§1-9; Team 5 PDF pp9-10,13. **System of record:** Team 2. Team 5 owns connection/mapping/checkpoint; it neither stores a second editable task nor applies Team 2 workflow transitions itself.

**Source-specified reads:** GET `/api/v1/projects/{id}`, `/api/v1/projects/{id}/members`, `/api/v1/projects/{id}/tasks`, `/api/v1/tasks/{id}`. The PDF also defines create/update/delete paths, but their existence does not authorize an external connector to call unrestricted task CRUD. An import operation is a new agreement.

| Flow | Proposed contract | Security and failure behavior |
|---|---|---|
| Team 5 context builder -> Team 2 | Owner-authorized project/task read, returning canonical ID, org/project relation, permitted intent/outcome and resource revision | Delegated caller + service identity; Team 2 checks actual resource access. Missing/forbidden context is marked unavailable, not fabricated. |
| PM connector -> Team 2 | Proposed POST `/internal/v1/work-items/import`; one normalized item, stable source key and delivery key | Connection's tenant/service grant plus approved import scope; Team 2 validates status/assignee/project and decides canonical create/update. |
| Team 2 -> shared events | Project/task change envelope via CT-06 | Team 2 is authenticated producer; resource ownership is not established by arbitrary event payload. |

Proposed import request:

```json
{
  "schema_version": "1",
  "organization_id": "org-example-01",
  "connection_id": "connection-example-02",
  "delivery_id": "delivery-example-02",
  "source": {"provider": "jira", "namespace": "external-project-example", "entity_type": "work_item", "external_id": "external-item-42", "revision": "source-revision-7"},
  "target_project_id": "project-example-01",
  "item": {"title": "Example imported task", "description": "Sanitized source text", "external_status": "In Progress", "external_assignee_id": "external-person-8"},
  "observed_at": "2026-10-27T08:10:00Z"
}
```

Proposed durable acknowledgment:

```json
{
  "receipt_id": "receipt-example-02",
  "delivery_id": "delivery-example-02",
  "status": "applied",
  "canonical": {"owner_team": "team2", "type": "task", "id": "task-example-01", "organization_id": "org-example-01", "revision": "task-revision-4"},
  "warnings": ["ASSIGNEE_UNRESOLVED"]
}
```

`applied` is returned only after Team 2 commits the canonical mutation and dedupe receipt. Alternative statuses: `duplicate` returns the same canonical result; `ignored_stale` returns current revision; invalid mapping returns a typed failure and no checkpoint advance. If Team 2 chooses asynchronous admission, `accepted`/202 needs a durable receipt-status interface; Team 5 cannot treat admission as canonical completion. Recommend synchronous per-item durable acknowledgment first, with batching only after measured need.

**Validation:** External project mapping must resolve to an accessible same-tenant Team 2 project. Do not infer assignee by email; unresolved external author/assignee remains explicit. Team 2 owns status mapping, conflict precedence, native-edit preservation, deletion/archive semantics, epic/subtask mapping, and repeated/out-of-order revisions. Proposed initial direction is import-only; bidirectional writes require separate approval. A source timestamp is not always a total order; where version ordering is unavailable, fetch current provider state and reconcile using the adapter's documented rule.

**Failure/retry/observability:** Retry retryable transport/429/5xx with the same delivery/idempotency key within policy. Validation/403/conflict pauses or quarantines the item; do not skip it silently. Parent project unresolved means no child task creation. Report connection/job/delivery/receipt IDs and accepted/rejected counts; payload text is not logged. CT-06 events are at least once. Tests include duplicate import, changed body same key, same external ID in two connections, missing project, unresolved assignee, stale source revision and timeout after canonical commit.

**Open decisions:** Q02/Q04/Q06/Q10/Q13; Abhishek/Sagar with Avinash for actor mapping. No provider subset, sync direction or business-field mapping is approved by listing Jira/Linear/Azure DevOps as targets.

## 4. CT-03 - Team 3 canonical engineering handoff

**Evidence:** `Nexora_Team3_Engineering_Productivity_Change_Intelligence_Spec.pdf` pp6-8,15,17,20; Team 3 ERD §§1-8; Team 5 PDF pp9-10. **System of record:** Team 3 for repositories, branches, commits, pull requests, builds and deployments; Team 5 for provider connection, ingestion transport, external bindings and sync status. Team 3 owns engineering analysis and task-code relations.

**Source-specified reads:** GET `/api/v1/repositories`, `/api/v1/repositories/{id}`, `/api/v1/projects/{project_id}/repositories`. No source establishes a canonical ingest endpoint. Proposed POST `/internal/v1/engineering/import` uses owner-approved tagged record schemas. Proposed read operations for PR/diff/build/deployment require Team 3 agreement; tool names such as `get_pull_request` are capabilities, not proof of HTTP endpoints.

Proposed one-record handoff:

```json
{
  "schema_version": "1",
  "organization_id": "org-example-01",
  "connection_id": "connection-example-01",
  "delivery_id": "delivery-example-03",
  "source": {"provider": "github", "account_id": "installation-example", "entity_type": "pull_request", "external_id": "provider-pr-42", "parent_external_id": "provider-repository-17", "revision": "provider-revision-8"},
  "references": {"project_id": "project-example-01", "repository_id": "repository-example-01"},
  "record": {"title": "Example change", "state": "open", "source_branch": "feature/example", "target_branch": "main", "head_commit_sha": "example-opaque-sha", "external_author_id": "provider-person-3"},
  "observed_at": "2026-10-27T08:20:00Z"
}
```

Proposed acknowledgment:

```json
{
  "receipt_id": "receipt-example-03",
  "delivery_id": "delivery-example-03",
  "status": "applied",
  "canonical": {"owner_team": "team3", "type": "pull_request", "id": "pull-request-example-01", "organization_id": "org-example-01", "revision": "pr-revision-8"}
}
```

The opaque SHA placeholder is illustrative, not a valid production hash. Record variants must have separate schemas for repository/branch/commit/PR/build/deployment; a catch-all unvalidated record is prohibited. Team 3 approves required fields, parent ordering, branch identity/rewrite behavior, optional build/deployment availability, timestamps, author mapping, deleted resources and stale revision handling. Provider absence of deployment data is `not_available`, not a fabricated deployment record. Unknown parent mapping is retried/quarantined and never used to bypass tenant validation.

**Authorization:** Team 5 authenticates the installation/credential, provider event and allowlisted repository; CT-01 authenticates workload/delegation. Team 3 validates project/repository organization and permitted import scope before canonical writes. Context/tool reads independently check the effective user's resource permission; possession of connector credentials is not permission to expose all connected repositories. Domain tool handlers may call Team 3 canonical APIs or approved scoped connector fetches, but they use the same resource grant and provenance.

**Retries and durability:** CT-02 acknowledgment rules apply. Team 5 advances checkpoint only after canonical commit acknowledgment. Stable key survives a worker crash; Team 3's dedupe receipt survives its own restart. A stale worker lease cannot commit a new checkpoint. Provider rate limits use bounded backoff/Retry-After where provided; unsupported event types produce an explicit ignored outcome. Reconciliation fetches current source state to repair missing/out-of-order webhooks. No exactly-once claim.

**Observability/tests:** Trace provider delivery -> inbox -> job -> canonical receipt -> event -> analysis request. Counts distinguish fetched, applied, duplicate, stale, rejected and unavailable. Test two tenants with same provider IDs, parent absent, duplicate PR webhook, reordered update/close, invalid signature, revoked repository access, partial pagination, downstream unavailable and crash after Team 3 commit. Repository/import APIs are contract-blocked until Srushti/Sagar accept Q02/Q04/Q06; Q05 concerns service links, not Team 3's confirmed Build/Deployment ownership.

## 5. CT-04 - Team 4 incident/evidence/approval boundary

**Evidence:** `Nexora_Team4_Incident_RCA_Spec.pdf` pp5-6,8,12-14,18; Team 4 ERD §§1-8; Team 5 PDF pp10,13-14,20,23. **System of record:** Team 4 for incidents, evidence, investigations, findings, fix proposals, validation results and domain review decisions. Team 5 supplies connector transport, governed runtime, technical execution and audit infrastructure.

**Source-specified paths:** GET `/api/v1/incidents/{id}`, `/api/v1/incidents/{id}/evidence`, `/api/v1/incidents/{id}/timeline`, `/api/v1/incidents/{id}/rca`, `/api/v1/incidents/{id}/related-changes`; incident POST/PATCH also specified. Source pp6,8 assigns incident normalization and evidence correlation to Team 4. Shared transport normalization in Team 5 does not transfer business interpretation.

| Flow | Proposed interface | Required behavior |
|---|---|---|
| Observability -> Team 4 | POST `/internal/v1/incidents/import` with verified provider envelope | Team 4 decides canonical incident creation, severity/status mapping, dedupe and ownership; Team 5 does not invent incident severity. |
| Team 4 -> connector | `fetch_telemetry(source_ref, scope, time_range, continuation)` operation; endpoint undecided | Validate resource scope/tenant/provider and query limits; return source attribution, explicit partial/unavailable/empty states. No arbitrary URL or provider query from model output. |
| Runtime -> Team 4 | Authorized evidence/context reads by incident/evidence ID and revision | Team 4 filters data to user and classifies/redacts it before provider disclosure; Team 5 applies its own data policy and context bounds. |
| Team 4 -> CT-07 | Invoke approved agent with incident/evidence references | Team 4 owns RCA/fix/test logic and persists domain result; Team 5 returns runtime state/output provenance. |
| Runtime -> authoritative approval | `claim_approval` / status/revocation semantics, transport unresolved | Must bind exact tenant, principal, tool version, arguments, resource revision, policy and expiry. A review record alone is insufficient. |

Proposed incident transport envelope:

```json
{
  "schema_version": "1",
  "organization_id": "org-example-01",
  "connection_id": "connection-example-03",
  "delivery_id": "delivery-example-04",
  "source": {"provider": "sentry", "external_id": "source-incident-9", "revision": "source-revision-2"},
  "service_ref": null,
  "observation": {"external_title": "Sanitized example failure", "external_severity": "error", "occurred_at": "2026-10-27T08:30:00Z"},
  "mapping_status": "service_unresolved"
}
```

Team 4 may reject this until service mapping is supplied, or accept an explicitly unmapped incident if its business rules allow it. That is Q05/CT-04 agreement, not a default inferred from a nullable example. Acknowledgment uses the same receipt/applied/duplicate/ignored_stale semantics as CT-03 and returns canonical incident ID only after Team 4 durable processing.

Proposed evidence/context response:

```json
{
  "incident_id": "incident-example-01",
  "organization_id": "org-example-01",
  "revision": "incident-revision-4",
  "context_status": "partial",
  "items": [{"evidence_id": "evidence-example-01", "type": "deployment", "owner_team": "team3", "resource_id": "deployment-example-01", "source_revision": "deployment-revision-2", "classification": "internal", "summary": "Authorized sanitized deployment summary"}],
  "missing_sources": [{"source_kind": "trace", "reason_code": "DEPENDENCY_UNAVAILABLE"}]
}
```

Partial evidence cannot be silently promoted to a complete investigation. Model conclusions distinguish evidence, inference and unknown per overview p13 §9. The reference string is not an unrestricted download URL. Read authorization must be repeated for the output consumer, not only the initiator, and source redaction does not eliminate policy checks at provider dispatch.

### Approval proposal and concurrency boundary

Example authoritative approval claim result; it is not a model-generated object:

```json
{
  "approval_ref": "review-example-01",
  "approval_version": "review-revision-3",
  "organization_id": "org-example-01",
  "principal": {"type": "user", "id": "user-example-01"},
  "tool": {"name": "create_pull_request", "version": "tool-version-1"},
  "arguments_digest": "sha256-example-arguments",
  "resource_revision_digest": "sha256-example-resource-revisions",
  "policy_version": "policy-version-2",
  "expires_at": "2026-10-27T09:00:00Z",
  "claim_id": "claim-example-01",
  "status": "claimed"
}
```

**OPEN DECISION Q08:** Recommend an authoritative compare-and-set claim that checks approval validity and revocation, with a claim ID bound to one execution. Team 5 then durably records a one-use `approval_binding` and execution intent. This sequence is not a distributed atomic transaction. A crash after remote claim but before local recording requires querying the same claim and recovering the binding, not issuing a second claim. Local claim-before-send prevents local duplicate dispatch, but cannot make a network side effect atomic or eliminate the authority/revocation race. Define whether revocation is permitted after claim, its execution lease/expiry, recovery and maximum claim-to-dispatch delay; until agreed, write tools stay disabled.

Recheck identity/resource/policy/tool enablement just before dispatch; an approval cannot grant a missing permission. Unknown external write outcome prevents automatic replay. Team 4 approves domain remediation; Team 1 provides approver authority; Team 5 verifies and enforces technical binding. Non-RCA write approval authority remains a coordinator decision rather than defaulting to Team 4. Automatic production deploy/merge is not enabled by these examples.

**Failure/retry/tests:** Retry safe telemetry reads within bounds; distinguish no results from provider outage/denial. Evidence content is not copied into logs. Test unavailable source, permission removed before context use, same incident ID across tenants, malicious log instructions, stale/expired/revoked/mismatched approval, two concurrent claimants, crash around claim/dispatch and unknown side-effect reconciliation. Poonam/Sagar must resolve Q04/Q05/Q08/Q10; coordinator decides enabled autonomy and service authority (Q13).

## 6. CT-05 - Team 5 public foundation and integration APIs

**Evidence:** Team 5 PDF pp5,9-10,16. The following paths are source-specified; behavior and schemas are proposed.

| Method/path | Proposed permission and request | Proposed success / failure semantics |
|---|---|---|
| GET `/health` | Exposure policy Q14; no secret input | 200 process alive; no provider checks or configuration disclosure |
| GET `/ready` | Restricted detailed health recommended | 200 compatible schema/mandatory local dependencies ready; 503 otherwise; external provider degradation reported separately |
| GET `/version` | Exposure policy Q14 | 200 release identifier only |
| GET `/api/v1/integrations` | Tenant-scoped read grant; cursor/provider/state filters | 200 sanitized list; no credential reference/value |
| POST `/api/v1/integrations` | `integration.manage` example; provider key, approved config, credential binding reference | 201 connection receipt in pending/active state; validation and credential testing outcomes explicit |
| GET `/api/v1/integrations/{id}` | Same-tenant read grant | 200 sanitized state/revision/health; unauthorized cross-tenant 404 |
| POST `/api/v1/integrations/{id}/sync` | Same-tenant sync grant; idempotency key; bounded scope | 202 durable queued job with status URL; never claims sync completed |
| DELETE `/api/v1/integrations/{id}` | Manage grant + revision precondition | 202 if asynchronous disconnect; 204 only after disable/cancellation/revocation policy completed; repeat safe |

Additional proposed endpoints needed to observe/operate the above lifecycle: GET `/api/v1/integrations/{id}/sync-jobs/{job_id}`; POST `/api/v1/integrations/{id}/sync-jobs/{job_id}/cancel`; POST `/api/v1/integrations/{id}/disconnect` if DELETE's lifecycle interpretation is rejected; POST `/api/v1/webhooks/github/{connection_id}` as an illustrative callback path, subject to provider mode and routing. These additions require Sagar's API review. Credential setup/callback routes are provider-specific decisions; no generic arbitrary secret-writing API is assumed.

Proposed sync request body and receipt:

```json
{"scope": {"entity_types": ["repository", "pull_request"], "repository_ids": ["repository-example-01"]}, "mode": "incremental"}
```

```json
{
  "job_id": "job-example-01",
  "connection_id": "connection-example-01",
  "status": "queued",
  "status_url": "/api/v1/integrations/connection-example-01/sync-jobs/job-example-01",
  "request_id": "req-example-05"
}
```

Proposed status response:

```json
{
  "job_id": "job-example-01",
  "status": "retry_wait",
  "attempt": 2,
  "accepted_count": 12,
  "rejected_count": 0,
  "next_attempt_at": "2026-10-27T08:45:00Z",
  "error_code": "CANONICAL_SERVICE_UNAVAILABLE",
  "correlation_id": "corr-example-05"
}
```

State vocabulary matches [database state machines](database-schema.md). Scope always intersects connection allowlist and current actor/service authority. Initializer identities are retained as references for reauthorization; a background worker cannot inherit a client-selected actor string. Status reads are tenant/permission checked. Cancel stops new work; in-flight external calls may finish and their outcomes must be recorded. Retry never resets accepted counts/checkpoints or repeats an uncertain write without reconciliation.

**Webhook protocol proposal:** Adapter verifies provider signature/authenticity on raw bounded bytes using the connection's secret/version, checks delivery identity and installation/resource binding, inserts inbox/job durably, then returns a provider-compatible success. Invalid auth rejects; unavailable durable store returns retryable failure; duplicate same event returns prior receipt; key/digest collision quarantines. Signature algorithm/headers/timestamp support are provider-specific and must be verified against current provider documentation during connector implementation. A verified webhook may authorize ingestion only, not a user or arbitrary AI action.

**Open decisions and tests:** Q03/Q06/Q09/Q10/Q14/Q15. Test exposure/redaction, unhealthy readiness, invalid config, secret-ref tenant mismatch, sync queue persistence, duplicate key/body mismatch, job permission revocation, disconnect during worker execution, webhook validation and 429/5xx recovery. Provider capability registration supports the source methods authenticate/connect/disconnect/health_check/sync/fetch/handle_webhook; unsupported capabilities return typed unsupported results rather than fake success.

## 7. CT-06 - audit and platform events

**Evidence:** Team 5 PDF pp8,16,18; source event names are examples. Source-specified GET `/api/v1/audit/events`; proposed POST `/internal/v1/audit/events` and POST `/internal/v1/events` for authenticated service producers. No event broker, subscription API, user channel or existing endpoint is confirmed.

Audit envelope proposal:

```json
{
  "schema_version": "1",
  "producer": "team5",
  "producer_event_id": "audit-example-01",
  "organization_id": "org-example-01",
  "actor": {"type": "user", "id": "user-example-01"},
  "action": "AI_TOOL_EXECUTION",
  "resource": {"owner_team": "team3", "type": "pull_request", "id": "pull-request-example-01"},
  "outcome": "denied",
  "reason_code": "PERMISSION_DENIED",
  "occurred_at": "2026-10-27T08:50:00Z",
  "request_id": "req-example-06",
  "correlation_id": "corr-example-06",
  "metadata": {"tool_name": "get_pull_request", "tool_version": "tool-version-1"}
}
```

Authenticated producer identity must match producer and be authorized to publish for the tenant/actor/resource scope. Actor assertions are provenance attributed to the producer, not automatic impersonation authority. Missing tenant for unauthenticated security events needs a separate restricted system stream contract; never insert such events into a guessed customer's audit history. Metadata uses event-type allowlists and redaction; tokens, keys, raw prompts, full code/diffs, personal evidence and unnecessary IP data are excluded.

Platform business-event proposal:

```json
{
  "event_id": "event-example-01",
  "schema_version": "1",
  "producer": "team3",
  "organization_id": "org-example-01",
  "event_type": "PR_CREATED",
  "subject": {"type": "pull_request", "id": "pull-request-example-01", "revision": "pr-revision-1"},
  "occurred_at": "2026-10-27T08:50:00Z",
  "correlation_id": "corr-example-06",
  "causation_id": "delivery-example-03",
  "payload": {"repository_id": "repository-example-01", "project_id": "project-example-01"}
}
```

The producer commits its domain change and local outbox atomically. Team 5 accepts only after durable storage, returning a receipt; consumers acknowledge only after their durable transaction and dedupe by producer/event/tenant identity. Delivery is at least once and not globally ordered. Consumers use resource revisions or read current state, never order solely by arrival timestamp. Retry transient failures with backoff/deadline/attempt limits; exhausted delivery is visible with authorized replay. Do not claim exactly-once or a distributed transaction across teams.

Audit is separate from notifications/business events: a missing subscriber must not erase the audit trail. For sensitive Team 5 mutations, local durable audit intent is part of the transaction; if it cannot be recorded, deny the mutation. For domain teams, publish policy must preserve durable local audit and surface backlog; centralized audit outage behavior must be agreed per event risk. An audit intent records attempted action; a later outcome records actual result. Do not label unconfirmed external success as succeeded.

GET audit supports approved tenant/time/action/resource/actor/outcome filters and cursor pagination. `audit.read` is a source example, but exact scope and export grants need Team 1 approval. Audit queries/exports are themselves security-audited where required by agreed policy. User notifications require Q11 recipient lookup, opt-in/preferences, channel, redaction, dedupe and delivery ownership; they are not automatically authorized by a business event.

**Compatibility/tests:** Schema registry may initially be repository files, not new infrastructure. Each event type has an owner, schema version and consumer list. Validate duplicate delivery, replay after crash, out-of-order events, oversized/sensitive metadata, fake producer, tenant mismatch, subscriber outage, retention purge and unauthorized audit export. Q10/Q11/Q14 gate release; consumers must agree replay horizon and idempotency retention.

## 8. CT-07 - AI gateway, registry and execution

**Evidence:** Team 5 PDF pp11-16,19-20,23; overview pp14-15. Source-specified paths: POST `/api/v1/ai/chat`, POST `/api/v1/ai/execute`, GET `/api/v1/ai/usage`, GET `/api/v1/ai/tools`, GET `/api/v1/ai/tools/{id}`. Agent registration, management, policy and evaluation endpoints are not specified. Initially propose reviewed configuration/registry migrations for management rather than inventing an unrestricted admin UI.

### 8.1 Gateway request and result proposal

The caller supplies purpose/model policy and permitted content; the server derives actor/organization and validates context references. It selects only approved providers/models and tenant credential bindings. Provider credentials never enter caller payloads, tool context or logs. A change of provider/model fallback requires explicit policy and data-transfer approval; no silent fallback.

```json
{
  "purpose": "rca_advisory",
  "model_policy": "approved-advisory-route",
  "prompt_version": "rca-prompt-version-1",
  "messages": [{"role": "user", "content": "Summarize the authorized evidence and identify unknowns."}],
  "context_refs": [{"owner_team": "team4", "type": "incident", "id": "incident-example-01", "revision": "incident-revision-4"}],
  "response_format": "structured"
}
```

Public callers cannot submit trusted system/developer instruction roles or arbitrary tool results. Domain agent configuration is a separately reviewed trust boundary. Input schemas distinguish trusted instruction configuration from untrusted task/code/log/evidence data. Context limits and allowed response schema are policy-selected, not model-determined.

```json
{
  "ai_request_id": "ai-request-example-01",
  "status": "succeeded",
  "model": {"provider": "approved-provider", "name": "approved-model", "version": "approved-version"},
  "result": {"summary": "Example advisory result", "evidence_refs": ["evidence-example-01"], "unknowns": ["Trace source unavailable"]},
  "usage": {"input_tokens": 120, "output_tokens": 45, "status": "reported", "estimated_cost": null, "currency": null, "cost_status": "price_unknown"},
  "correlation_id": "corr-example-07"
}
```

The numbers are test-fixture values, not limits or business targets. A response is untrusted advisory content; structured shape validation does not make its claims true. Domain teams validate meaning and evidence. Unknown token use after timeout remains unknown and may be reconciled; estimated price is not a provider invoice. Each send creates `ai_attempt`; one logical request can have multiple billable attempts only under approved retry policy.

For work exceeding the interactive deadline, proposed 202 receipt returns `ai_request_id`, `status` and a status URL. Proposed GET `/api/v1/ai/requests/{id}` exposes scoped state and sanitized results; an inaccessible request is not discoverable. Store a redacted response only under Q10-approved retention; if results are intentionally ephemeral, asynchronous execution must use a secure retained result reference for its advertised retrieval window. The API cannot promise later retrieval while retaining no result.

### 8.2 Registry and execution proposal

Tool read responses expose only tools the tenant may discover. Tool metadata contains name/version/description/input/output schemas/required permission/risk/audit requirement/operation kind. Registration is separate from enablement, and agent-tool membership is separate from user permission. Tool implementations are trusted compiled/deployed handlers identified by allowlisted key; registry JSON cannot install arbitrary code or URLs. Team 3/4 supplies domain agent version/prompt and approves tool needs; Team 5 manages execution infrastructure.

```json
{
  "agent": {"name": "rca_advisory", "version": "agent-version-1"},
  "context_refs": [{"owner_team": "team4", "type": "incident", "id": "incident-example-01", "revision": "incident-revision-4"}],
  "input": {"question": "Explain the available evidence and missing context."}
}
```

```json
{
  "run_id": "run-example-01",
  "status": "queued",
  "status_url": "/api/v1/ai/runs/run-example-01",
  "correlation_id": "corr-example-08"
}
```

Proposed GET `/api/v1/ai/runs/{id}` and POST `/api/v1/ai/runs/{id}/cancel` support observation/cancellation. Status reads check current authority to all output resources and apply redaction; a creator does not keep perpetual access after revocation. Proposed resume POST `/api/v1/ai/runs/{id}/resume` accepts an authoritative approval reference, not `approved:true`; enable only after CT-04/Q08. These are additions, not source-specified existing endpoints.

Run lifecycle: queued/running/awaiting_approval/succeeded/failed/cancelled. Individual tool executions additionally have unknown outcome. The run may fail with `TOOL_OUTCOME_UNKNOWN` while preserving the tool's unknown state for reconciliation. No new tool dispatch follows cancellation, denied context, exceeded steps/time/budget or revoked grant. Already-dispatched effects are not promised undone. Every step checks exact actor, tenant, delegation, agent/tool version, schema, resource, policy and approval. Approval reuse, argument/resource mutation and tool version changes are denied. All checks occur outside model generation.

Context from external documents/logs/code is untrusted. Injection detection may flag suspicious content but cannot replace deterministic authorization, allowlists, schema validation, egress controls and separation of data from instructions. The model cannot request more permissions, choose another tenant, fetch an arbitrary URL, disclose secrets, invoke an unregistered tool or bypass human review. Approved provider responses/tool results are still validated and sanitized before they become subsequent context.

### 8.3 Usage and evaluation

GET `/api/v1/ai/usage` accepts approved time/model/provider/agent filters and returns logical request count, physical attempt count, known tokens, number of unknown usage/cost attempts, estimated totals grouped by currency and price provenance. Tenant/user detail is permission-scoped. Do not sum measurement corrections twice or combine currencies. Budget reporting is confirmed as a capability; hard monetary caps, reservation algorithm, thresholds and rate-card governance are proposals under Q07.

Evaluation module receives approved case/version, domain owner, expected result/criteria, prompt/model version, actual result, latency and usage references. Team 3/4 owns correctness and evidence-grounding criteria. Evaluation fixtures are approved synthetic/redacted data; no unapproved production corpus export. Pass/fail/inconclusive semantics and numerical score ranges require Q12. No evaluation endpoint path is invented as approved; an internal batch runner can satisfy the initial infrastructure if accepted.

**Failure/retry/observability:** Known rejection before dispatch does not incur a provider attempt; record the denial/audit as appropriate. Provider timeout after dispatch is unknown, never zero-cost success. Retry/fallback requires policy, remaining deadline and safe semantics; future external write tools require explicit idempotency/reconciliation capability. Record request/run/attempt/tool/approval/policy/model/prompt/correlation IDs, timing and sanitized codes. Raw inputs/outputs stay out of routine logs. Tests cover malformed output, provider rejection/429/timeout, disabled model, unauthorized context, injection, unknown tool, tool-schema mismatch, revoked user, stale approval, duplicate execution, budget race if hard caps approved, duplicate usage correction and inaccessible stored result.

## 9. Contract acceptance and change procedure

For each CT contract, Sagar and the provider lead record the accepted version, exact schema/path/protocol, service authentication/delegation, tenant validation, resource permissions, required/optional fields, idempotency and order semantics, error taxonomy, limits, retention, test fixtures and rollout compatibility. Record approver/date only when actual approval occurs. Published contract tests run in both producer and consumer CI after approval; before that they are proposal fixtures, not production integration evidence.

A change requires an impact review of PRD requirement IDs, owning modules, migrations, consumers, security checks and tests. Contract tests must include positive, denied, malformed, duplicate, cross-tenant and dependency-failure cases. Prove at least one real access chain, GitHub-to-Team 3 handoff and governed advisory AI chain in an agreed environment before integrated feature completion. Scope approval and source confirmation are not substitutes for this verification.
