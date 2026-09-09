---
title: ""
description: ""
date: "2026-04-25"
tags: []
owners: ["[principal]"]
status: "draft"
version: "0.2.0"
provenance:
  last_reviewed: ""
  sources: []
---

<!-- DMF:GLOBAL:START
  GLOBAL is the platform layer. Durable principal-level defaults that
  travel with every project under the same DMF binding. Configure once
  per principal (where principal is you, your team, or your organization).
  Every project inherits this section.

  Examples of content commonly placed in GLOBAL:
  - Ownership and contact information (below)
  - License defaults (below)
  - Required sections in standard documents (below)
  - Cross-project conventions and policies
  - Style rules (banned punctuation, voice constraints, etc.) typically
    live in the GLOBAL of AGENTS.md, but can land here if relevant to
    the README itself.

  Do not remove or modify the DMF:GLOBAL fences unless updating the
  master DMF template.
-->

# Project Ownership

- **Owner**: [your name, team name, or organization]
- **Contact**: [email, ticket queue, channel, etc.]
- **License**: [default license; LOCAL may override per project]

# README Standard

Every project README under this principal must contain the following
sections once populated. Sections may be reordered but not omitted. If
a section is genuinely not applicable, replace its content with a
one-line explanation of why.

Required sections: Project Identity, What This Is, Getting Started,
Architecture, Development, Dependencies, Versioning, License.

<!-- DMF:GLOBAL:END -->

<!-- DMF:INITIAL:START
  BOOTSTRAP DIRECTIVES - This entire block is removed after local
  content is populated and approved by the project owner. This includes
  updating all 'dmf' references to the name of the new project.

  TRIGGER: If this block exists, the agent is in bootstrap mode.
  Do not operate on the project until bootstrap is complete.

  PHASE 1 - DISCOVERY
  Scan the repository for the following. Record what you find and
  what you do not find.

  Project identity sources (check in order, use first match):
    - package.json (name, version, description)
    - pyproject.toml (project.name, project.version, project.description)
    - Cargo.toml ([package] name, version, description)
    - go.mod (module path)
    - *.csproj (PropertyGroup > AssemblyName, Version)
    - pom.xml (groupId, artifactId, version)
    - setup.py / setup.cfg (name, version)
    - Any existing README.md content

  Architecture sources:
    - Directory tree (top two levels)
    - Dockerfile / docker-compose.yml
    - CI/CD configs (.github/workflows/, .gitlab-ci.yml, Jenkinsfile)
    - Entry point files (main.*, index.*, app.*, server.*)

  Development workflow sources:
    - CONTRIBUTING.md
    - Makefile / Taskfile / justfile
    - package.json scripts
    - Pre-commit config (.pre-commit-config.yaml)
    - Test configuration (jest.config.*, pytest.ini, etc.)

  Dependency sources:
    - Lock files (package-lock.json, yarn.lock, poetry.lock, Cargo.lock, go.sum)
    - Manifest files (same as project identity sources)

  Discovery output handling:
    - Record what you find and what you do not find.
    - If discovery surfaces conflicting signals (e.g., two different
      project names, mismatched versions between manifest and README,
      inconsistent documentation of the same system), capture each
      conflict explicitly and feed it into Phase 2 as a disambiguation
      question for the project owner. Do not silently pick one.

  PHASE 2 - INTERVIEW
  For any required section not populatable from discovery, ask the
  project owner directly. Do not infer content. Do not leave sections
  blank. Ask specific questions, not open-ended ones.

  Minimum interview questions if no existing docs are found:
    1. What does this project do, in one or two sentences?
    2. Who is it for?
    3. What are the prerequisites to run it?
    4. Is there anything an agent should know about the architecture
       that is not obvious from the directory structure?

  Versioning interview (run for every project, regardless of discovery):

  Ask the owner:

  1. Do you want version pinning enforced for this project?
     - yes: Cargo.lock, Pipfile.lock, Docker tags like nginx:1.25.3.
     - no: quick bash scripts, notebook prototypes.

  2. What versioning scheme will this project use?
     - semver (1.2.3): React, Express, lodash.
     - calver (2026.04, 24.10): Ubuntu, Windows 11, pip.
     - custom (6.5.10, 3.141592): Linux kernel, TeX.
     - none: a one-off bash script.

  3. If semver, what is your bumping policy?
     - strict-consumer-contract: React, Stripe SDK.
     - liberal: an internal dashboard your team alone uses.
     - internal-only: anything 0.x.y still taking shape.
     - undefined: say so, instead of letting the agent pretend.

  Record answers in LOCAL under "Versioning Policy." These become
  the project's binding version policy after INITIAL is cleaned.
  Changes later happen in LOCAL, not in conversation.

  PHASE 3 - POPULATE
  Fill each local section below with discovered and interviewed content.
  Keep language direct. No filler. Match the principal's voice if a
  voice contract is defined in AGENTS.md.

  PHASE 4 - REVIEW GATE
  Present the populated README to the project owner. Do not remove
  this initial block until the owner explicitly approves. If the owner
  requests changes, make them and re-present.

  PHASE 5 - CLEAN
  Upon approval, delete everything between DMF:INITIAL:START and
  DMF:INITIAL:END, including the fences themselves. Update the
  frontmatter date and status fields. Commit with message:
  "DMF: bootstrap README complete"

  STACK-SPECIFIC HINTS
  If you need to add discovery heuristics for a stack not listed above,
  append them to the discovery phase before running. Do not modify the
  master DMF template; add hints inline for this project only.
-->
<!-- DMF:INITIAL:END -->

<!-- DMF:LOCAL:START -->

# [Project Name]

> [One-line description]

![Version](https://img.shields.io/badge/version-0.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-draft-orange.svg)

## What This Is

[2-3 sentences. What problem does this solve? For whom? What is the
core value proposition?]

## Getting Started

### Prerequisites

[What needs to be installed before this project can run.]

### Installation

[Step-by-step install commands.]

### First Run

[How to verify the project works after installation.]

## Architecture

[High-level structure. Key directories and what they contain.
Entry points. Data flow if applicable. Keep it scannable.]

```
[directory tree or diagram placeholder]
```

## Development

[How to contribute. Branch strategy. Test commands. Linting.
CI/CD expectations. Code review process.]

## Dependencies

[Key dependencies and why they exist. Not an exhaustive list;
point to the lock file for that. Call out anything non-obvious
or load-bearing.]

## Versioning

This project uses [versioning scheme]. Current version: [version].
Bumping policy: [strict-consumer-contract / liberal / internal-only / undefined].

See [CHANGELOG.md](CHANGELOG.md) for release history.

## License

[License type]. See [LICENSE](LICENSE) for details.

<!-- DMF:LOCAL:END -->
