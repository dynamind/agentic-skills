# Page Contracts

Choose the primary reader need before writing.

## Landing

Route by intent. State what each destination helps the reader accomplish. Avoid becoming a second system overview.

## Explanation

Lead with a short summary, context, and mental model. Explain normal behavior, constraints, trade-offs, failure modes, and related decisions. Avoid procedural detours and exhaustive parameter tables.

## Tutorial

Provide a reliable, bounded learning path with a visible result. Minimize branching, explain only what supports the learning step, and verify that commands work in the stated environment.

## How-to

Name the outcome and prerequisites. Give an actionable sequence, decision points, verification, and recovery. Assume the reader has baseline competence.

## Reference

Define scope and organize exact facts for lookup. Be exhaustive within that scope, terse, structured, and explicit about versions and defaults. Link to explanation rather than embedding essays.

## Feature

Explain purpose, actors, user or system flow, business rules, edge cases, data, interfaces, operational considerations, limitations, architecture, and decisions. Keep exact API and configuration facts canonical elsewhere.

## Architecture component

Explain responsibility, context, owned state, inputs, outputs, dependencies, runtime behavior, failure modes, scaling, security, observability, related features, and decisions.

## Decision

Record status, context, decision, consequences, alternatives considered, and supersession. Do not rewrite the record merely because preferences change.

## Runbook

State trigger conditions, safety constraints, prerequisites, diagnostic evidence, actions, verification, rollback or escalation, and ownership. Treat commands as operationally sensitive.

## Release and roadmap

Separate shipped fact from planned direction. Date entries and make compatibility, migration, deprecation, and uncertainty explicit.

## Incremental disclosure

Use summaries and section ordering appropriate to the contract. Do not impose one universal template. Split a page when different reader intents cause it to alternate repeatedly between learning, action, lookup, and explanation.

## Diagrams and decisions

Use Mermaid for diagrams. Prefer structural meaning over fixed colors and diagram-local themes so diagrams remain legible in light and dark palettes. Store architecture decisions under `docs/architecture/adrs/` with three-digit identifiers; update both the ADR index and site navigation.
