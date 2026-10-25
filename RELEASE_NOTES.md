# 2.1.0 release notes (draft)

Status: Unreleased preparation for maintainer review. These notes do not record
a tag or published release; the maintainer decides when to release.

Target: **2.1.0**, from [`c-0004`](board/cards/ready/c-0004.toml).
Release date and tag are pending. The [changelog](CHANGELOG.md) remains
Unreleased until release execution.

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

## Version scope and release decisions

The release target and the bundled linter are 2.1.0. The root `AGENTS.md`
frontmatter is prepared for 2.1.0. Template and worked-example frontmatter,
manifest-file versions, sample-project versions, historical release entries,
and completed board cards retain their independent or historical values.

Before release, the maintainer still needs to:

- Confirm the planned 2.1.0 MINOR classification despite the expanded lint
  floor changing acceptance for existing adopters.
- Review the [adoption warning](README.md#how-to-adopt) against
  [`c-0005`](board/cards/shaping/c-0005.toml). The card remains open;
  documenting the warning does not approve a release.
- Review acceptance results on the final release commit, including the
  configured CI checks.
- Choose the release date and tag spelling, and execute tagging under the
  release refs ruleset before publication. Card `c-0004` stays open until
  its full release work is complete.
