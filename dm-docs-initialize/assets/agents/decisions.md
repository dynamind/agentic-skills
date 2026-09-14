# Settled decisions

Decisions that are settled. Implement against them. Do not reopen them in a diff. If one
looks wrong, say so and stop. Do not route around it.

Where a decision has an ADR, the ADR is authoritative and the line here is a pointer.

Where the running system knowingly departs from one of these, the departure is registered in
[`docs/architecture/exceptions.md`](../docs/architecture/exceptions.md) with a boundary and an
exit condition. Check the register before concluding that code contradicts a decision.

## Product and scope

<!-- One bold line per decision, then the pointer: → [`docs/...`](../docs/...) -->

## Architecture and integration
