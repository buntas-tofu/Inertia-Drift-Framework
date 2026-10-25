# 2.1.0 release notes

Status: Final release material for maintainer execution. Tagging and GitHub
publication are pending verification.

Version: **2.1.0**. Release date: **2026-10-25**. Intended tag: `v2.1.0`.
Release execution is tracked in [`c-0004`](board/cards/active/c-0004.toml).

## Adopter impact: the lint floor reaches more artifacts

**An existing project can fail its next lint without changing its own files.**
The 2.1.0 linter expands the style-floor scan beyond markdown to plain text,
YAML, JSON, TOML, INI, and common source formats. Previously unchecked em dashes
and ellipsis characters in those artifacts now fail the check. The floor walk
also includes `examples/`, `tests/`, and `archive/`.

Captured CSV and TSV data, dependency trees, build output, and run-receipt
directories remain outside the floor scan. Hard style constraints govern
artifacts, including code comments, rather than conversational replies or the
agent's reasoning.

The [How to Adopt guide](README.md#how-to-adopt) places this warning before
the linter-copy step and includes the validation commands.

Before adopting the updated linter:

1. Review the formats and exclusions in `FLOOR_SUFFIXES` and
   `FLOOR_IGNORE_DIRS` in `scripts/inertia-drift-lint`.
2. Copy the updated script into the adopting project and run:

   ```sh
   python3 scripts/inertia-drift-lint --version
   python3 scripts/inertia-drift-lint .
   ```

3. Confirm the version command reports `inertia-drift-lint 2.1.0`. Use the
   findings to fix the characters in affected artifacts, then rerun lint.
   Do not narrow the floor check to hide violations.

## Other changes

- **Optional project board.** `board/` ships a file-based card store, nested
  lanes, a validator, generated views, and an adoption guide. Its six starting
  cards are this repository's backlog. See [board/README.md](board/README.md).
- **Public name.** The repository is now `buntas-tofu/Inertia-Drift-Framework`.
  DMF remains the short name; the former repository URL redirects.
- **Artifact scope.** Hard Style Constraints are scoped to artifacts in the
  principal contract, template, and worked example.

## Version scope and MINOR classification

The release and the bundled linter are 2.1.0. The root `AGENTS.md`
frontmatter is 2.1.0. Template and worked-example frontmatter,
manifest-file versions, sample-project versions, historical release entries,
and completed board cards retain their independent or historical values.

The maintainer's 2026-10-25 finish approval retains the planned 2.1.0 MINOR.
The 2.0 contract already applied the style floor to persisted artifacts,
including code comments. The expanded scan corrects enforcement of that
existing policy, and the optional project board adds functionality. This is
the classification basis, rather than the absence of CLI argument or manifest
schema changes.

**Lint acceptance is stricter.** Previously passing projects can now fail on
unchanged files. That compatibility impact is explicit in the adoption
warning and the guidance above.

The [adoption warning](README.md#how-to-adopt) was accepted for this release
after [PR #3](https://github.com/buntas-tofu/Inertia-Drift-Framework/pull/3)
merged. Its record is [`c-0005`](board/cards/done/c-0005.toml).

## Release execution

The release commit must pass `drift`, `links`, `markdown`, and `validate`
before tagging and publication. The active release refs ruleset protects tags
against deletion and non-fast-forward updates. Card `c-0004` remains active
until the `v2.1.0` target and published GitHub release are verified; the tag
will remain fixed if a later board reconciliation advances main.
