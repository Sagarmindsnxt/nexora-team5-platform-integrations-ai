# ADR-0006: Minimized AI data and usage ledger

Status: **PROPOSED — pending provider, price, retention and evaluation decisions (Q06/Q07/Q10/Q12/Q14)**

## Context

Team 5 needs model routing, prompt/input handling, usage/cost tracking, guardrails and evaluations. The sources provide no selected model/provider, approved data classification, token-price schedule, budget policy, retention period, residency rule or evaluation benchmark. [S06 pp9-15; S01 pp14-16]

## Problem

Storing raw prompts/provider responses by default can expose code, incident evidence or personal data. Treating a provider-reported token count or a mutable price as a final cost can misstate usage and mask unknowns.

## Options considered

1. Store all raw inputs/outputs indefinitely and calculate a single mutable total cost.
2. Store minimal request/attempt metadata, pointers or approved redacted artifacts; retain raw content only under explicit policy; record provider usage and price-version estimate separately, with unknown state where absent.
3. Do no metering/evaluation until every policy is finalized.

## Proposed decision

Use option 2 as the target. Separate a logical request from provider attempts, usage observations and price versions. Default audit/logging excludes raw prompt/output/credential data. Evaluation fixtures are synthetic/redacted unless a data policy approves another route. No automatic model/tool promotion follows from a score.

## Consequences and risks

- Q07 decides provider/model/budget/currency/pricing authority; Q10 retention; Q12 evaluation policy; Q14 operational data placement.
- `unknown` is a valid cost/usage/retention disposition and must not be coerced to zero.
- More detailed diagnostics may require a deliberately approved, access-controlled artifact path.
- Data minimization can reduce later debugging fidelity; provenance and safe correlation IDs compensate without pretending to retain content.

## Acceptance / approver

Coordinator plus data/security/operations and Team 5 accept the applicable policies. Verify route/data-class denial, redaction canary, provider-price version calculation, unknown usage, retention/purge and evaluation fixture provenance before live model traffic.
