# Exceptions register

Where the running system deviates from an accepted decision, on purpose.

An ADR states what we believe is right. Reality sometimes needs something else. The wrong
response is to soften the ADR until the deviation fits inside it, because then the
principle no longer tells anyone anything. The right response is to leave the principle
intact and **record the deviation, with a name, a reason, a boundary, and a way out.**

## How to use this register

**Precedence.** For anything listed here, the exception describes what the system does today
and governs implementation. The ADR remains the target state. An exception never amends an
ADR. If a deviation turns out to be permanent and correct, that is a new ADR superseding the
old one, not an entry that lives here forever.

**Adding an entry.** Take the next `EX-nnn`. Name what we actually do, which decision it
departs from, why, what bounds the damage, and what would end it. An entry with no exit
condition is not an exception; it is an undocumented decision. Write the ADR instead.

**Status.** `Accepted` means someone with the authority to carry the risk has said yes, and
the entry records who. `Proposed` means the deviation exists in the running system but nobody
has explicitly accepted it: a finding awaiting a decision, not a license.

**Reviewing.** Every entry gets read whenever its exit condition plausibly became reachable.
Closed entries move to the table at the bottom rather than being deleted.

<!-- Entry format:

## EX-001: Short name of what we do

|  |  |
|---|---|
| **Deviates from** | [ADR-NNN](adrs/adr-NNN-title.md) § Section, "quoted rule" |
| **Status** | Accepted · YYYY-MM-DD · Name |
| **Exit** | The condition that ends the deviation |

**What we actually do.** ...
**Why.** ...
**What bounds it.** ...
-->

## Closed

| Entry | Closed | How |
|---|---|---|
