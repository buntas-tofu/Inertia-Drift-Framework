# Board

Generated 2026-10-25 15:25:44 by `tools/board.py index`. This is a view, not the truth.
The truth is one TOML file per card under `cards/`. If a card moved since
this stamp, this page is wrong and the file is right.

**6 cards** in 2 columns, across 11 declared lanes.

## Flight

### inbox (0)

_empty_

### shaping (0)

_empty_

### ready (0)

_empty_

### active (0)

_empty_

### blocked (1)

| id | title | lane | owner | tier |
|---|---|---|---|---|
| c-0004 | Release 2.1.0: version bump, tag, and release notes | release/versioning | maintainer | 1 |

### review (0)

_empty_

### done (5)

| id | title | lane | owner | tier |
|---|---|---|---|---|
| c-0005 | Adoption note for the 2.1.0 floor expansion | adoption/docs | maintainer | 1 |
| c-0006 | Ship the board as a DMF template | adoption/template | maintainer | 1 |
| c-0001 | The style floor covers every text artifact format | governance/floor | maintainer | 1 |
| c-0003 | Hard Style Constraints are scoped to artifacts | governance/rules | maintainer | 1 |
| c-0002 | The public name is Inertia-Drift-Framework | release/publishing | maintainer | 1 |

## Lanes

Counts roll up: a parent lane includes everything nested under it.

| lane | level | inbox | shaping | ready | active | blocked | review | done | total |
|---|---|---|---|---|---|---|---|---|---|
| governance | area | . | . | . | . | . | . | 2 | 2 |
| governance/rules | topic | . | . | . | . | . | . | 1 | 1 |
| governance/linter | topic | . | . | . | . | . | . | . | 0 |
| governance/floor | topic | . | . | . | . | . | . | 1 | 1 |
| adoption | area | . | . | . | . | . | . | 2 | 2 |
| adoption/docs | topic | . | . | . | . | . | . | 1 | 1 |
| adoption/template | topic | . | . | . | . | . | . | 1 | 1 |
| adoption/examples | topic | . | . | . | . | . | . | . | 0 |
| release | area | . | . | . | . | 1 | . | 1 | 2 |
| release/versioning | topic | . | . | . | . | 1 | . | . | 1 |
| release/publishing | topic | . | . | . | . | . | . | 1 | 1 |

## Blocked

- **c-0004** Release 2.1.0: version bump, tag, and release notes. Tag v2.1.0 was created and verified on 2026-10-25. Annotated tag object 6afb9cfb2e6f01e109bc561da53f68edb84d5efe resolves to release commit be12b3406ff863ff3da4d7d69e9ed3ae7f221721; drift, links, markdown and validate passed on that exact commit. GitHub release creation failed at the CLI GraphQL route with Forbidden. The connector releases API confirms no release was created. Publication awaits an authorized API or UI path; do not move the existing tag. Close this card only after published release verification.

