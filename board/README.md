# The board

A project board that lives in your repository as files, so the work and the
governance are in the same place and the same history.

This is a template. It ships with DMF because a framework that governs
agent-assisted work should be able to show its own work, and because a board is
the cheapest honest answer to "what is actually happening" that does not
require a service, an account, or a database.

## Why files

Every property below is a consequence of one decision: the card is a file in
git, and every view is generated from those files.

- **The diff is the audit trail.** A card that moved is a rename. A card that
  changed is a diff. Nobody has to trust a status field, because the history
  says when it moved and the commit says why.
- **No shared register, so no merge conflict.** One card, one file. Two agents
  working on unrelated cards never touch the same bytes.
- **Readable with no tooling.** `cat cards/active/c-0001.toml` works on a
  machine with no network, no service, and no account.
- **Every actor is equal.** An agent writing a card and a human writing a card
  produce the same kind of object, through the same tools, under the same gate
  if you have one.

## Five minute adoption

```sh
cp -r board/ /path/to/your-repo/board
cd /path/to/your-repo/board
python3 tools/board.py validate
python3 tools/board.py new-card --title "First real card" --lane governance/rules
python3 tools/board.py index
git add -A && git commit -m "board: adopt the DMF project board"
```

Then edit `lanes.toml` to your own areas and `board.toml` if you want different
columns. Nothing in the tool assumes this template's vocabulary.

## The shape

```
board.toml                 the declaration: columns, horizons, lane levels
lanes.toml                 the lane tree, and it nests
cards/<column>/<id>.toml   one card per file, one column per card
projects/<slug>/           optional: a named effort cards roll up to
BOARD.md                   generated reading, says when it was taken
index/board.json           generated machine reading
tools/board.py             the operator tool, standard library only
```

A card carries an id, a title, a lane path, a column, an owner, an authority
tier, a horizon, links, and a note. Optional fields cover distribution
(`platform`, `workers`, `models`), decomposition (`subtasks`), dependencies
(`blocked_by`), and what it is waiting on (`awaiting`).

The lane tree is the classification axis and the column is the flight axis.
They are independent on purpose: a board that merges them cannot answer "what
moved in governance this week" and "what is actually in progress" at once.

## The floor is enforced here

`validate` fails a card that carries an em dash, an en dash, an ellipsis, or a
curly quote, and it names the file and the character. It also fails a card with
no authority tier, because an unlabeled claim is the thing the framework exists
to prevent.

That is the whole reason this template ships with DMF rather than as a separate
tool: the board is where artifacts get written, so the board is where the floor
gets checked.

## The one command that matters

```sh
python3 tools/board.py stale
```

It prints three things and nothing else: what is waiting on the operator, what
is blocked, and what has gone quiet while still marked in flight. If your
morning needs a single board read, that is the read.

## What this is not

It is not a tracker with a server. It is not a replacement for issues, and it
does not need one: a projection script that turns cards into issues is a
reasonable extension, and the files stay the record either way. It is not a
second authority model; it reuses whatever gate you already have, because a
write to `cards/` is an ordinary file write.

## Extending it

Two extensions are worth knowing about because they keep the one-way rule:

- **A projection.** Read the cards, write something else (issues, a site, a
  chat message). Never read that thing back as authority.
- **A generated mirror.** Translate the cards into another tool's shape, in a
  directory that tool does not scan, so the other surface can read without
  becoming a second store.

Both are one-way. The moment a projection writes back, you have two records and
a conflict rule to maintain, which is the cost this design exists to avoid.
