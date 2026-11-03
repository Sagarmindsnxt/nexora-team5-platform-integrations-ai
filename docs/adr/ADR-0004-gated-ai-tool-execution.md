# ADR-0004: Gated AI tool execution

Status: **PROPOSED — pending authority, policy and approval contract (CT-07; Q08)**

## Context

Team 5's source requires an AI gateway, agent/tool registry, policy/guardrail capability, usage/cost tracking, evaluation and audit. It requires AI to assist analysis and remediation with human review; it does not approve autonomous merge/deploy. Model output and retrieved engineering/incident content can be adversarial or wrong. [S05 pp12-14; S06 pp9-15,20]

## Problem

If a model can select arbitrary endpoint/code/tenant or a generic administrator-like tool, a prompt injection or hallucination becomes an external authorization bypass.

## Options considered

1. Let a model invoke arbitrary HTTP/code tools based on prompt output.
2. Allow only versioned registered tools with typed schemas, fixed trusted handlers, intersected subject/domain/tool/policy permission and audit; require exact human approval for high-risk writes.
3. Deliver only free-text model chat with no registry or audit.

## Proposed decision

Use option 2. A model proposes structured arguments; server code validates them, resolves trusted tenant/resource context, applies policy and current authorization, and dispatches only the fixed registered handler. High-risk writes require a single-use approval bound to actor, tenant, tool/version, argument digest, resource revision, policy and expiry. Automatic merge/deploy remains disabled.

## Consequences and risks

- An agent is not an identity or permission source; it acts only through explicit delegation.
- The first live slice should be read-only/advisory and use approved, minimized context.
- Q08 must define approvers/risk/actions/expiry/revocation before any write path.
- Human approval is not sufficient without post-approval authorization/policy recheck.

## Acceptance / approver

Security, Team 1, affected domain owner, Team 5 and coordinator accept CT-07/Q08. Test injection, argument mutation, disabled tool, stale permission, approval reuse/race/expiry and provider failure before a write-capable tool is eligible.
