#!/usr/bin/env python3
"""Scaffold a Dynamind Quarkus + Vue monorepo without network calls."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DEFAULT_NODE = "v22.18.0"
DEFAULT_NPM = "11.10.0"
DEFAULT_ENVS = "dev,staging,production"


def prompt(label: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or (default or "")


def yes_no(label: str, default: bool = False) -> bool:
    marker = "Y/n" if default else "y/N"
    value = input(f"{label} [{marker}]: ").strip().lower()
    if not value:
        return default
    return value in {"y", "yes", "true", "1"}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "new-project"


def java_identifier(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_]", "", value)
    if not cleaned:
        return "App"
    if cleaned[0].isdigit():
        cleaned = f"App{cleaned}"
    return cleaned[0].upper() + cleaned[1:]


def package_path(package_prefix: str) -> Path:
    return Path(*package_prefix.split("."))


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip(), encoding="utf-8")


def ensure_empty_or_confirm(path: Path, force: bool) -> None:
    if not path.exists():
        return
    if force:
        return
    if any(path.iterdir()):
        raise SystemExit(f"Refusing to write into non-empty directory: {path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-name")
    parser.add_argument("--package-prefix")
    parser.add_argument("--output-dir")
    parser.add_argument("--node-version", default=DEFAULT_NODE)
    parser.add_argument("--npm-version", default=DEFAULT_NPM)
    parser.add_argument("--environments", default=DEFAULT_ENVS)
    parser.add_argument("--with-capacitor", action="store_true")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    project_name = args.project_name or prompt("Project name", "Example App")
    slug = slugify(project_name)
    package_prefix = args.package_prefix or prompt("Java package prefix", f"com.dynamind.{slug.replace('-', '')}")
    output_dir = Path(args.output_dir or prompt("Output directory", str(Path.cwd() / slug))).expanduser().resolve()
    node_version = args.node_version or DEFAULT_NODE
    npm_version = args.npm_version or DEFAULT_NPM
    environments = [env.strip() for env in (args.environments or DEFAULT_ENVS).split(",") if env.strip()]
    with_capacitor = args.with_capacitor or (not args.output_dir and yes_no("Include Capacitor iOS/Android placeholders?", False))

    ensure_empty_or_confirm(output_dir, args.force)
    app_class = java_identifier(slug)
    pkg_path = package_path(package_prefix)
    env_list = ", ".join(environments)

    create_root(output_dir, project_name, slug, package_prefix, node_version, npm_version, env_list)
    create_backend(output_dir, project_name, slug, package_prefix, pkg_path, app_class)
    create_frontend(output_dir, project_name, slug, node_version, npm_version, with_capacitor)
    create_docs(output_dir, project_name, slug, package_prefix, env_list)
    create_infra(output_dir, slug, environments)
    create_pipelines(output_dir, slug, environments)

    print(f"Created scaffold at {output_dir}")
    print("Next checks:")
    print("  cd frontend && npm install && npm run build")
    print("  cd .. && mvn -DskipDocs package")
    print("  cd docs && mvn package")
    print("  cd ../infra && terraform init && terraform validate")
    return 0


def create_root(root: Path, project_name: str, slug: str, package_prefix: str, node_version: str, npm_version: str, env_list: str) -> None:
    write(root / ".gitignore", """
target/
dist/
node_modules/
.idea/
.vscode/
.DS_Store
data/local-only/
.env.local
.terraform/
*.tfstate
*.tfstate.*
""")
    write(root / ".nvmrc", f"{node_version}\n")
    write(root / "NPM_HARDENING.md", f"""
# npm Hardening

This repo pins Node and npm and uses hardened npm defaults.

- Node is pinned in `.nvmrc` to `{node_version}`.
- npm is pinned through `frontend/package.json` `packageManager` to `npm@{npm_version}`.
- `frontend/.npmrc` disables lifecycle scripts with `ignore-scripts=true`.
- New dependencies are saved exactly with `save-exact=true`.
- `min-release-age=7` avoids resolving package versions published less than seven days ago.

