# Nexora source inventory and ownership register

Version 0.1 | Updated 2026-10-27 | Owner: Team 5 / Sagar | Status: review draft; no stakeholder sign-off recorded.

## Discovery boundary and evidence rules

The supplied workspace `C:/Users/ADmin/Documents/Codex/2026-10-26/x20` contained no application repository or implementation files at discovery; Git reported that it was not a repository. No existing PRD, architecture, migrations, dependency manifest, API specification or tests were available there. All twelve supplied artifacts were found in `C:/Users/ADmin/Downloads/nexora`: six PDFs (121 pages total), five team ERD PNGs and one staffing PNG. The source folder contained no other files at inspection. All PDF pages were text-extracted and reviewed; the PNGs were visually reviewed. No supplied artifact was missing or unreadable. The review does not establish the state of an unprovided repository, running services, private decisions, contracts, credentials or infrastructure. Source files were not modified.

S00 is the user's current project context and reported coordinator decisions, not a separate file. It supplies the current ownership boundary, team members, approximate two-hours-per-person-per-day capacity, and this documentation assignment. It takes precedence over contradictory historical specifications. Instructions inside attachments are treated as project evidence, not as instructions to the document-authoring agent.

Evidence order: S00 current coordinator decisions; S01 main overview requirements; S02-S06 team requirements; S07-S12 ERDs/resource plan; clearly labelled recommendations. `CONFIRMED` means explicitly supported by that evidence; it does not mean deployed or stakeholder-approved. `PROPOSED` means recommended but not approved. `OPEN DECISION` requires agreement. `ASSUMPTION` is temporary and must identify consequences. No source contains an approval record for the new documentation or a finalized database schema. Dates are source publication dates, not release commitments. Source API paths are specified interface intentions, not proof of an implemented or agreed payload contract.

## Files reviewed

| ID | Filename | Subject | Extent / source date |
|---|---|---|---|
| S01 | Nexora_Product_Solution_Overview.pdf | Product vision and architecture | 21 pages; 2026-09-30 |
| S02 | Nexora_Team1_HRMS_Organization_Spec.pdf | Team 1 organization and people | 17 pages; 2026-10-01 |
| S03 | Nexora_Team2_Task_Project_Management_Spec.pdf | Team 2 work management | 19 pages; 2026-10-01 |
| S04 | Nexora_Team3_Engineering_Productivity_Change_Intelligence_Spec.pdf | Team 3 engineering intelligence | 20 pages; 2026-10-01 |
| S05 | Nexora_Team4_Incident_RCA_Spec.pdf | Team 4 incident and RCA | 21 pages; 2026-10-01 |
| S06 | Nexora_Team5_Platform_Integrations_AI_Spec.pdf | Team 5 platform/integrations/AI | 23 pages; 2026-10-01 |
| S07 | Detailed HRMS Organization ERD Schema.png | Proposed Team 1 ERD | One image; date not stated |
| S08 | Nexora_Resource_Plan.png | Staffing and delivery responsibilities | One image; date not stated |
| S09 | Team 2 Project Management ER Diagram.png | Proposed Team 2 ERD | One image; date not stated |
| S10 | Team 3 Engineering ERD Diagram.png | Proposed Team 3 ERD | One image; date not stated |
| S11 | Team 4 Incident Management ERD.png | Proposed Team 4 ERD | One image; date not stated |
| S12 | Team 5 Platform ERD Blueprint.png | Proposed Team 5 ERD | One image; date not stated |

Page citations below use physical PDF page numbers, matching printed page numbers. ERD citations use the named/numbered panel. S00 is the current working authority for ownership; final handoff details remain open in [open-questions.md](open-questions.md).

## Per-source requirements, entities, dependencies and limitations

### S01 — Nexora_Product_Solution_Overview.pdf

- Subject/purpose: whole-product vision and high-level architecture for CEO, CTO, engineering/product leadership, architects and developers. Dated 30 September 2026, 21 pages.
- Important requirements: connect fragmented organizational/work/code/delivery/runtime/incident context into one intelligence layer (pp3-8 §§1-5); native, integrated and hybrid operating modes (p4); five product areas and shared foundation (p9 §6); preserve normal developer IDE/Git workflow, initially no control of Cursor/Codex required (p10 §7); contextual impact/scope signals rather than developer scoring (pp10-12); evidence-grounded RCA distinguishing Evidence/Inference/Unknown (p13 §9); human review of remediation (pp14-15); AI agents interact only through registered tools, same authorization model/least privilege as humans (p15 §12); tools define name/description/input schema/output schema/permission/risk/audit; canonical models independent of vendor (p16 §13); FastAPI/PostgreSQL high-level architecture (p18 §15).
- Entities/relationships: Employee -> Team -> Project -> Task -> Branch -> Commit -> PR -> Build -> Deployment -> Service -> Incident -> RCA -> Fix -> Validation (p8 §5); not proof of a graph database.
- Dependencies: Teams 1-4 domain data feeding intelligence; Team 5 foundation and connectors; listed integration examples Jira/Linear/Azure DevOps, GitHub/GitLab/Azure DevOps, Sentry/Datadog/PagerDuty/Prometheus/OpenTelemetry (p16). Provider listing does not prove every provider is approved for first delivery.
- Explicit approval evidence: none found; requirements and architecture statements only.
- Proposals/future/conditional: fix branch/apply patch/run tests/create PR is potential future workflow (p14); controlled low-risk automation explicitly depends on policy, permissions, audit/governance (p15); example tool names not implemented APIs.
- Missing/ambiguous: ownership discrepancy for auth/RBAC (p9); no concrete identity/tenant/service contracts; no version choices, deployment topology, NFR targets, provider selection, cost/retention rules or approval records.

