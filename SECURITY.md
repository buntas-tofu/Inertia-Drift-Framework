# Security Policy

This policy covers the DMF framework as published in this repository: the template artifacts in `template/`, the worked example in `examples/`, the schemas, and the documentation. It does not cover downstream projects that have adopted DMF; those are the responsibility of their respective maintainers.

## Reporting a Vulnerability

The primary channel for reporting security issues is **GitHub Security Advisories** for this repository:

https://github.com/buntas-tofu/dmf/security/advisories/new

Reports submitted through Security Advisories are private to the maintainer and the reporter while the issue is being investigated. Please use this channel rather than opening a public Issue.

When you report, please include:

1. A description of the vulnerability and its impact.
2. A reproduction recipe (steps, manifest snippet, or sample directive that triggers the issue).
3. The DMF version or commit SHA you observed it on.
4. Your assessment of severity, if you have one.

What to expect:

- Acknowledgment within 7 days of report.
- Status updates at meaningful milestones throughout investigation.
- Public credit to you on the resulting advisory unless you request to remain anonymous.

If GitHub Security Advisories is unavailable to you, open a placeholder Issue titled "Security report pending" without any vulnerability details, and the maintainer will reach out to establish a private channel.

## Security Update Policy

DMF follows semantic versioning. Security fixes ship as PATCH releases against the current MINOR. Only the latest MINOR of the current MAJOR is supported.

| Version | Supported     |
| ------- | ------------- |
| 1.x     | yes (current) |
| < 1.0   | no            |

When a security fix is published:

- The corresponding GitHub Release notes call it out explicitly.
- The `CHANGELOG.md` entry is prefixed `Security:`.
- A GitHub Security Advisory is published, with a CVE assigned where applicable.

For coordinated disclosure of high-severity issues, the default window is 90 days from initial report to public advisory. Severe or actively exploited issues may be disclosed sooner; complex fixes may extend the window with reporter agreement.

## Security-Related Configuration

DMF is a governance framework. The framework itself *is* the security posture for LLM-assisted development under DMF. Adopters should understand the following before deploying it:

**The four invariants are the load-bearing protections.** Authority-in-files, halt on conflict, halt on missing authority, and label inference together prevent the most common drift modes when humans and agents share a project. Removing any of them removes a defense.

**Conversation is not binding.** Authority exists only in files. Out-of-band instructions delivered through chat, comments, or any other ephemeral channel do not bind the agent under DMF. This is the primary defense against prompt injection through user-facing surfaces. Adopters who route conversational requests around the file-based authority model defeat this defense.

**Optional escalations are available and should be considered per-project.** During `DMF:INITIAL` bootstrap, projects can opt in to:

- Version pinning enforcement (block changes to pinned dependencies without an authority artifact).
- Separate source authority registers (split read-only references from authoritative artifacts).
- Halt strictness (treat any unresolved halt as a hard stop, no soft continuation).

These are not universal because they are not free; they add friction. They are the right default for higher-stakes environments and should be opted into deliberately.

**`examples/buntas-tofu/` is a worked reference, not a default template.** Adopters must populate their own GLOBAL during `DMF:INITIAL`. Copying the example wholesale binds your project to another principal's style, register, and conventions.

**The JSON Schema validates manifest shape, not semantic correctness.** A manifest that passes `agent-manifest.schema.json` may still encode bad authority decisions or contradict the GLOBAL. Schema conformance is necessary but not sufficient.

## Known Security Gaps and Future Enhancements

DMF is honest about the limits of what it currently enforces. The following are known gaps:

**Invariants are agent-honored, not mechanically enforced.** DMF assumes the executing agent honestly labels inference and respects halt directives. A misaligned or compromised agent can violate the invariants without DMF noticing. Mitigation: human review of agent actions on consequential changes; do not run agents unattended in high-stakes contexts.

**`DMF:INITIAL` bootstrap directives execute in the host agent's permission context.** DMF does not sandbox file writes, command execution, or repository modification performed during bootstrap. Adopters should review the directives in any `DMF:INITIAL` block before running it, especially in templates pulled from sources other than this repository.

**No automated invariant linter exists yet.** Planned. Until one ships, invariant compliance is verified by the agent or by human review.

**No automated pointer-integrity check exists yet.** Planned. References between GLOBAL, LOCAL, and `agent-manifest.json` are currently verified at read time by the agent, not at commit time by tooling.

**Adoption review is the responsibility of the adopter.** Blind adoption is not safe adoption. Read the template files and the populated GLOBAL before committing them to your project.

## Maintainer

This policy and the channels above are maintained by buntas-tofu and DMF Contributors. Updates to the policy are versioned with the framework and announced in `CHANGELOG.md`.
