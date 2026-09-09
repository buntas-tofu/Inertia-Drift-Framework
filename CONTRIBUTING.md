# Contributing to DMF

Forks, issues, and improvement suggestions are welcome. DMF is the result of several iterations, and pull requests are how the next iteration arrives.

## How to contribute

1. **Open an issue first** for substantive changes. Brief description of the problem and the approach you have in mind. This avoids parallel work and lets the framework evolve through discussion rather than surprise PRs.
2. **Fork the repository** and create a feature branch.
3. **Make your changes** in the appropriate directory:
   - `template/` for changes to the four artifacts that ship with the framework.
   - `examples/` for new examples or fixes to existing examples.
4. **Update `CHANGELOG.md`** with a brief note about your change in the `[Unreleased]` section.
5. **Open a PR** with a clear description: what changed, why, and what kind of change it is (PATCH, MINOR, or MAJOR per semver).

## Style

- No em dashes. No ellipses. DMF's own hard style constraint applied to its own materials.
- Match the tone of existing prose: direct, no marketing language, examples over abstractions where possible.
- Keep template content generic. If you need an example to illustrate, add a worked example under `examples/` rather than putting personal content in the template.

## What kinds of contributions are welcome

- Bug reports against the template files (broken pointers, unclear directives, ambiguous fences)
- Improvements to the bootstrap directives in `DMF:INITIAL` blocks
- Additional examples under `examples/` (if you have adopted DMF and want to publish your own filled-in template as a reference)
- Translation or localization of templates
- New escalation patterns, with rationale for why they should be project-scoped rather than universal

## What is out of scope

- Adding tier vocabulary back. DMF is a single build spec; tiered escalation models were deliberately compressed away. New escalations should be triggered by project-scoped decisions captured during `INITIAL`.
- Changing the four DMF Core Invariants (authority-in-files, halt on conflict, halt on missing authority, label inference) without first opening an issue and a discussion. These are load-bearing.
- Adding heavy tooling, build steps, or runtime dependencies. DMF is markdown and JSON by design.

## License

By contributing, you agree that your contributions are licensed under the project's MIT License. See [LICENSE](LICENSE).