### S02 — Nexora_Team1_HRMS_Organization_Spec.pdf

- Subject/purpose: Team 1 organizational context implementation specification, 1 October 2026, 17 pages; Avinash lead, Vijay developer, Meghana developer/shared QA.
- Requirements: HRMS-001 Organizations, 002 Departments, 003 Teams, 004 Employees, 005 Roles/reporting, 006 Project/team assignment, all P0 (p4 §2). Not a complete enterprise HRMS/payroll system (p4). Keep organizational roles separate from platform roles (p9 §7). Employee lifecycle Invited -> Active -> Inactive -> Archived (p8 §6). Team 2 owns Project; Team 1 owns organizational assignment relationships (p10 §8).
- Entities: organizations, departments (organization_id, department_head_id), teams (organization_id, department_id, team_lead_id), employees (organization_id, department/team/manager references), organizational_roles (fields unspecified), team_project_assignments (team_id/project_id/role/dates), project_assignments (employee_id/project_id/allocation_role/dates) (p4).
- Relationships: organization -> department -> team -> employee; employee.manager_id -> employee.id (p10); assignments reference Team 2 project IDs without duplicating project entity (pp10-11).
- Specified API intentions: organization create/list/get/update p5; department/team CRUD pp6-7; employee create/list/get/update, manager/team/project reads p8; teams/{team_id}/projects and employees/{employee_id}/projects POST/GET p11. Not verified implementations; auth and payload/error details absent.
- Technology evidence: SQLAlchemy models, Alembic migration, Pydantic schemas, repository/service/API, validation, unit/API tests, OpenAPI named for organization deliverables (p5 §3).
- Dependencies: consumes Team 2 project_id; provides employee/team/department/project-association context to Teams 3/4; spec expects Team 5 auth/authorization/tenant/RBAC/audit (p14 §11), conflicting with current coordinator ownership. Can develop on agreed IDs/stubs before real services exist (pp11,14-15).
- Explicit approvals: none found.
- Proposals: source schema is design deliverable, not deployed schema evidence; no finalized role fields.
- Missing/ambiguous: new current auth/RBAC scope not integrated into this PDF; user vs employee contract, tenancy/membership/lifecycle invalidation; assignment vs Team 2 membership; identifier formats; deletion semantics; interface shapes/security; main spec vs ERD naming/fields.

### S03 — Nexora_Team2_Task_Project_Management_Spec.pdf

- Subject/purpose: native project/work management spec, 1 October 2026, 19 pages. Abhishek lead, Amod, Sunil developers.
- Requirements: PROJ-001 Project, 002 Epic, 003 Task, 004 Subtask, 005 Assignment/Workflow P0; 006 Sprint, 007 Dependencies, 008 Comments/Activity, 009 Views/Dashboard P1 (p4). Not a complete Jira clone (p3). Must not create competing Employee table (p5 §3). Controlled task flow Backlog -> Todo -> In Progress -> In Review -> Done (p10). Task types FEATURE/BUG/TASK/IMPROVEMENT/SPIKE (p8). Stable task/project IDs enable code/incident traceability (p16).
- Entities/relationships: projects belong to organization; epics belong to project; tasks reference project/epic/parent task/assignee/reporter/team; sprints per project; task_dependencies; task_comments; task_activity (p4). Subtask persistence design explicitly open: parent_task_id or dedicated structure, required relationship remains Task -> Subtask (p9). Sprint-task association required but not table specified in PDF (p11).
- Specified API intentions: project CRUD/member/task/epic reads p6; epic CRUD p7; task CRUD/filtering p8; subtask APIs p9; assignment/status p10; sprint and sprint-task APIs p11; dependencies p12. Comments/activity entities described p13 but endpoint shapes absent.
- Dependencies: Team 1 organization/team/employee references; Team 3 consumes work intent and linking IDs; Team 4 traces task/project/team; Team 5 needs project/task context for authorization, audit, integrations, agents, notifications (p16 §15). Required questions for agents include task's PR link, owner, team/project, expected outcome. Mock stable IDs allowed (p16).
- Explicit approvals: none found.
- Proposals/conditional: sprint statuses are described as possible (p11), dependency types are initial MVP candidates (p12); examples and wireframes not metric targets. Subtask physical model open.
- Missing/ambiguous: assignment authorization, workflow transition matrix, member ownership/permissions vs T1 assignments, canonical task import/upsert/conflict policy, external sync direction, user/employee identity, workspace/epic ERD mismatch, target date/timezone/deletion rules.

