# 2.1.0 release notes

Status: Tagged release material for adopters and maintainers. GitHub release
publication is pending.

Version: **2.1.0**. Release date: **2026-10-25**. Verified tag: `v2.1.0`.
Release execution is tracked in [`c-0004`](board/cards/blocked/c-0004.toml).

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

Release commit: `be12b3406ff863ff3da4d7d69e9ed3ae7f221721`.
Its four required checks passed:
[drift, links, and markdown](https://github.com/buntas-tofu/Inertia-Drift-Framework/actions/runs/40206354366),
and [validate](https://github.com/buntas-tofu/Inertia-Drift-Framework/actions/runs/40206354321).

Annotated tag `v2.1.0`, object `6afb9cfb2e6f01e109bc561da53f68edb84d5efe`,
was pushed and verified to resolve to that exact release commit on 2026-10-25.
The release refs ruleset remains active; the tag will not be moved as later
board reconciliation advances main.

GitHub release creation was attempted with `gh release create --verify-tag`.
The CLI failed with `Post "https://api.github.com/graphql": Forbidden`.
An independent read through the connected GitHub app returned an empty
releases list after the attempt. Publication remains uncompleted.

Card `c-0004` is blocked awaiting an authorized API or UI path to publish
the existing tag. After publication is verified, close the card and regenerate
its views through the protected PR workflow without changing `v2.1.0`.