When adding dependencies:

1. Prefer exact versions.
2. Review lockfile changes.
3. Do not enable lifecycle scripts globally.
4. If a package requires an install script, document the exception and run it explicitly.
""")
    write(root / "pom.xml", f"""
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>{package_prefix}</groupId>
    <artifactId>{slug}</artifactId>
    <version>0.1.0-SNAPSHOT</version>
    <packaging>pom</packaging>

    <modules>
        <module>docs</module>
        <module>backend</module>
    </modules>
</project>
""")
    write(root / "README.md", f"""
# {project_name}

Full-stack monorepo scaffold:

- `backend/`: Java 21 Quarkus REST API.
- `frontend/`: Vite/Vue 3 app packaged into the backend static resources.
- `docs/`: Maven-backed MkDocs architecture and onboarding guide.
- `infra/`: Azure Terraform starter.
- `pipelines/`: Azure DevOps pipeline skeletons.

## Local Development

```bash
cd backend && mvn quarkus:dev
cd frontend && npm install && npm run dev
```

The frontend dev server proxies `/api` to `http://localhost:8080`.

## Build

```bash
cd frontend && npm install && npm run build
cd .. && mvn -DskipDocs package
cd docs && mvn package
```

The backend build copies `frontend/dist` into `backend/target/classes/META-INF/resources` and generated docs from `site/` into `META-INF/resources/docs`.

## Environments

Initial environments: {env_list}.
""")
    write(root / "AGENTS.md", f"""
# AGENTS.md

This repo is a Quarkus + Vue monorepo. Keep changes bounded and verify with focused commands.

## Layout

- `backend/`: Quarkus REST API and static resource packaging.
- `frontend/`: Vite/Vue 3 client.
- `docs/`: MkDocs project guide, architecture brief, ADRs, exceptions, glossary.
- `infra/`: Terraform for Azure.
- `pipelines/`: Azure DevOps YAML.

## Common Commands

```bash
cd frontend && npm install && npm run build
cd . && mvn -DskipDocs package
cd docs && mvn package
cd infra && terraform validate
```

## Dependency Rules

Follow `NPM_HARDENING.md`. Keep npm lifecycle scripts disabled unless a reviewed exception is documented.

## Architecture Notes

Write ADRs only for important structural decisions that are hard to reverse later. Do not write ADRs for routine feature choices.
""")


def create_backend(root: Path, project_name: str, slug: str, package_prefix: str, pkg_path: Path, app_class: str) -> None:
    backend = root / "backend"
    write(backend / "pom.xml", f"""
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>{package_prefix}</groupId>
        <artifactId>{slug}</artifactId>
        <version>0.1.0-SNAPSHOT</version>
    </parent>

    <artifactId>{slug}-backend</artifactId>
    <packaging>quarkus</packaging>

    <properties>
        <compiler-plugin.version>3.13.0</compiler-plugin.version>
        <maven.compiler.release>21</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <quarkus.platform.group-id>io.quarkus.platform</quarkus.platform.group-id>
        <quarkus.platform.artifact-id>quarkus-bom</quarkus.platform.artifact-id>
        <quarkus.platform.version>3.34.6</quarkus.platform.version>
        <skipITs>true</skipITs>
        <surefire-plugin.version>3.5.4</surefire-plugin.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>${{quarkus.platform.group-id}}</groupId>
                <artifactId>${{quarkus.platform.artifact-id}}</artifactId>
                <version>${{quarkus.platform.version}}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <dependencies>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-rest</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-rest-jackson</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-smallrye-health</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-smallrye-openapi</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-jdbc-postgresql</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-flyway</artifactId>
        </dependency>
        <dependency>
            <groupId>io.quarkus</groupId>
            <artifactId>quarkus-junit5</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>io.rest-assured</groupId>
            <artifactId>rest-assured</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>${{quarkus.platform.group-id}}</groupId>
                <artifactId>quarkus-maven-plugin</artifactId>
                <version>${{quarkus.platform.version}}</version>
                <extensions>true</extensions>
                <executions>
                    <execution>
                        <goals>
                            <goal>build</goal>
                            <goal>generate-code</goal>
                            <goal>generate-code-tests</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
            <plugin>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>${{compiler-plugin.version}}</version>
                <configuration>
                    <parameters>true</parameters>
                </configuration>
            </plugin>
            <plugin>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>${{surefire-plugin.version}}</version>
                <configuration>
                    <systemPropertyVariables>
                        <java.util.logging.manager>org.jboss.logmanager.LogManager</java.util.logging.manager>
                        <maven.home>${{maven.home}}</maven.home>
                    </systemPropertyVariables>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-resources-plugin</artifactId>
                <version>3.3.1</version>
                <executions>
                    <execution>
                        <id>copy-frontend-resources</id>
                        <phase>validate</phase>
                        <goals>
                            <goal>copy-resources</goal>
                        </goals>
                        <configuration>
                            <outputDirectory>${{project.build.directory}}/classes/META-INF/resources/</outputDirectory>
                            <resources>
                                <resource>
                                    <directory>${{project.parent.basedir}}/frontend/dist/</directory>
                                </resource>
                                <resource>
                                    <directory>${{project.parent.basedir}}/site/</directory>
                                    <targetPath>docs</targetPath>
                                </resource>
                            </resources>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