### S04 — Nexora_Team3_Engineering_Productivity_Change_Intelligence_Spec.pdf

- Subject/purpose: engineering graph/intelligence spec, 1 October 2026, 20 pages. Srushti lead; Noor productivity/metrics; Kailash change/impact.
- Requirements: ENG-001 canonical model, 002 repository/Git, 003 PR intelligence, 004 metrics, 005 work-to-code, 007 Change Intelligence, 008 impact/dependency P0; 006 insights, 009 scope expansion, 010 dashboards P1 (p4). Canonical entities must not depend on single vendor (p6 §4). Team 5 owns connector; Team 3 consumes normalized Git (p15 §14). Context/trends not developer scoring (p9). Confidence-based signals must not aggressively block changes (p12). Link tasks from branch/message/PR title/description/manual association/integration metadata (p10). Impact combines intent, changes, dependencies, active work, open PRs, tests (p11).
- Entities/relationships: canonical Repository/Commit/PR/Build/Deployment (p6); repositories include project_id/provider/external_id/url/default_branch/status (p7); PRs include repository_id/external_id/author_id/branches/status/review/approval/merge timestamps and change sizes (p8). Engineering relationship chain Task -> Branch -> Commit -> PR -> Build -> Deployment, then Service/Incident/RCA (p5). Builds/deployments explicit final deliverables (p20).
- Specified API intentions: GET repositories, repositories/{id}, projects/{project_id}/repositories (p7). No ingestion/upsert event schema specified. Source field author_id is Team 1 reference but author resolution workflow not defined.
- Dependencies: Team 1 people/team/department, Team 2 project/task/epic/sprint, Team 4 deployment/service/incident relations, Team 5 GitHub/external connectors/AI gateway/auth/authorization (p17 §16). Stable contract IDs/stubs allow parallel work (p17).
- Explicit approvals: none found.
- Future/conditional: GitHub PR status posting marked possible future (p15); metrics list includes may include (p9); no single developer score. Deployment/service boundary needs specificity.
- Missing/ambiguous: canonical ingestion contract, external mapping/dedup/out-of-order/deletion semantics, authors not mapped to employees, repository-to-organization derivation, graph physical storage, service ownership, branch/commit/build schema, metrics precision, PR diff redaction/access.

### S05 — Nexora_Team4_Incident_RCA_Spec.pdf

- Subject/purpose: incident/evidence/RCA/remediation spec, 1 October 2026, 21 pages. Poonam lead, Basvaprasad evidence, Afreen AI/RCA/remediation.
- Requirements: RCA-001 Incident, 002 Ingestion, 003 Timeline, 004 Evidence, 005 Evidence Engine, 006 RCA Agent, 007 candidates, 011 Human Review P0; 008 Fix, 009 Test, 010 Validation, 012 History/Audit P1 (p4). Team 4 explicitly owns incident interpretation/normalization/workflow/RCA; T5 connector framework (p6 §4). Evidence-grounded results distinguish Evidence/Inference/Unknown (pp9-10); multiple root causes with support/contradiction/confidence/affected component/change (pp10-11). Initial fix: patch proposal -> human review, no direct production code modification (p12). Test planning/selection/generation proposals; actual execution via validation pipeline (p13). Human approve/reject/request changes/retry investigation, no automatic merge/deploy default (p14). Investigation audit spans incident/evidence/AI/candidates/fix/tests/validation/review/outcome (p15).
- Entities: incidents with organization_id/project_id/service_id, source/external_id, severity SEV1-4, states OPEN/INVESTIGATING/MITIGATED/RESOLVED/CLOSED, owner IDs and timestamps (p5); evidence record with evidence/incident IDs, type/source/time/reference/content/summary/relevance/confidence (p8); candidate, fix proposal, validation, review/history concepts. Detailed physical schemas outside incident/evidence are not finalized in PDF.
- Specified API intentions: incident create/list/read/update, timeline/evidence/rca/related-changes reads (p5). No agreed T5 ingestion endpoint/event, runtime invocation contract or approval proof format.
- Dependencies: T1 organization/team/employee, T2 project/task, T3 repository/commit/PR/build/deployment/engineering links, T5 GitHub/observability/AI gateway/auth/authorization/audit (p18). Stable IDs allow independent development. Evidence includes logs/metrics/traces, code/build/deployment, service/task/config/previous incidents (p8).
- Explicit approvals: none found.
- Future/conditional: external sources eventually supported; future controlled Fix flow creates branch/applies patch/runs tests/creates PR (p12). T4 spec source normalization may conflict with generic T5 normalization wording; canonical incident business rules remain T4.
- Missing/ambiguous: service owner/API, evidence retrieval vs evidence storage security, user/employee mapping, retention/sensitivity, domain approval vs technical execution approval, validation runner isolation, tool write enablement, incoming canonical contract/idempotency, authorization semantics.

### S06 — Nexora_Team5_Platform_Integrations_AI_Spec.pdf

