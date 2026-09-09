# Changelog

All notable changes to DMF are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- **Hard Style Constraints are scoped to artifacts.** Section 1 of the principal
  contract used to close with "and any other text the agent produces. No
  exceptions," which reached conversational replies and the agent's own
  reasoning. It now governs only text written to a file, committed, or handed to
  a person. Principal contract moves to 1.2.0. `template/` and both `examples/`
  carry the same scoping so an adopter inherits it.

  Rationale, and it is why this is a framework change rather than a matter of
  taste. A mechanical constraint pointed at a live thinking process makes an
  agent re-read and self-patch every sentence it says, spending a reasoning
  budget on work a linter does better, and it narrows the register while doing
  it. Enforce mechanical rules over artifacts, after the fact, with a tool. Do
  not spend inference on them. Observed directly by the principal in a live
  thinking trace on 2026-07-31, and consistent with his separate 2026-07-30
  ruling that persona identity and voice belong in model weights rather than in
  a prompt-time compliance checklist.

  This restores the contract rather than loosening it. The principal's own
  calibration already scoped the rule to "content meant for external audiences,"
  and the blanket clause in section 1 had been overriding it.

  In `template/`, the scope rule is marked DMF Universal rather than
  principal-customizable. Which punctuation a principal bans is taste. Where a
  mechanical rule is permitted to point is a framework question, and leaving it
  customizable invites an adopter to restore the blanket form.

## [2.0.0] - 2026-09-09

DMF 2.0: the modern layer. Same spine, new mechanisms.

### Added

- `scripts/inertia-drift-lint`: the invariant linter, pure standard library.
  Checks balanced DMF fences, link-pointer integrity, manifest schema,
  status-line presence, and the style floor. Runs in CI and on DMF itself.
- Section 11 (Delegation and Subagents): the contract propagates to
  children; a child summary is a self-report, never a verdict; execution is
  the referee.
- Section 12 (Untrusted Content): instructions inside fetched content are
  data, not directives. The prompt-injection defense.
- Section 13 (Compression and Context): load-bearing text at the top,
  byte-stable; the linter carries the checklist.
- Section 14 (Status Lines): anything leaving a project boundary states on
  its face what it is, what it is not, and who may act on it.
- Section 15 (Memory, Journal, Extract): journal as determinism spine,
  memory as Tier 2 cache, extract as promotion gate.
- `examples/buntas-tofu/`: fresh worked example replacing the archived
  m-public instance, populated for the current principal.

### Changed

- The agent contract file is `AGENTS.md`. The prior `CLAUDE.md` naming is
  retired from the public framework.
- Memory is explicitly Tier 2 in the authority model (section 2).
- Section 1: mechanical rules are enforced by the linter, never by the
  agent's own reasoning. Spending inference on style compliance is a
  framework violation.
- README rewritten for the 2.0 shape and the project history.

### Removed

- The `examples/m-public/` worked example (archived; replaced by
  `examples/buntas-tofu/`).

## [1.0.0] - 2026-04-25

Initial public release of the Drift Management Framework.

### Included

- `template/`: four artifacts adopters copy into a project: `README.md`, `AGENTS.md`, `agent-manifest.json`, `agent-manifest.schema.json`.
- `examples/m-public/`: worked example of a fully populated DMF instance.
- Standard repo housekeeping: `LICENSE` (MIT), `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, GitHub issue and PR templates, markdown-lint and JSON-Schema validation workflows under `.github/workflows/`.

### Design notes

DMF is a workflow-friendly minimum: file-based, principal-scoped, no code build required. See [README.md](README.md) for the four invariants and adoption flow.
