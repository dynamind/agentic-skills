# Exceptions register

Where the running system deviates from an accepted decision, on purpose.

An ADR states what we believe is right. Reality sometimes needs something else. Do not
soften the ADR to fit the deviation. A softened principle no longer constrains anything.
Instead, leave the principle intact and **record the deviation, with a name, a reason, a
boundary, and a way out.**

## How to use this register

**Precedence.** For anything listed here, the exception describes what the system does today
and governs implementation. The ADR remains the target state. An exception never amends an
ADR. If a deviation turns out to be permanent and correct, that is a new ADR superseding the
old one, not an entry that lives here forever.

**Adding an entry.** Take the next `EX-nnn`. Name what we do, which decision it departs
from, why, what bounds the damage, and what would end it. An entry with no exit condition
is not an exception. It is an undocumented decision. Write the ADR instead.

**Status.** `Accepted` means someone with the authority to carry the risk has said yes, and
the entry records who. `Proposed` means the deviation exists in the running system, but no
one has accepted it yet. It is a finding that awaits a decision, not a license.

**Reviewing.** Read every entry again once its exit condition might be reachable. Move a
closed entry to the table at the bottom. Do not delete it.

<!-- Entry format:

## EX-001: Short name of what we do

|  |  |
|---|---|
| **Deviates from** | [ADR-NNN](adrs/adr-NNN-title.md) § Section, "quoted rule" |
| **Status** | Accepted · YYYY-MM-DD · Name |
| **Exit** | The condition that ends the deviation |

**What we do.** ...
**Why.** ...
**What bounds it.** ...
-->

## Closed

| Entry | Closed | How |
|---|---|---|