- Subject/purpose: horizontal platform foundation, integration framework, AI infrastructure and cross-cutting services for Teams 1-4; Sagar, Varshini and source spelling Sharanbasva (pp1-3). Team 5 explicitly does not own other teams' business functionality (p3 §1).
- Important requirements: PLAT-001 foundation/config/errors/logging/health/API standards (p5); PLAT-002 historical auth/session ownership (p5), PLAT-003 shared authorization/RBAC (p6), PLAT-004 tenant context and enforcement with organizational business entities remaining T1 (p7), PLAT-005 central audit and PLAT-016 common events/subscriptions (p8), PLAT-006 reusable connector contract and canonical integrations (p9), PLAT-007 GitHub read/webhooks/build/deployment where available (p10), PLAT-008 Jira/Linear/Azure DevOps initial targets complementary to T2 (p10), PLAT-009 potential observability integrations for T4 (p10), PLAT-010 central provider-agnostic gateway with routing/retries/timeouts/usage/cost/policy (p11), PLAT-011 permission/risk/schema/audit tool metadata (p12), PLAT-012 generic agent infrastructure/context mechanisms while domains stay T3/T4 (p13), PLAT-013 tiered governance (p14), PLAT-014 organization/user/agent/model/provider/token/request/latency/estimated-cost tracking (p15), PLAT-015 eventual versioned evaluation (p15). Every AI request follows authentication, authorization, policy, tool permission, execution, audit; no access beyond the acting user's rights (p20).
- Entities/relationships: source audit record `id, organization_id, actor_id, event_type, resource_type, resource_id, action, metadata, timestamp` (p8); canonical PR/work-item/incident mappings (p9); provider-model-gateway-agent-tool relationships and request usage/evaluation dimensions (pp11-15). These describe responsibilities and conceptual data; the PNG remains a proposed schema.
- Interfaces: common `/health`, `/ready`, `/version` expected p5; connector `authenticate/connect/disconnect/health_check/sync/fetch/handle_webhook` operations p9; illustrative platform API catalog p16 includes integrations list/create/read/sync/delete, AI chat/execute/usage, tools list/read, audit events; historical auth/roles/permissions endpoints require ownership handoff to T1 under S00. Presence in this PDF is not deployment verification or final payload agreement.
- Dependencies: S06 p18 §17 says publish stable contracts for all teams to develop in parallel; T1 platform enforcement/audit, T2 enforcement/audit/events/notifications, T3 normalized engineering/GitHub/AI, T4 observability/GitHub/AI/audit. Three end-to-end acceptance chains are access, external-tool-to-canonical-Nexora, and authorized/policy-controlled/audited AI (p22 §21).
- Explicitly approved decisions: none recorded. Shared architecture responsibilities and P0/P1 labels are source statements, not individual delivery commitments. S00 supersedes identity store/RBAC ownership in pp5-6,16-18,23.
- Proposed/conditional items: agent planner/context/evaluation architecture is labelled potential (p13); advanced provider choices are expandable, observability options potential (p10); evaluation eventual (p15); production tool example requires explicit policy, permissions, human approval, audit (p14), not authorization to deploy automatically. Listed connector method names do not settle unsupported-capability semantics.
- Missing/ambiguous: p4 says ten P0/six P1, while its actual rows contain eleven P0/five P1 (C07/Q13). Notification channels/recipients/delivery rules, first provider/model, secret manager, auth/service trust, tenant/ID schemas, retry budgets, cost budgets/rates, approval proof, context responsibility split, retention/SLOs/deployment topology remain open. P0 gateway tracking and P1 consolidated usage/evaluation sequencing must be agreed, preserving minimum governance on any AI use.


### S07 — Detailed HRMS Organization ERD Schema.png

- Subject/purpose: proposed detailed Team 1 schema across organization/structure, job roles, authentication/users, employees/reporting, RBAC, attendance, leave. No approval marker observed.
- Entities: organization, department, team; job_role; authentication_provider, user_credential, user, user_session, refresh_token; employee, employee_reporting; role, permission, role_permission, user_role; attendance_record/type; leave_type/balance/request/approval.
- Relationships: organization->department->team; employees reference organization/department/team/manager/job role; user->employee; credentials/sessions/refresh tokens attach user; user_role links user/role; role_permission links role/permission; reporting stores dated manager relationships; attendance/leave link employees.
- Supported boundary: identity/RBAC resident with T1 aligns current coordinator, contradicts older PDFs. Job role separate from RBAC role correctly mirrors T1 PDF principle.
- Cross-team dependencies: user_id, employee_id, organization_id, team_id and role/permission references consumed elsewhere. Diagram's employee/user cardinality and team-user arrow need clarification; must not infer they are interchangeable.
- Proposal concerns: user email/employee email duplicated; global uniqueness code/email may not match tenant policy; department/team lacks explicit org scope in some nodes; timestamp types/timezone unspecified; attendance/leave outside six-module spec; `password_hash`/token_hash designs proposed, not accepted identity design.
- Missing/ambiguous: organization membership if one user spans organizations; tenant-scoped platform roles; permission grant/version/invalidation API; login identity lifecycle; project assignments present in PDF absent from this ERD; field naming mismatch singular/plural/id.

### S08 — Nexora_Resource_Plan.png

