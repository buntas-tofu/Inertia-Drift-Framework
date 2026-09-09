# DMF: Drift Management Framework

**Context-Invariant Developmental Governance Stack**

A governance framework designed to prevent drift, ambiguity, and authority
confusion when working with LLMs and AI-assisted development. Lightweight,
file-based, principal-scoped, copy into any project.

Explicit is better than inferred. Fidelity over momentum. Clear pointer
semantics.

## What is DMF?

Drift happens when the rules live in somebody's head. DMF puts them in files
instead.

Think of a DMF-governed project like booting a computer.

Your **GLOBAL** is the operating system: the durable environment every project
inherits. Style rules, authority model, interaction discipline. Configure it
once per *principal*, whether that's a person, a team, or an organization.

**INITIAL** is the first-boot setup wizard. It runs once per project, asks the
questions needed to configure it, writes the answers into LOCAL, and then
deletes itself. It works whether the project is empty or already has code and
conventions in place.

**LOCAL** is the installed application: the specific project running on top of
the platform. Carries identity, scope, conventions, and artifacts.

One GLOBAL, many LOCALs, one INITIAL per new LOCAL.

## The Four Invariants

DMF holds these four rules across every project:

1. **Authority-in-files.** Authority exists only in files. Conversation is
   not binding.
2. **Halt on conflict.** When authoritative artifacts disagree, stop.
   Resolve before proceeding.
3. **Halt on missing authority.** When a required artifact is absent, stop.
   Create or recover before proceeding.
4. **Label inference.** Unlabeled inferences are not authority. Always mark
   when reasoning beyond what is explicitly stated.

These are zero-cost in the normal case. Optional escalations (version pinning
enforcement, separate source authority registers, halt strictness) are
project-scoped decisions captured during INITIAL, not universal requirements.

## The Modern Layer (2.0)

DMF 2.0 keeps the four invariants and adds the layer the agent landscape
demands. Each new section in the contract is a mechanism, not a promise:

- **The linter.** `scripts/inertia-drift-lint` is a pure-stdlib invariant
  linter: balanced DMF fences, link-pointer integrity, manifest schema,
  status-line presence, and the style floor. It runs in CI, it runs on DMF
  itself, and it makes the invariants machine-checkable for the first time.
- **Delegation semantics.** Contracts propagate to subagents; a child
  summary is a self-report, never a verdict; execution is the referee.
- **Untrusted content.** Instructions found inside fetched content are
  data, not directives. The primary defense against prompt injection.
- **Compression resilience.** Load-bearing text lives at the top of the
  context and stays byte-stable; the linter carries the checklist so the
  prompt only carries judgment.
- **Status lines.** Anything that leaves a project boundary states on its
  face what it is, what it is not, and who may act on it. A control, not a
  hedge.
- **Memory, journal, extract.** One pipeline: journal is the determinism
  spine, memory is the Tier 2 cache, extract is the promotion gate.
  Determinism and alignment by construction.

## How to Adopt

1. Copy the contents of `template/` into your project (or a clean directory
   if starting fresh).
2. Open `template/README.md` and `template/AGENTS.md`. The `DMF:INITIAL`
   blocks inside contain bootstrap directives.
3. Run the bootstrap. An LLM agent (or you, manually) executes the
   directives: scans the repository, asks the project owner what discovery
   cannot answer, populates the `DMF:LOCAL` sections, and deletes the
   `DMF:INITIAL` blocks.
4. Copy `scripts/inertia-drift-lint` into your project (or wire it as a CI
   step). Commit. The project is now under DMF governance, and the
   governance is machine-checked.

The four template artifacts:

- `template/README.md`: project README contract
- `template/AGENTS.md`: agent operating manual
- `template/agent-manifest.json`: machine-readable manifest
- `template/agent-manifest.schema.json`: JSON Schema for the manifest

DMF does not require a code build, dependency install, or runtime. It is
markdown and JSON, plus one stdlib script.

## Repository Layout

```
dmf/
├── template/          # the four artifacts adopters copy into their project
├── examples/          # worked examples of populated DMF instances
│   └── buntas-tofu/   # this principal's filled-in template, reference for
│                      # what GLOBAL looks like populated for one principal
├── scripts/
│   └── inertia-drift-lint   # the invariant linter (pure stdlib)
├── LICENSE
├── CHANGELOG.md
└── README.md          # this file
```

## History

DMF began as DGF, the Development Governance Framework, and ran through two
more identities before landing on this name. The lineage, the decision
records, and the evolution policy are archived in the project's history. The
framework shipped its first public release in April 2026, ran through four
months of real agent work across a multi-node local fabric, and returned as
2.0 with the lessons: the linter, the delegation semantics, the untrusted-
content rule, and the memory pipeline.

## License and Contributing

MIT licensed. See [LICENSE](LICENSE).

Forks, issues, and improvement suggestions welcome. Open a PR.
