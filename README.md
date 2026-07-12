# Dynamind Agentic Modularity Skills

Personal but shareable skills for making agentic software work more bounded, understandable, and contract-driven.

## Included Skills

- `dm-agentic-module-boundaries`
- `dm-contract-first-modules`
- `dm-understandability-review`
- `dm-hypothesis-space-reasoning`
- `dm-bounded-agent-work`
- `dm-new-project`

See [SUITE.md](SUITE.md) for the conceptual overview.

`README.md` and `SUITE.md` are pack-level documentation. The install commands below copy only the skill folders, so those two files are not installed as skills.

## Install In Codex

Copy the skill folders into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R dm-agentic-module-boundaries ~/.codex/skills/
cp -R dm-contract-first-modules ~/.codex/skills/
cp -R dm-understandability-review ~/.codex/skills/
cp -R dm-hypothesis-space-reasoning ~/.codex/skills/
cp -R dm-bounded-agent-work ~/.codex/skills/
cp -R dm-new-project ~/.codex/skills/
```

Restart Codex or start a new task so the skills are discovered.

Test prompt:

```text
Use $dm-bounded-agent-work to plan a safe change to a large Quarkus/Vue codebase.
```

## Install In Claude Code

For a single project, copy the skill folders into `.claude/skills/`:

```bash
mkdir -p .claude/skills
cp -R /path/to/dynamind-agentic-modularity-skills/dm-agentic-module-boundaries .claude/skills/
cp -R /path/to/dynamind-agentic-modularity-skills/dm-contract-first-modules .claude/skills/
cp -R /path/to/dynamind-agentic-modularity-skills/dm-understandability-review .claude/skills/
cp -R /path/to/dynamind-agentic-modularity-skills/dm-hypothesis-space-reasoning .claude/skills/
cp -R /path/to/dynamind-agentic-modularity-skills/dm-bounded-agent-work .claude/skills/
cp -R /path/to/dynamind-agentic-modularity-skills/dm-new-project .claude/skills/
```

For user-level use, copy them to the skills directory supported by your Claude Code installation, commonly `~/.claude/skills/` when local custom skills are enabled.

Test prompt:

```text
Use $dm-understandability-review to review this module boundary for hidden coupling.
```

## Install In OpenCode Or Other Skill-Compatible Agents

Use the agent's configured skills directory or project-local skills folder. Each skill is self-contained and follows the standard folder shape:

```text
skill-name/
  SKILL.md
  agents/openai.yaml
  scripts/        # only when needed
```

If the agent only supports plain prompt files, load the relevant `SKILL.md` directly and run any script manually.

Test prompt:

```text
Use the skill at ./dm-new-project to scaffold a new project named Trial App with package prefix com.dynamind.trial.
```

## Test The New Project Scaffold

Run:

```bash
cd dm-new-project
python3 scripts/scaffold_project.py \
  --project-name "Trial App" \
  --package-prefix com.dynamind.trial \
  --output-dir /tmp/trial-app \
  --with-capacitor \
  --force
```

Inspect:

```bash
find /tmp/trial-app -maxdepth 3 -type f | sort
python3 -m json.tool /tmp/trial-app/frontend/package.json
```

Network-dependent checks:

```bash
cd /tmp/trial-app/frontend && npm install && npm run build
cd .. && mvn -DskipDocs package
cd docs && mvn package
cd ../infra && terraform init && terraform validate
```

## Safety Notes

- The scaffold script writes only to the requested output directory.
- It refuses to write into a non-empty directory unless `--force` is passed.
- It does not install npm packages, download Maven dependencies, run Terraform, or provision Azure resources.
- Treat skills from any third party as executable code when they include scripts.