- Subject/purpose: staffing and responsibility overview. 5 teams, 5 leads, 10 developers, 1 QA, 53 modules stated. No publication date/approval marker observed.
- Assignments: Vignesh Tech Lead/Solution Architect owns technical direction and integration; Team1 Avinash/Vijay/Meghana, Team2 Abhishek/Amod/Sunil, Team3 Srushti/Noor/Kailash, Team4 Poonam/Basavaprasad/Afreen, Team5 Sagar/Varshini/Sharanbasva. Team5 Varshini platform services/security/common infrastructure; Sharanbasva integrations/AI gateway/infrastructure; Sagar architecture/coordination.
- Dependencies: all teams develop in parallel against agreed contract IDs; requirements->architecture->assignment->implementation->review->testing->integration->delivery chain. Shared QA shown under each team.
- Proposal/approval distinction: staffing responsibilities documented; this is not approval of proposed architecture or task scheduling. User current names `Sharanbasava` and `Sagar/Varshini` take precedence for final doc spelling; source shows `Sharanbasva` and Team4 spelling varies.
- Ambiguity: Team1 developer `Meghana` is tagged shared QA while separate repeated QA card says `Megha`; confirm QA contact/allocation. Resource-plan technical lead Vignesh is not automatically the named project coordinator. User gives 2 hours/person/day; no source deadline or throughput commitment. Do not infer six productive implementation hours daily after reviews/coordination; plan bounded reviewable work and explicit integration capacity.

### S09 — Team 2 Project Management ER Diagram.png

- Subject/purpose: proposed project/task/collaboration ERD; labels summary/reporting optional. No approval evidence.
- Entities: workspace, project, project_member, project_role, task, task_assignee/comment/attachment, task_status_history/time_log/dependency, sprint/sprint_task, milestone/milestone_task, project_status_history/document.
- Relationships: workspace organization_id reference -> project; project->task/sprint/milestone; task parent self-reference; task dependencies and multiple task assignees; employees referenced by IDs. No duplicate Employee table.
- Cross-team dependencies: Team1 organization/employee, T3/T4 use project/task IDs.
- Proposal differences: PDF has organization directly on project, epics explicit; ERD workspace added, epic absent. PDF single assignee vs ERD task.assigned_to plus task_assignee many; project_member role_in_project vs project_role graphic ambiguous; role lookup key missing from member schema. Milestones/time logs/attachments/documents not confirmed P0/P1 modules in PDF.
- Missing/ambiguous: project-member vs T1 assignments; role permissions; tenant derivation through workspace; hard FK vs logical cross-service reference; deletion/sync policy.

### S10 — Team 3 Engineering ERD Diagram.png

- Subject/purpose: proposed engineering/canonical/change-intelligence ERD, explicitly notes it can be refined with team feedback.
- Entities: repository, branch, commit, pull_request, pr_changed_file, pr_review, task_pr_link, commit_pr_link, code_component, component_dependency, pr_metrics, review_metrics, deployment_metrics, change_analysis/finding, expected_change_scope, actual_change_scope, scope_finding; optional incident_pr_link.
- Relationships: repository->branches/commits/PRs/components; PR->changed files/reviews/metrics/analysis; task and incident are external references; components form dependency edges; scope compares expected and actual.
- Dependencies: Team1 employee refs for created/reviewer/deployed_by, Team2 task, Team4 incident (the optional link note confusingly says incident from RCA if managed by Team3, contrary coordinator).
- Proposal concerns: repository omits project_id/external_id present in PDF and organization context; no canonical Build entity; deployment_metrics is not a substitute for canonical Deployment model; repo full_name and commit sha globally unique may conflict with tenant/provider scopes; pr_id vs pull_request_id naming differs; optional incident ownership note wrong under coordinator.
- Missing/ambiguous: which side owns link records; event ordering/deletes; author mapping; diff retention; graph representation; versioned upserts; reference resolution.

### S11 — Team 4 Incident Management ERD.png

- Subject/purpose: proposed incident/evidence/RCA/remediation/testing/review/history schema. No approval marker observed.
- Entities: incident/event/timeline, evidence/source/link, rca_investigation, root_cause_candidate, analysis_finding, finding_evidence, fix_proposal, proposed_code_change, remediation_task, test_plan/case/execution, review_decision, approval_history, incident_fix_link, resolution, investigation_history.
- Relationships: incident->events/timeline/evidence/investigations; investigation->candidates/findings/fix proposals; evidence supports findings; fixes->code changes/remediation tasks/tests/reviews; resolution links incident/proposal. External project/task IDs T2; repository/PR/component IDs T3; employee/reviewer IDs T1.
- Scope supported: T4 owns full domain workflows and evidence; T5 must not duplicate these business tables. T4 investigation_history is domain history; T5 audit infrastructure can ingest event references.
- Proposal concerns: incident drops organization_id/service_id from PDF; evidence_source.connection_config can duplicate T5 integration credentials; should reference T5 connection and keep domain source metadata only, subject to agreement. root_cause_candidate evidence_id single while multi-evidence supported in PDF requires relational design refinement. `remediation_task` repeats task title/status/assignee; must clarify projection vs authoritative T2 Task.
- Missing/ambiguous: credential boundary, service identifier owner, multi-tenancy, approvals binding identity/resource/version, domain vs platform audit lifecycle, proposed code patch storage/redaction/retention.

