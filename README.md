# Nexora Team 5 — Platform, Integrations & AI Infrastructure

## Overview

Team 5 is responsible for providing shared platform services, integration infrastructure, and AI capabilities for the Nexora platform.

The team supports Teams 1–4 through common services and agreed interfaces without duplicating their core business entities.

## Scope

- Platform and tenant management
- Integration framework and synchronization
- GitHub integration, webhooks, and repository synchronization
- Project management integrations and external ID mapping
- Observability integrations for logs, metrics, and traces
- AI gateway and model management
- Agent and tool registry
- AI governance, guardrails, and evaluation
- AI usage and cost tracking
- Audit logs and platform events

## Team Responsibilities

- **Team Lead:** Platform planning, cross-team coordination, shared contracts, and code reviews.
- **Platform Developer:** Platform services, security, and common infrastructure.
- **Integrations & AI Developer:** Integration framework, AI gateway, and AI infrastructure.

## Cross-Team Dependencies

- **Team 1:** Organization, users, authentication, and RBAC.
- **Team 2:** Projects, tasks, and project/task identifiers.
- **Team 3:** Repositories, branches, commits, pull requests, and engineering data.
- **Team 4:** Incidents, evidence, and root-cause analysis.

## Development Status

The ERDs are proposed designs for review. Shared identifiers, API contracts, ownership boundaries, and technical decisions must be agreed upon before finalizing the database schemas and implementation.

## Development Workflow

The team will follow the agreed Git branching, pull-request, code-review, and testing practices once confirmed.

## Documentation

### Run and verify the backend

From the repository root, install dependencies with `python -m pip install -r requirements.txt`, then run:

```powershell
python -m uvicorn nexora_platform.app:app --app-dir src --reload
```

Open Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) and use **Try it out** to verify:

| GET endpoint | Behavior |
| --- | --- |
| `/api/v1/health`, `/health` | Same application-health response, HTTP 200, with no database access. |
| `/api/v1/health/db`, `/ready` | Same database-health response; executes `SELECT 1` using the shared engine. HTTP 200 on success, sanitized HTTP 503 when configuration is missing or connectivity fails. |
| `/version` | `{"version": "0.1.0"}`, matching the OpenAPI release version. |

The application can start without database configuration. To enable successful readiness checks, configure PostgreSQL using `.env.example` as a reference and start the database. Do not commit real credentials. The readiness check currently verifies connectivity, not schema compatibility.

Run unit tests without PostgreSQL:

```powershell
python -m pytest tests/unit -q
```

With a configured, running PostgreSQL instance, run the real connectivity test:

```powershell
python -m pytest tests/integration -q
```

Project documentation will be maintained in the `docs/` directory as the architecture and implementation decisions are finalized.
