---
name: dm-new-project
description: "Scaffold Roy Willemse's standard full-stack monorepo: Java 21 Quarkus backend, Vite/Vue 3 frontend packaged into Maven, hardened npm settings, human and agent onboarding docs, ADRs, Terraform placeholders, Azure DevOps pipeline skeletons. TRIGGER when the user says 'new project', 'start a repo', 'scaffold', 'bootstrap', 'project template', 'greenfield', or asks to create a project in this stack. SKIP when adding to an existing repository."
---

# DM New Project

Use this skill to create a new project in Roy's preferred shape.

## What It Creates

The scaffold creates:

- `backend/`: Java 21 Quarkus application with `quarkus-rest`, JSON support, health, OpenAPI, tests, and Maven wrapper placeholder guidance.
- Postgres/Flyway starter wiring with Quarkus Dev Services and an initial migration.
- `frontend/`: Vite/Vue 3 application with pinned Node/npm, exact dependency versions, hardened npm config, and a dev proxy to the backend.
- Maven Resources Plugin wiring that copies `frontend/dist` into `backend/target/classes/META-INF/resources` and generated docs into `META-INF/resources/docs`.
- `docs/`: VitePress project guide for rapid onboarding by humans and agents, as laid out by `dm-docs-initialize`.
- `docs/architecture/adrs/`: ADR home using a three-digit index, for important structural decisions only.
- `docs/architecture/brief.md`: concise architecture overview with Mermaid diagrams, business context, goals, trade-offs, and roadmap notes.
- `docs/architecture/exceptions.md`: accepted deviations from the intended architecture or delivery plan.
- `docs/architecture/glossary.md`: technology-agnostic ubiquitous language.
- `infra/`: Terraform starter files for Azure deployment.
- `pipelines/`: Azure DevOps CI, CD, and infrastructure deployment skeletons.
- `AGENTS.md`: concise root operating guide for coding agents.
- Optional Capacitor starter configuration inside `frontend/`.

## Before Running

Ask or infer:

- project name;
- Java package prefix, such as `com.dynamind.example`;
- output directory;
- Node and npm versions to pin;
- whether to include Capacitor iOS/Android placeholders;
- Azure environments, defaulting to `dev,staging,production` when unspecified.

If the user wants production-ready Azure resources, gather hosting, database, identity, region, subscription, and naming constraints before extending the Terraform. The included scaffold is a starter, not a live deployment plan.

## Run The Scaffold

From this skill folder:

```bash
python3 scripts/scaffold_project.py
```

Or pass values non-interactively:

```bash
python3 scripts/scaffold_project.py \
  --project-name "Example App" \
  --package-prefix com.dynamind.example \
  --output-dir /path/to/example-app \
  --node-version v22.18.0 \
  --npm-version 11.10.0 \
  --environments dev,staging,production
```

Add `--with-capacitor` to include Capacitor dependencies and `capacitor.config.ts` placeholders.

## After Running

Tell the user the generated project is a scaffold and should be verified with:

```bash
cd frontend && npm install && npm run build
cd .. && mvn -DskipDocs package
cd docs && mvn package
```

Optionally add the Maven wrapper after scaffolding:

```bash
cd backend && mvn -N wrapper:wrapper
```

For Azure Terraform work, validate before planning:

```bash
cd infra
terraform init
terraform validate
terraform plan -var-file=main.tfvars.json
```

Do not run `terraform apply` unless the user explicitly asks to provision resources.