### S12 — Team 5 Platform ERD Blueprint.png

- Subject/purpose: proposed Team 5 platform/integration/AI blueprint; footer explicitly says it is a proposed design refinable on team feedback. No schema approval found.
- Panels/entities: (1) `organization`, `tenant_setting`; (2) `integration_provider`, `integration`, `integration_sync_job`; (3) `github_connection`, `github_repository`, `github_webhook`, `github_sync_history`; (4) `external_project`, `external_task`, `external_id_mapping`; (5) `service`, `log_source`, `metric_source`, `trace_source`; (6) `ai_provider`, `ai_model`, `ai_request`, `usage_event`; (7) `agent`, `tool`, `agent_tool`, `tool_execution`; (8) `ai_policy`, `guardrail`, `evaluation_result`; (9) `model_cost`, `usage_summary`; (10) `platform_event`, `audit_log`, `event_delivery`.
- Relationships: org->settings/integrations/connections/service; provider->integration->sync jobs; GitHub connection->repository/webhooks->history; integration->external projects/tasks/mappings; service->telemetry sources; provider->models->requests->usage; agents/tools through binding plus execution records; policy->guardrails->evaluation results; model->cost periods; event->audit/delivery.
- Dependencies: footer references T1 users/roles/permissions, T2 project/task IDs, T3 repository/PR/commit IDs, T4 incident/evidence/RCA IDs. These must be logical domain references unless shared deployment and cross-schema constraints are separately agreed. Neither diagram lines nor `FK` text authorizes direct cross-team database writes.
- Supported concepts: connection/sync state, provider metadata, tool bindings, execution/audit/usage infrastructure match S06. Each physical structure is still PROPOSED, and entity boundaries must be reconciled first.
- Ownership conflicts: organization is a T1 source of truth (C02); `github_repository` fields overlap T3 repository and must become mapping/bounded connector metadata, not canonical duplicate (C03); `external_project/external_task` duplicate titles/status/assignee unless explicitly bounded transport projections (C04); service catalog owner unresolved, telemetry connection configuration overlaps T4 evidence_source (C05).
- Security/schema gaps: many AI/tool/policy/event tables lack tenant scope; user/employee IDs conflated in other sources; plaintext `prompt/response/input/output/payload/config` fields need allowlisting/redaction/retention, not unconditional persistence; `is_encrypted` flag does not provide secret management; tool required-permission/risk/schema/version metadata from S06 is absent in table fields; no explicit run/step/approval binding, idempotency, cursor, transactional event delivery, usage reservation or policy version. `evaluation_result` per guardrail does not capture full prompt/model/dataset evaluation required by S06 p15. Model cost units/effective periods/precision and usage aggregation boundaries unspecified.
- Explicit approvals: none. Proposed schema in [database-schema.md](database-schema.md) must record retained/replaced/deferred entities and explain additions without asserting diagram acceptance.


## Conflict and discrepancy register

These are detected discrepancies, not silent resolutions. S00 supplies the current target ownership where it explicitly speaks; related contracts still require their owners' agreement.

| ID | Sources and discrepancy | Impact / disposition | Responsible decision and question |
|---|---|---|---|
| C01 | S00/S07 place identity/auth/RBAC in T1; S01 p9, S02 p14, S04 p17, S05 p18, S06 pp5-6,18 assign/provide it through T5 | Adopt S00 T1 authority; T5 only consumes/enforces. Historical auth API ownership and handoff remain unresolved. | Coordinator, Avinash, Sagar; Q01/Q02 |
| C02 | S12 panel1 contains organization despite S00 and S06 p7 T1 organizational ownership | No T5 organization master table; tenant settings reference T1 org. | Avinash/Sagar; Q02/Q15 |
| C03 | S12 GitHub repository repeats S04 canonical repository fields; S04 p15 expressly separates connector and engineering | T5 owns external mappings/delivery state; T3 owns canonical engineering records. Agree ingest acknowledgment, not shared database writes. | Srushti/Sagar; Q04/Q15 |
| C04 | S12 external projects/tasks resemble S03 core entities; S09 membership may overlap S02 project allocations | No T5 business masters; decide bounded transport projections and T1/T2 allocation vs membership semantics. | Abhishek, Avinash, Sagar; Q04/Q16 |
| C05 | S12 service/telemetry credentials vs S11 evidence_source.connection_config; S05 owns incident normalization while S06 shows generic canonical integration | Service owner unresolved; propose T5 credential reference with T4 domain source metadata; T4 owns incident normalization rules. T3 builds/deployments confirmed by S04 pp6,20. | Coordinator, Srushti, Poonam, Sagar; Q05/Q06 |
| C06 | PDFs use `EMP-001` examples/`id`; ERDs UUID/`*_id`; S06 p7 labels User with EMP example; tenant refs absent from several proposed tables | No assumed UUID-wide contract or user=employee equivalence. Agree stable IDs and organization verification before live authorization/ingest. | All leads, especially Avinash; Q02/Q15 |
| C07 | S06 p4 prose 10 P0/6 P1 versus table 11 P0/5 P1; source gateway tracking P0 but consolidated usage P1 | Keep row priorities as evidence; final phased release scope and minimum AI metering need confirmation. | Coordinator/Sagar; Q13/Q07 |
| C08 | S06 PLAT-016 promises events/notifications but only event examples/subscriptions supplied | Event transport can be proposed; no invented email/Slack/SMS channel, recipient rule or SLA. | Sagar/domain leads/coordinator; Q11 |
| C09 | S01 p15/S06 p14 describe assisted write tools; S05 p12 labels branch/patch/test/PR future; all retain human control | Default first execution profile advisory; write eligibility and approval boundary require explicit agreement. No automatic merge/deploy. | Poonam/Sagar/coordinator; Q08/Q13 |
| C10 | S00 Sharanbasava vs S06/S08 Sharanbasva; S08 Meghana shared-QA and Megha QA; T4 Basvaprasad/Basavaprasad variants | Use user spelling for T5; do not infer QA identity or availability, nor identify Vignesh as coordinator without evidence. | Sagar/coordinator; Q16 |

