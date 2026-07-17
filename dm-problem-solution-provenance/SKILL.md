---
name: dm-problem-solution-provenance
description: Trace why work exists by mapping goals, experienced problems, decomposed sub-problems, candidate solutions, trade-offs, and problems introduced by each solution. Use when evaluating feature requests, architecture choices, roadmap items, operational changes, or competing approaches; when asking "what does this solve?"; when a proposed fix may create consequential follow-up work; or when changing an upstream solution could invalidate an entire downstream problem tree.
---

# Problem-Solution Provenance

Model design as an evolving graph of reasons, choices, and consequences. Preserve enough provenance to reconsider an
upstream choice without treating all downstream work as permanent requirements.

## Start With the Goal and Experienced Problem

State the desired outcome before naming a solution. Record the problem as an observable gap between the current and
desired state.

Prefer:

> Reviewers spend attention on claims they experience as meaningfully duplicative.

Avoid:

> We need claim aggregation.

Capture the evidence that the problem exists. Treat an anticipated problem as a hypothesis, not an experienced fact.

## Build the Graph

Use these node types:

- **Goal**: desired outcome or capability.
- **Problem**: an observed or anticipated obstacle to a goal.
- **Solution option**: one possible intervention, not a requirement.
- **Decision**: the selected option with rationale and reconsideration triggers.

Use these relationships:

- `decomposes_into`: a problem contains smaller solvable problems;
- `addressed_by`: a solution option attempts to solve a problem;
- `introduces`: adopting a solution creates or exposes another problem;
- `also_addresses`: one solution helps with another problem;
- `supersedes`: a later choice replaces an earlier solution;
- `invalidates`: an upstream change makes a downstream branch irrelevant;
- `observed_by`: feedback, measurements, incidents, or examples demonstrate a problem.

Treat the structure as a graph even when presenting one local branch as a tree. Problems and solutions may be shared
across branches.

## Evaluate More Than One Solution

For each credible option, state:

- the mechanism by which it solves the problem;
- what it deliberately does not solve;
- assumptions required for it to work;
- benefits and costs;
- new problems it introduces;
- reversibility and switching cost;
- the smallest observation or experiment that would discriminate it from alternatives.

Include "do nothing yet," improve an upstream step, and change the presentation rather than the underlying model when
they are credible options.

Do not turn every introduced problem into immediate work. Record it, then prioritize it only when risk or experience
justifies doing so.

## Reconsider Upstream Choices

Before solving a deep leaf, walk back toward the root:

1. Confirm the root goal still matters.
2. Confirm the parent problem is experienced or sufficiently risky.
3. Ask whether the current upstream solution created this problem.
4. Compare fixing the leaf with replacing or narrowing the upstream solution.
5. Mark branches invalidated by a changed upstream decision.

This guard prevents accidental commitment to a large consequence tree. For example, on-premises and cloud hosting may
serve the same goal while producing substantially different security, staffing, cost, availability, and governance
problem graphs.

## Drive Depth From Feedback

Prefer a thin end-to-end path through all essential capabilities. Deepen a component when observed defects, risks, or
value demonstrate the need.

When feedback reveals friction:

1. Record the experienced problem and evidence.
2. Locate the goal and existing solution that produced the context.
3. Generate alternatives before accepting the most obvious feature.
4. Choose the smallest reversible intervention that improves the outcome.
5. Preserve introduced problems and reconsideration triggers.

## Compose With Other Skills

Use `dm-hypothesis-space-reasoning` when several explanations for the problem fit the evidence. Use this skill to map
what each solution would solve and create. Use ADRs to record structurally significant decisions selected from the
graph; the graph preserves the wider rationale and rejected alternatives.

## Output Shape

Keep the map proportional to the decision:

```markdown
## Goal

## Observed problem
Evidence:
Parent or introducing decision:

## Solution options

### Option A
Solves through:
Does not solve:
Trade-offs:
Introduces:
Reconsider when:

### Option B
...

## Recommendation
Selected option:
Why now:
Smallest validating step:
Invalidated or deferred branches:
```

Use Mermaid only when branching or cross-links materially improve understanding. Make provenance explicit rather than
producing a decorative diagram.