""")
    write(backend / "src/main/resources/application.properties", f"""
quarkus.http.port=8080
quarkus.smallrye-openapi.path=/q/openapi
quarkus.swagger-ui.always-include=true
quarkus.application.name={slug}

quarkus.datasource.db-kind=postgresql
quarkus.datasource.devservices.image-name=postgres:18-alpine
quarkus.datasource.devservices.port=5432
quarkus.datasource.devservices.volumes."../data/local-only/postgres-dev"=/var/lib/postgresql/data
quarkus.flyway.migrate-at-start=true
""")
    write(backend / "src/main/resources/db/migration/V001__initial_schema.sql", """
CREATE TABLE app_health_marker (
    id INTEGER PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO app_health_marker (id)
VALUES (1)
ON CONFLICT (id) DO NOTHING;
""")
    write(backend / "src/main/java" / pkg_path / "HelloResource.java", f"""
package {package_prefix};

import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

@Path("/api/hello")
public class HelloResource {{
    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String hello() {{
        return "Hello from {project_name}";
    }}
}}
""")
    write(backend / "src/test/java" / pkg_path / "HelloResourceTest.java", f"""
package {package_prefix};

import static io.restassured.RestAssured.given;
import static org.hamcrest.CoreMatchers.is;

import io.quarkus.test.junit.QuarkusTest;
import org.junit.jupiter.api.Test;

@QuarkusTest
class HelloResourceTest {{
    @Test
    void helloReturnsMessage() {{
        given()
            .when().get("/api/hello")
            .then()
            .statusCode(200)
            .body(is("Hello from {project_name}"));
    }}
}}
""")
    write(backend / "README.md", f"""
# Backend

Quarkus backend for {project_name}.

```bash
mvn quarkus:dev
mvn test
mvn package
```

The Maven Resources Plugin copies `../frontend/dist` into `target/classes/META-INF/resources` and `../site` into `target/classes/META-INF/resources/docs`.
""")


def create_frontend(root: Path, project_name: str, slug: str, node_version: str, npm_version: str, with_capacitor: bool) -> None:
    frontend = root / "frontend"
    capacitor_deps = ""
    capacitor_scripts = ""
    capacitor_dev_dep = ""
    if with_capacitor:
        capacitor_deps = """
    "@capacitor/app": "8.1.0",
    "@capacitor/core": "8.4.0",
    "@capacitor/ios": "8.4.0",
    "@capacitor/android": "8.4.0","""
        capacitor_scripts = """
    "cap:sync": "npx cap sync",
    "ios:sync": "npx cap sync ios",
    "android:sync": "npx cap sync android","""
        capacitor_dev_dep = """
    "@capacitor/cli": "8.4.0","""
    write(frontend / ".nvmrc", f"{node_version}\n")
    write(frontend / ".npmrc", """
ignore-scripts=true
save-exact=true
min-release-age=7
engine-strict=true
""")
    write(frontend / "package.json", f"""
{{
  "name": "{slug}-frontend",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "packageManager": "npm@{npm_version}",
  "scripts": {{
    "dev": "vite",
    "build": "vitest run src/tests/unit && npm run type-check && npm run build-only",
    "build-only": "vite build",
    "preview": "vite preview",
    "test:unit": "vitest src/tests/unit",
    "type-check": "vue-tsc --build"{',' if with_capacitor else ''}
{capacitor_scripts.rstrip(',')}
  }},
  "dependencies": {{
{capacitor_deps}
    "vue": "3.5.35",
    "vue-router": "5.1.0",
    "pinia": "3.0.4"
  }},
  "devDependencies": {{
{capacitor_dev_dep}
    "@tsconfig/node22": "22.0.2",
    "@vitejs/plugin-vue": "6.0.7",
    "@vue/test-utils": "2.4.10",
    "@vue/tsconfig": "0.9.1",
    "jsdom": "29.1.1",
    "typescript": "6.0.3",
    "vite": "8.0.16",
    "vitest": "4.1.8",
    "vue-tsc": "3.3.3"
  }},
  "engines": {{
    "node": "{node_version.lstrip('v')}",
    "npm": "{npm_version}"
  }}
}}
""")
    write(frontend / "index.html", f"""
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{project_name}</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
""")
    write(frontend / "vite.config.ts", """
import { fileURLToPath, URL } from 'node:url';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 5173,
    strictPort: true,
    proxy: {
      '/api': 'http://localhost:8080',
    },
  },
  test: {
    environment: 'jsdom',
  },
});
""")
    write(frontend / "tsconfig.json", """
{
  "extends": "@vue/tsconfig/tsconfig.dom.json",
  "include": ["src/**/*.ts", "src/**/*.vue"],
  "compilerOptions": {
    "composite": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
""")
    write(frontend / "src/main.ts", """
import { createApp } from 'vue';
import App from './App.vue';

createApp(App).mount('#app');
""")
    write(frontend / "src/App.vue", f"""
<script setup lang="ts">
const title = '{project_name}';
</script>

<template>
  <main>
    <h1>{{{{ title }}}}</h1>
    <p>Vite/Vue frontend served by Quarkus in production.</p>
  </main>
</template>
""")
    write(frontend / "src/tests/unit/app.test.ts", """
import { mount } from '@vue/test-utils';
import { describe, expect, it } from 'vitest';
import App from '../../App.vue';

describe('App', () => {
  it('renders the project title', () => {
    expect(mount(App).text()).toContain('Vite/Vue frontend');
  });
});
""")
    if with_capacitor:
        write(frontend / "capacitor.config.ts", f"""
import type {{ CapacitorConfig }} from '@capacitor/cli';

const config: CapacitorConfig = {{
  appId: 'com.dynamind.{slug.replace("-", "")}',
  appName: '{project_name}',
  webDir: 'dist',
}};

export default config;
""")


def create_docs(root: Path, project_name: str, slug: str, package_prefix: str, env_list: str) -> None:
    write(root / "docs/pom.xml", f"""
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>{package_prefix}</groupId>
        <artifactId>{slug}</artifactId>
        <version>0.1.0-SNAPSHOT</version>
    </parent>

    <artifactId>{slug}-docs</artifactId>
    <packaging>pom</packaging>

    <properties>
        <skipDocs>false</skipDocs>
        <exec-maven-plugin.version>3.5.0</exec-maven-plugin.version>
    </properties>

    <build>
        <plugins>
            <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>exec-maven-plugin</artifactId>
                <version>${{exec-maven-plugin.version}}</version>
                <executions>
                    <execution>
                        <id>mkdocs-build</id>
                        <phase>compile</phase>
                        <goals>
                            <goal>exec</goal>
                        </goals>
                        <configuration>
                            <executable>${{project.basedir}}/.mkdocs/docs-serve</executable>
                            <workingDirectory>${{project.basedir}}/.mkdocs</workingDirectory>
                            <arguments>
                                <argument>build</argument>
                            </arguments>
                            <skip>${{skipDocs}}</skip>
                        </configuration>
                    </execution>
                    <execution>
                        <id>mkdocs-serve</id>
                        <phase>none</phase>
                        <goals>
                            <goal>exec</goal>
                        </goals>
                        <configuration>
                            <executable>${{project.basedir}}/.mkdocs/docs-serve</executable>
                            <workingDirectory>${{project.basedir}}/.mkdocs</workingDirectory>
                            <arguments>
                                <argument>serve</argument>
                            </arguments>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
""")
    write(root / "docs/.mkdocs/mkdocs.yml", f"""
site_name: {project_name}
site_description: Living guide and knowledge base for {project_name}
docs_dir: ..
site_dir: ../../site

theme:
  name: material
  features:
    - navigation.sections
    - navigation.indexes
    - navigation.top
    - content.code.copy

plugins:
  - search
  - mermaid2

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - tables
  - toc:
      permalink: true
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:mermaid2.fence_mermaid_custom

exclude_docs: |
  pom.xml
  target/
  .mkdocs/

nav:
  - Home: index.md
  - Architecture:
      - Brief: architecture/brief.md
      - Exceptions: architecture/exceptions.md
      - Glossary: architecture/glossary.md
      - ADRs:
          - Overview: architecture/adrs/README.md
          - 000 Record architecture decisions: architecture/adrs/000-record-architecture-decisions.md
""")
    write(root / "docs/.mkdocs/docs-requirements.txt", """
mkdocs-material==9.7.2
mkdocs-mermaid2-plugin==1.3.0
pymdown-extensions==10.18.1
""")
    write(root / "docs/.mkdocs/Dockerfile", """
FROM python:3.12-slim

COPY docs-requirements.txt /tmp/docs-requirements.txt
RUN pip install --no-cache-dir -r /tmp/docs-requirements.txt

WORKDIR /work/docs/.mkdocs
ENTRYPOINT ["mkdocs"]
""")
    write(root / "docs/.mkdocs/docs-serve", """
#!/usr/bin/env sh
set -eu

COMMAND="${1:-serve}"
if [ "$#" -gt 0 ]; then
  shift
fi
REPO_ROOT="$(cd ../.. && pwd)"
IMAGE_NAME="${DOCKER_IMAGE_NAME:-dynamind-mkdocs}"

if command -v uvx >/dev/null 2>&1; then
  exec uvx --with mkdocs-material==9.7.2 --with mkdocs-mermaid2-plugin==1.3.0 --with pymdown-extensions==10.18.1 mkdocs "$COMMAND" "$@"
fi

if command -v docker >/dev/null 2>&1; then
  docker build -t "$IMAGE_NAME" .
  if [ "$COMMAND" = "serve" ]; then
    exec docker run --rm -p 8000:8000 -v "$REPO_ROOT:/work" "$IMAGE_NAME" "$COMMAND" --dev-addr=0.0.0.0:8000 "$@"
  fi
  exec docker run --rm -v "$REPO_ROOT:/work" "$IMAGE_NAME" "$COMMAND" "$@"
fi

echo "Install uv or Docker to build/serve docs." >&2
exit 1
""")
    (root / "docs/.mkdocs/docs-serve").chmod(0o755)
    write(root / "docs/index.md", f"""
# {project_name} Guide

Use this folder to keep humans and agents oriented.

- `architecture/brief.md`: concise architecture overview.
- `architecture/glossary.md`: ubiquitous language.
- `architecture/exceptions.md`: accepted deviations from the intended design.
- `architecture/adrs/`: structural decision records.
""")
    write(root / "docs/architecture/brief.md", f"""
# Architecture Brief

## Business Context

Describe the business problem, primary users, and operational setting.

## Goal

Deliver {project_name} as a maintainable full-stack application with a Quarkus backend and Vue frontend.

## System Context

```mermaid
flowchart LR
  User[User] --> Frontend[Vue frontend]
  Frontend --> Backend[Quarkus backend]
  Backend --> External[(External systems)]
```

## Container View

```mermaid
flowchart TB
  subgraph repo["{slug} monorepo"]
    FE["frontend: Vite/Vue 3"]
    BE["backend: Quarkus REST API"]
    DOCS["docs: onboarding and decisions"]
    INFRA["infra: Azure Terraform"]
  end
  FE -->|/api| BE
  BE -->|serves static build| FE
  INFRA --> Azure[Azure]
```

## Accepted Trade-offs

- The production frontend is packaged into the backend artifact for a single deployable unit.
- The frontend still runs independently during local development through Vite.

## Roadmap Notes

- Environments: {env_list}.
- Add database, identity, and deployment details when they are selected.
""")
    write(root / "docs/architecture/exceptions.md", """
# Architecture Exceptions

Document accepted deviations from the intended design.

Use this file for temporary PoC shortcuts, known constraints, and deliberate compromises so future agents do not mistake them for accidental brokenness.

| Date | Decision | Why accepted | Expiry or revisit trigger |
|---|---|---|---|
| TBD | TBD | TBD | TBD |
""")
    write(root / "docs/architecture/glossary.md", """
# Glossary

Define domain terms in technology-agnostic language.

| Term | Meaning | Notes |
|---|---|---|
| User | A person who uses the system to accomplish the primary job. | Replace with project-specific roles. |
""")
    write(root / "docs/architecture/adrs/README.md", """
# ADRs

Use ADRs for important, structural, hard-to-change-later decisions.

Do not write ADRs for routine feature-level choices.

File naming:

```text
000-description-of-the-decision.md
001-next-structural-decision.md
```
""")
    write(root / "docs/architecture/adrs/000-record-architecture-decisions.md", f"""
# 000 Record Architecture Decisions

## Status

Accepted

## Context

{project_name} needs a durable way to preserve important architectural context for humans and agents.

## Decision

Record important structural decisions as ADRs in this folder using a three-digit index.

## Consequences

- Agents can recover why major choices were made.
- Feature-level decisions stay out of ADRs unless they change the structure of the system.
""")


def create_infra(root: Path, slug: str, environments: list[str]) -> None:
    primary_env = environments[0] if environments else "dev"
    write(root / "infra/main.tf", f"""
terraform {{
  required_version = ">= 1.8.0"

  required_providers {{
    azurerm = {{
      source  = "hashicorp/azurerm"
      version = ">= 4.2.0"
    }}
    azurecaf = {{
      source  = "aztfmod/azurecaf"
      version = ">= 1.2.28"
    }}
  }}
}}

provider "azurerm" {{
  subscription_id      = var.subscription_id
  storage_use_azuread = true
  features {{}}
}}

resource "azurecaf_name" "resource_group" {{
  name          = var.application
  resource_type = "azurerm_resource_group"
  suffixes      = [var.environment]
}}

resource "azurerm_resource_group" "app" {{
  name     = azurecaf_name.resource_group.result
  location = var.location
  tags     = var.tags
}}

# Add App Service, Key Vault, monitoring, database, and managed identity resources
# once hosting and data requirements are known.
""")
    write(root / "infra/variables.tf", """
variable "subscription_id" {
  type        = string
  description = "Azure subscription ID."
}

variable "application" {
  type        = string
  description = "Short application name."
}

variable "environment" {
  type        = string
  description = "Deployment environment."
}

variable "location" {
  type        = string
  description = "Azure region."
  default     = "westeurope"
}

variable "tags" {
  type        = map(string)
  description = "Common Azure tags."
  default     = {}
}
""")
    write(root / "infra/outputs.tf", """
output "resource_group_name" {
  value = azurerm_resource_group.app.name
}
""")
    write(root / "infra/main.tfvars.json", f"""
{{
  "subscription_id": "00000000-0000-0000-0000-000000000000",
  "application": "{slug}",
  "environment": "{primary_env}",
  "location": "westeurope",
  "tags": {{
    "managedBy": "terraform",
    "application": "{slug}"
  }}
}}
""")
    write(root / "infra/README.md", """
# Infrastructure

Terraform starter for Azure.

Validate before planning:

```bash
terraform init
terraform validate
terraform plan -var-file=main.tfvars.json
```

Do not run `terraform apply` until resource naming, hosting, identity, database, and environment strategy are confirmed.
""")


def create_pipelines(root: Path, slug: str, environments: list[str]) -> None:
    env_yaml = "\n".join([f"      - {env}" for env in environments])
    write(root / "pipelines/build-ci.yml", """
trigger:
  branches:
    include:
      - main
      - feature/*

pr:
  branches:
    include:
      - main

pool:
  vmImage: ubuntu-latest

stages:
  - stage: Build
    jobs:
      - job: Build
        steps:
          - task: NodeTool@0
            inputs:
              versionSpec: '22.18.0'
          - script: |
              cd frontend
              npm ci
              npm run build
            displayName: Build frontend
          - task: JavaToolInstaller@0
            inputs:
              versionSpec: '21'
              jdkArchitectureOption: x64
              jdkSourceOption: PreInstalled
          - script: |
              cd backend
              mvn test package
            displayName: Test and package backend
          - publish: backend/target
            artifact: component
""")
    write(root / "pipelines/infra-deploy.yml", f"""
trigger: none
pr: none

parameters:
  - name: environment
    type: string
    default: {environments[0] if environments else "dev"}
    values:
{env_yaml}

pool:
  vmImage: ubuntu-latest

stages:
  - stage: Provision
    jobs:
      - deployment: Terraform
        environment: ${{{{ parameters.environment }}}}
        strategy:
          runOnce:
            deploy:
              steps:
                - checkout: self
                - task: AzureCLI@2
                  inputs:
                    azureSubscription: 'REPLACE_WITH_AZURE_SERVICE_CONNECTION'
                    scriptType: bash
                    scriptLocation: inlineScript
                    inlineScript: |
                      cd infra
                      terraform init
                      terraform validate
                      terraform plan -var-file=main.tfvars.json
                # Add a reviewed apply step after service connections and state are configured.
""")
    write(root / "pipelines/deploy-cd.yml", f"""
trigger: none
pr: none

resources:
  pipelines:
    - pipeline: ci
      source: {slug}-ci
      trigger:
        branches:
          include:
            - main

parameters:
  - name: environment
    type: string
    default: {environments[0] if environments else "dev"}
    values:
{env_yaml}

pool:
  vmImage: ubuntu-latest

stages:
  - stage: Deploy
    jobs:
      - deployment: Deploy
        environment: ${{{{ parameters.environment }}}}
        strategy:
          runOnce:
            deploy:
              steps:
                - download: ci
                  artifact: component
                - task: AzureCLI@2
                  inputs:
                    azureSubscription: 'REPLACE_WITH_AZURE_SERVICE_CONNECTION'
                    scriptType: bash
                    scriptLocation: inlineScript
                    inlineScript: |
                      echo "Deploy packaged backend artifact to the selected Azure host."
                      echo "Keep PR validation deployment-free."
""")
    write(root / "pipelines/README.md", """
# Pipelines

Recommended split:

- `build-ci.yml`: build and test only. No Azure deployment in CI or pull request validation.
- `infra-deploy.yml`: provision Azure resources after service connections and state are configured.
- `deploy-cd.yml`: deploy built artifacts to an existing environment.

Use Azure DevOps service connections backed by app registration and workload identity federation. Configure environment approvals and checks in Azure DevOps for staging and production.
""")


if __name__ == "__main__":
    sys.exit(main())