Additional ERD drift under Q15: S07 attendance/leave exceed S02 six-module organizational scope; S09 adds workspace/milestones/documents and omits S03 explicit epic; S10 omits canonical build and project reference; S11 incident drops S05 organization/service references. These changes are proposals awaiting respective domain approval.

## Platform ownership matrix

The owner is the system of record, regardless of physical deployment. APIs below are source-listed intentions or proposed contracts; no endpoint has been verified against an implementation. CT identifiers are defined in [api-contracts.md](api-contracts.md).

| Entity / capability | Owning team and source of truth | Consumers | Responsible API/service evidence | Data boundary and dependencies | Open issue |
|---|---|---|---|---|---|
| Organizations | T1, S00/S02 | T2-T5 | S02 p5 organization API catalog; CT-01 proposed payload | T5 stores org reference/settings only; trust context derives from T1 | Q01/Q02 |
| Users, authentication, sessions, RBAC grants | T1 per S00; current owner confirmed | All teams | CT-01 needed; S06 auth paths historically assigned to T5 | No T5 user, password, session, role or permission-grant master; T5 enforcement calls trusted T1 contract | C01; Q01/Q02 |
| Departments, teams, employees, job roles, reporting | T1, S02 pp4,9-10 | T2-T5 | S02 pp6-8 domain API catalog; CT-01 | Employee identifiers distinct from user identity; organizational role grants no permission by itself | Q02/Q16 |
| Organizational team/employee project allocations | T1, S02 p10 | T2/T3/T4/T5 | S02 p11 assignment API catalog | References T2 project; do not use as authorization membership implicitly | Q16 |
| Projects, epics, tasks, subtasks, sprints, comments/activity/dependencies | T2, S03 pp4-5 | T1/T3/T4/T5 | S03 pp6-12 API catalog; CT-02 | T5 owns only connector mapping/transport state; T2 owns import validation/business transitions | Q04/Q16 |
| Project membership/roles | T2 ERD proposal; relationship to T1 allocations open | T1/T3/T4/T5 | S03 project members read; detailed contract absent | No duplicate membership authority; T1 permission decision must honor agreed domain scope | Q16 |
| Repository, branch, commit, PR and file/review data | T3, S04 pp6-8,15 | T4/T5 | S04 p7 read catalog; CT-03 ingest/read proposed | T5 authenticates connector/fetches/maps; T3 canonical records and business schema | Q04/Q06 |
| Canonical build/deployment and engineering relationships | T3, S04 pp6,20; S05 p18 | T4/T5 | No complete ingest/read contract supplied; CT-03 | T5 provider transport where available, not deployment business source of truth | Q04/Q05 |
| Metrics, work-code links, Change Intelligence, impact/scope | T3, S04 pp9-15 | Product users/T4/T5 runtime | Domain API details missing | T5 generic model/context tooling; T3 meaning/results/scoring and storage | Q04/Q12 |
| Incident, timeline, interpretation/normalization | T4, S05 pp5-7 | T3/T5 | S05 p5 incident API catalog; CT-04 ingest proposed | T5 external transport; T4 owns normalization rules, severity/workflow/idempotent canonical upsert | Q04/Q05 |
| Evidence, RCA, candidates, fix/test/validation, domain approvals/history | T4, S05 pp8-15 | Users/T3/T5 execution | S05 p5 incident evidence/RCA reads; CT-04 | T5 stores technical execution refs and platform audits, not RCA domain masters | Q05/Q08/Q10 |
| Service catalog | OPEN, graph in S01 p8, refs S05 p5, proposed S12 | T3/T4/T5 | No owner/API agreed | T5 telemetry-source config may reference service; no master creation until decision | Q05 |
| Tenant enforcement, common API/config/health conventions | T5, S00/S06 pp5,7 | All teams | health/readiness/version intentions; CT-05 | Depends T1 trust/permission and domain resource ownership, not identity duplication | Q01-Q03 |
| Integration providers/connections/secrets references/mappings/sync | T5, S00/S06 pp9-10 | T2/T3/T4 | S06 p16 integration API catalog; CT-02-CT-05 | Provider credentials never copied to domains; domain schemas/rules remain domain-owned | Q04/Q06 |
| Observability connectors and bounded telemetry access | T5, S06 p10 | T4 primarily, T3 as agreed | CT-04 and registered tool contracts proposed | External systems hold telemetry; T4 owns selected evidence records; service mapping pending | Q05/Q06/Q10 |
| Gateway, model routing, registry, generic agent runtime/context | T5, S06 pp11-13 | T3/T4 and approved future callers | S06 p16 AI/tool API catalog; CT-07 | T1 authorization and T3/T4 context decisions; no model-output authority | Q01/Q07/Q08 |
| AI policy/guardrails/usage/cost/evaluation infrastructure | T5, S06 pp14-15 | Governance users/T3/T4 | AI usage catalog, details proposed CT-07 | Domain teams own evaluation expected results and domain acceptance; provider data rules pending | Q07/Q08/Q10/Q12 |
| Central audit/security events, common event delivery | T5, S06 p8 | All teams and authorized reviewers | Audit read catalog; CT-06 ingest/events proposed | Domain activity/history persists with owner; audit payloads minimized, access tenant-scoped | Q10/Q11 |
| Notifications | T5 capability in S06 PLAT-016, behavior OPEN | Domain consumers/users | No channel/recipient interface specified | No external channel implementation inferred from general capability | Q11/Q13 |

