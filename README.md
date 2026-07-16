# Dynamind Agentic Skills

This repository contains a unified set of skills for making agentic software more understandable, bounded, and maintainable. The skills are designed to compose: use them individually for a focused question or combine them for a larger change.

## Skill groups

### Agentic modularity

- `dm-agentic-module-boundaries` maps module boundaries and hidden coupling.
- `dm-contract-first-modules` defines contracts that make boundaries trustworthy.
- `dm-understandability-review` reviews code and designs for hidden behavior and reasoning risk.
- `dm-hypothesis-space-reasoning` makes ambiguity explicit and reduces plausible hypotheses.
- `dm-bounded-agent-work` turns requests into agent-sized, verifiable tasks.
- `dm-new-project` scaffolds the preferred Quarkus, Vue, documentation, Terraform, and Azure DevOps monorepo.

### Documentation

- `dm-docs-initialize` establishes a topic-first Material for MkDocs documentation system.
- `dm-docs-ingest` creates trustworthy documentation from bounded evidence.
- `dm-docs-garden` audits, synchronizes, and improves an existing documentation corpus.

See [SUITE.md](SUITE.md) for boundaries, principles, and recommended composition.

## Installation and synchronization

Run the installer from this repository to synchronize all nine skills with the global skill directories used by Codex and Claude Code:

```bash
./install-skills.sh
```

The script manages only the `dm-*` skill folders and does not remove unrelated skills. Preview changes first with:

```bash
./install-skills.sh --dry-run
```

Install into just one agent with `--codex-only` or `--claude-only`. The default locations are `~/.codex/skills` and `~/.claude/skills`; override them with `CODEX_SKILLS_DIR` and `CLAUDE_SKILLS_DIR` when needed.

Restart the agent or start a new task after synchronization so newly changed skills are discovered.

## Typical workflows

For a large codebase change:

```text
Use $dm-bounded-agent-work to define the slice and verification.
Use $dm-agentic-module-boundaries to locate the reasoning boundary.
Use $dm-contract-first-modules if the change crosses a boundary.
Use $dm-understandability-review before accepting the design or implementation.
```

For a new or undocumented repository:

```text
Use $dm-docs-initialize to establish the documentation system.
Use $dm-docs-ingest to document one bounded subsystem.
Use $dm-docs-garden to audit the result after feedback or change.
```

The skills are self-contained. Each installable folder contains a `SKILL.md`, optional references or scripts, and an `agents/openai.yaml` metadata file where applicable.

