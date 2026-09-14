---
name: dm-hypothesis-space-reasoning
description: "Diagnose or decide under ambiguity by holding several hypotheses open, comparing them, and ruling them out with evidence. TRIGGER when the user asks 'why does this happen', 'what's causing', 'investigate', 'debug', 'figure out', reports a bug or flaky behaviour without a known cause, or asks an under-specified question with several plausible readings. Also use when you notice yourself about to commit to a single explanation early. SKIP when the cause is already established or the question has one obvious answer."
---

# Hypothesis-Space Reasoning

Use this skill when "I do not know" means there are too many plausible answers, not too few.

## Expand Before Ranking

Before choosing an answer, generate qualitatively different hypotheses. Do not stop at three options because three looks tidy.

For each hypothesis, capture:

- what would make it true;
- what evidence supports it;
- what evidence would refute it;
- what assumption distinguishes it from the others;
- what observation would collapse the space fastest.

Prefer a small set of meaningfully different hypotheses over a long list of variants.

## Closed-World Guard

Do not assume the prompt or visible code is the whole world when the domain is open-ended.

Distinguish:

- **closed-world task**: the problem statement intentionally contains all relevant facts;
- **open-world task**: missing facts, hidden dependencies, external systems, or context may change the answer.

For open-world tasks, state the missing discriminators instead of presenting a single answer as settled.

## Certainty Expression

Express certainty through the state of the hypothesis space:

- **Settled**: one hypothesis explains the evidence and credible alternatives were checked.
- **Leaning**: one hypothesis is strongest, but named alternatives remain viable.
- **Underdetermined**: multiple hypotheses fit; more constraints are needed.
- **Unknown**: no adequate hypothesis exists yet; gather information.

This is different from generic confidence. A well-supported answer can still be underdetermined if several models fit the same evidence.

## Discriminating Questions

Ask questions only when answers would materially reduce the solution space.

Good questions distinguish hypotheses:

- "Did this begin after the deployment?"
- "Is the failure user-specific or global?"
- "Is the module the sole writer of this state?"
- "Are retries idempotent?"

Weak questions merely gather more context without changing the decision.

## Output Shape

Use this compact form:

```markdown
## Hypothesis Space

H1:
Evidence:
Missing discriminator:

H2:
Evidence:
Missing discriminator:

Current certainty:
Next best observation:
Recommended action:
```

If the user needs an answer now, provide the best provisional answer and mark the assumptions it rests on.