## Dependency map and principal user journeys

### Organization and native work context

Team1 creates organization/departments/teams/employees/roles/reporting; T2 creates project/epic/task/subtask, assigns employee/team via T1 refs, changes task state, records activity, groups sprints/dependencies. T1 owns organizational assignment relationships to T2 projects. Team5 consumes verified identities, permissions and organization context rather than copying core records. Unresolved identity vs employee and membership semantics block production authorization, though contract fixtures can begin.

### Preventive engineering intelligence

Developer continues IDE/Git workflow -> Git branch/commit/PR -> Team5 connector authenticates provider input and retrieves external changes -> agreed normalization/ingestion contract hands engineering records to T3 -> T3 persists canonical repository/branch/commit/PR/build/deployment and links T2 task intent plus T1 ownership -> T3 computes metrics/change impact/scope confidence and displays related work/components/tests/teams. T5 provides AI gateway/tool infrastructure if called, not impact domain rules. Future PR status posting requires separate enabling decision. Failure in provider/delivery should expose sync state and retry safely; no completed engineering update claimed until domain handoff acknowledged.

### Incident, evidence and RCA

External observability or native incident -> T5 connector transport -> T4 incident normalization/interpretation and canonical incident workflow -> T4 gathers evidence from logs/metrics/traces and T3 delivery/code and T2 work/T1 ownership -> T4 Evidence Engine normalizes/correlates investigation context -> T4 RCA workflow invokes T5 governed AI gateway/runtime/tools -> multiple candidates with evidence/inference/unknown/confidence -> T4 stores domain results. T5 stores bounded technical execution/audit/usage references. No unauthorized evidence or tenant data is exposed just because an AI agent requests it.

### Governed remediation

T4 likely cause -> fix proposal and test plan -> validation result -> human review approve/reject/request changes/retry. Future tool execution to branch/patch/test/create PR requires registered tool, caller and service authentication, resource authorization, agent binding, risk policy and specific approval. No default automatic merge/deploy or direct production code modification. T4 review records do not automatically satisfy T5 execution approval without agreed semantic and resource/version binding.

### Operational audit and learning

Each domain retains its business activity/history; T5 provides common security/audit capture and events, transport status, correlation and usage/cost accounting. Domain authorization remains relevant for reading events and AI outputs. Observable failure and replay cannot duplicate business state or billable execution; raw credentials/prompts/evidence are not blanket audit payloads. Retention, immutable/append-only evidence and deletion responsibilities need decisions.


## Confirmed decisions and approval limits

S00 confirms the current Team 1-5 ownership boundary, Sagar's Team 5 lead role, Varshini and Sharanbasava as developers, and approximate daily availability. S01 p18 states FastAPI services and PostgreSQL at the high-level architecture layer. S06 p3 confirms horizontal scope; S04 p15 and S05 p6 separate connector work from domain ownership; S06 p20 confirms no AI authorization bypass. Human review and no automatic merge/deploy by default are explicit in S01 pp14-15 and S05 pp12-14. These are supported requirements or current context, not an inferred approval of any new endpoint, schema, model/provider, infrastructure, release date or ADR.

The main work that can begin without inventing a platform decision is source reconciliation, contract/example drafting, negative test design, and acceptance-fixture preparation. Production identity integration, cross-domain ingestion, tenant-bearing migrations, paid provider execution and write tools are gated by the corresponding Q decisions. See [implementation-plan.md](implementation-plan.md) for task-level readiness.
