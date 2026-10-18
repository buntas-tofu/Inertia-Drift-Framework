#!/usr/bin/env python3
"""board.py - the DMF project board's one tool.

The truth is files in git. Every door (this CLI, BOARD.md, a GitHub projection,
a downstream reader) is a view of those files.

Shape, and why:

  cards/<column>/<id>.toml   one card per file. The column is a directory, so a
                             move is a `git mv` and the board's history is the
                             repository's history. Two cards cannot conflict in
                             a shared register because there is no register.

  lanes.toml                 the classification axis, and it NESTS. The tool
                             reads it; it never assumes a lane exists.

  board.toml                 the declaration: columns, horizons, lane levels,
                             and the vocabularies validate enforces.

The style floor is enforced HERE, not by hope. An artifact written to this board
carries the DMF floor: no em dashes, no en dashes, no ellipses, no curly quotes.
A card that breaks it fails validation with the file and the character named.

Stdlib only (tomllib reads, a small writer emits). Deterministic output.

Commands:
  validate                       check every file parses and agrees with itself
  index                          regenerate BOARD.md and index/board.json
  list                           cards, optionally filtered
  show <id>                      one card in full
  lanes                          the lane tree, with own and rolled-up counts
  stale                          rulings, blocked, and work gone quiet
  new-card --title T --lane L    create a card
  new-project --name N           create projects/<slug>/project.toml
  move <id> <column>             git mv a card between columns
  set <id>                       change note, owner, awaiting, horizon or tier

Exit codes: 0 ok, 1 validation failures or refused input, 2 usage.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "cards"
PROJECTS = ROOT / "projects"
INDEX = ROOT / "index"
BOARD_TOML = ROOT / "board.toml"

CARD_ORDER = ("id", "title", "lane", "project", "state", "owner", "tier",
              "horizon", "awaiting", "platform", "workers", "models", "subtasks",
              "links", "blocked_by", "created", "updated", "note")
PROJECT_ORDER = ("name", "id", "owner", "tier", "lane", "status", "repo",
                 "location", "summary", "created", "updated")

ACTIVE_COLUMNS = ("shaping", "ready", "active")

# The DMF floor, as characters. A card is an artifact, so it obeys the floor.
FLOOR_CHARS = {
    "\u2014": "em dash",
    "\u2013": "en dash",
    "\u2026": "ellipsis",
    "\u2018": "curly single quote",
    "\u2019": "curly apostrophe",
    "\u201c": "curly double quote",
    "\u201d": "curly double quote",
}


def today() -> str:
    return time.strftime("%Y-%m-%d")


# --- config ------------------------------------------------------------------

def board_config() -> dict:
    with BOARD_TOML.open("rb") as fh:
        return tomllib.load(fh)


def columns() -> tuple[str, ...]:
    return tuple(board_config().get("columns") or ())


def horizons() -> tuple[str, ...]:
    return tuple(board_config().get("horizons") or ())


def lane_levels() -> tuple[str, ...]:
    return tuple(board_config().get("lane_levels") or ())


def awaiting_values() -> tuple[str, ...]:
    return tuple(board_config().get("awaiting_values") or ())


def terminal_columns() -> tuple[str, ...]:
    return tuple(board_config().get("terminal_states") or ("done",))


def link_base() -> Path:
    """Where a relative link resolves from.

    A board that lives at the repository root wants `.`. A board that ships in a
    subdirectory, as this template does, wants `..`, because the documents a card
    cites (README, CHANGELOG, docs) live at the root. It is declared rather than
    guessed so a reader never has to know where this file sits.
    """
    raw = board_config().get("link_base") or "."
    return (ROOT / str(raw)).resolve()


def lanes() -> list[dict]:
    """The declared lanes in depth-first tree order, siblings by `order`."""
    cfg = board_config()
    path = ROOT / (cfg.get("lanes_file") or "lanes.toml")
    if not path.exists():
        return []
    with path.open("rb") as fh:
        data = tomllib.load(fh)
    raw = list(data.get("lane") or [])
    children: dict[str, list[dict]] = {}
    for lane in raw:
        p = lane.get("path", "")
        parent = p.rsplit("/", 1)[0] if "/" in p else ""
        children.setdefault(parent, []).append(lane)
    out: list[dict] = []

    def walk(parent: str) -> None:
        for lane in sorted(children.get(parent, []),
                           key=lambda x: (x.get("order", 1000), x.get("path", ""))):
            out.append(lane)
            walk(lane.get("path", ""))

    walk("")
    seen = {l.get("path") for l in out}
    out += [l for l in raw if l.get("path") not in seen]
    return out


def lane_paths() -> tuple[str, ...]:
    return tuple(l["path"] for l in lanes() if "path" in l)


def lane_by_path(path: str) -> dict | None:
    for lane in lanes():
        if lane.get("path") == path:
            return lane
    return None


def lanes_under(path: str) -> list[dict]:
    return [l for l in lanes()
            if l.get("path") == path or l.get("path", "").startswith(path + "/")]


def lane_is_valid(lane: str) -> tuple[bool, str]:
    segments = lane.split("/")
    levels = lane_levels()
    for depth, _ in enumerate(segments):
        prefix = "/".join(segments[:depth + 1])
        declared = lane_by_path(prefix)
        if declared is None:
            return False, f"{prefix!r} is not declared in lanes.toml"
        if depth >= len(levels):
            return False, f"{prefix!r} is deeper than the declared levels {levels}"
        if declared.get("level") != levels[depth]:
            return False, (f"{prefix!r} is level {declared.get('level')!r} "
                           f"but depth {depth + 1} means {levels[depth]!r}")
    return True, ""


# --- writing -----------------------------------------------------------------

def _q(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    s = str(v).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{s}"'


def dumps(fields: dict, order: tuple, header: str) -> str:
    lines = [f"# {header}"]
    for key in order:
        if key not in fields:
            continue
        val = fields[key]
        if isinstance(val, (list, tuple)):
            lines.append(f"{key} = [{', '.join(_q(i) for i in val)}]")
        else:
            lines.append(f"{key} = {_q(val)}")
    return "\n".join(lines) + "\n"


def loads(path: Path) -> dict:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def write_card(path: Path, fields: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dumps(fields, CARD_ORDER, "the project board - generated by tools/board.py"),
                    encoding="utf-8")


def write_project(path: Path, fields: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dumps(fields, PROJECT_ORDER, "the project board - generated by tools/board.py"),
                    encoding="utf-8")


# --- addressing --------------------------------------------------------------

def slug(name: str) -> str:
    return name.strip().lower().replace("_", "-").replace(" ", "-")


def next_id(prefix: str, existing: list[str]) -> str:
    top = 0
    for name in existing:
        body = Path(name).stem.split("-", 1)[-1]
        if body.isdigit():
            top = max(top, int(body))
    return f"{prefix}-{top + 1:04d}"


def all_cards() -> list[tuple[Path, dict]]:
    out = []
    if not CARDS.exists():
        return out
    for path in sorted(CARDS.glob("*/*.toml")):
        out.append((path, loads(path)))
    return out


def card_by_id(card_id: str) -> tuple[Path, dict] | None:
    for path, card in all_cards():
        if card.get("id") == card_id:
            return path, card
    return None


def all_projects() -> list[tuple[Path, dict]]:
    out = []
    if not PROJECTS.exists():
        return out
    for path in sorted(PROJECTS.glob("*/project.toml")):
        out.append((path, loads(path)))
    return out


def project_slugs() -> tuple[str, ...]:
    return tuple(p.parent.name for p, _ in all_projects())


def git_mv(src: Path, dst: Path) -> None:
    """Move through git when the repo owns both paths, plain rename otherwise.

    `git mv` refuses a destination directory that does not exist, so the parent
    is created first. Without that the fallback leaves a delete plus an
    untracked file, which is the same end state and loses the rename in history.
    """
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(["git", "mv", str(src.relative_to(ROOT)), str(dst.relative_to(ROOT))],
                       cwd=ROOT, check=True, capture_output=True, text=True)
    except (subprocess.CalledProcessError, ValueError):
        src.rename(dst)


def floor_breaches(text: str) -> list[str]:
    return [name for ch, name in FLOOR_CHARS.items() if ch in text]


# --- commands ----------------------------------------------------------------

def cmd_validate(args) -> int:
    bad: list[str] = []
    cfg_cols, cfg_horizons, cfg_levels = columns(), horizons(), lane_levels()
    seen_cards: dict[str, Path] = {}
    seen_projects = set(project_slugs())
    seen_lanes: set[str] = set()

    if not cfg_cols:
        bad.append("board.toml declares no columns")
    if not cfg_levels:
        bad.append("board.toml declares no lane_levels")

    for lane in lanes():
        path = lane.get("path", "")
        if not path:
            bad.append("lanes.toml: a lane has no path")
            continue
        if path in seen_lanes:
            bad.append(f"lanes.toml: duplicate path {path!r}")
        seen_lanes.add(path)
        ok, why = lane_is_valid(path)
        if not ok:
            bad.append(f"lanes.toml: {path!r}: {why}")
        for field in ("title", "level"):
            if not lane.get(field):
                bad.append(f"lanes.toml: {path!r} has no {field}")

    for path, card in all_cards():
        rel = path.relative_to(ROOT)
        column = path.parent.name
        cid = card.get("id", "")
        if column not in cfg_cols:
            bad.append(f"{rel}: unknown column directory {column!r}")
        if card.get("state") != column:
            bad.append(f"{rel}: state={card.get('state')!r} does not match column {column!r}")
        if not cid:
            bad.append(f"{rel}: no id")
        elif cid != path.stem:
            bad.append(f"{rel}: id {cid!r} does not match filename {path.stem!r}")
        elif cid in seen_cards:
            bad.append(f"{rel}: duplicate id {cid} (also {seen_cards[cid]})")
        else:
            seen_cards[cid] = rel
        if not card.get("title"):
            bad.append(f"{rel}: no title")

        lane = card.get("lane", "")
        if not lane:
            bad.append(f"{rel}: no lane")
        else:
            ok, why = lane_is_valid(lane)
            if not ok:
                bad.append(f"{rel}: lane {why}")

        proj = card.get("project")
        if proj and proj not in seen_projects:
            bad.append(f"{rel}: project {proj!r} has no projects/{proj}/project.toml")

        horizon = card.get("horizon")
        if horizon and horizon not in cfg_horizons:
            bad.append(f"{rel}: unknown horizon {horizon!r}")

        tier = card.get("tier")
        if tier not in (1, 2, 3):
            bad.append(f"{rel}: tier {tier!r} must be 1, 2 or 3 (authority is never unlabeled)")

        awaiting = card.get("awaiting", "")
        if awaiting and awaiting not in awaiting_values():
            bad.append(f"{rel}: unknown awaiting value {awaiting!r}")

        for link in card.get("links") or []:
            if isinstance(link, str) and not link.startswith(("http://", "https://")):
                if not (link_base() / link).exists():
                    bad.append(f"{rel}: link does not resolve from {link_base()}: {link}")

        blockers = card.get("blocked_by") or []
        for blocker in blockers if isinstance(blockers, (list, tuple)) else [blockers]:
            if blocker and not card_by_id(str(blocker)):
                bad.append(f"{rel}: blocked_by {blocker!r} does not resolve to a card")

        subs = card.get("subtasks") or []
        if not isinstance(subs, (list, tuple)):
            bad.append(f"{rel}: subtasks must be a list")
        elif any(not isinstance(s, str) for s in subs):
            bad.append(f"{rel}: every subtask must be a string")

        blob = " ".join([str(card.get("title", "")), str(card.get("note", ""))]
                        + [str(s) for s in (card.get("subtasks") or [])]
                        + [str(card.get("project", ""))])
        breaches = floor_breaches(blob)
        if breaches:
            bad.append(f"{rel}: style floor breached: {', '.join(sorted(set(breaches)))}")

    for path, proj in all_projects():
        rel = path.relative_to(ROOT)
        if proj.get("id") != path.parent.name:
            bad.append(f"{rel}: id {proj.get('id')!r} does not match directory {path.parent.name!r}")
        lane = proj.get("lane", "")
        if lane:
            ok, why = lane_is_valid(lane)
            if not ok:
                bad.append(f"{rel}: lane {why}")

    for line in bad:
        print(f"  FAIL {line}")
    print(f"validate: {len(seen_cards)} cards, {len(seen_projects)} projects, "
          f"{len(seen_lanes)} lanes, {len(bad)} failures")
    return 1 if bad else 0


def _cards_sorted(cards: list[dict]) -> list[dict]:
    return sorted(cards, key=lambda c: (c.get("lane", ""), c.get("id", "")))


def _lane_count(lane_path: str, cards: list[dict], column: str | None = None) -> int:
    keys = {l.get("path") for l in lanes_under(lane_path)}
    return len([c for c in cards
                if c.get("lane") in keys and (column is None or c.get("state") == column)])


def cmd_index(args) -> int:
    """Regenerate the reading. Staleness is stamped in the file, not hidden."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    cfg_cols = columns()
    cards = [c for _, c in all_cards()]
    lanes_decl = lanes()

    by_col: dict[str, list[dict]] = {c: [] for c in cfg_cols}
    for card in cards:
        by_col.setdefault(card.get("state", ""), []).append(card)

    md = ["# Board", "",
          f"Generated {stamp} by `tools/board.py index`. This is a view, not the truth.",
          "The truth is one TOML file per card under `cards/`. If a card moved since",
          "this stamp, this page is wrong and the file is right.", "",
          f"**{len(cards)} cards** in {len([k for k, v in by_col.items() if v])} columns, "
          f"across {len(lanes_decl)} declared lanes.", ""]

    rulings = [c for c in cards if c.get("awaiting") == "operator"]
    if rulings:
        md += ["## Waiting on the operator", ""]
        for card in _cards_sorted(rulings):
            md.append(f"- **{card.get('id')}** {card.get('title')} "
                      f"({card.get('state')}, `{card.get('lane')}`)")
        md.append("")

    md += ["## Flight", ""]
    for col in cfg_cols:
        rows = _cards_sorted(by_col.get(col, []))
        md.append(f"### {col} ({len(rows)})")
        md.append("")
        if not rows:
            md += ["_empty_", ""]
            continue
        md += ["| id | title | lane | owner | tier |", "|---|---|---|---|---|"]
        for card in rows:
            md.append("| {id} | {title} | {lane} | {owner} | {tier} |".format(
                id=card.get("id", ""),
                title=str(card.get("title", "")).replace("|", "\\|"),
                lane=card.get("lane", ""),
                owner=card.get("owner", "") or "-",
                tier=card.get("tier", "")))
        md.append("")

    md += ["## Lanes", "",
           "Counts roll up: a parent lane includes everything nested under it.", "",
           "| lane | level | " + " | ".join(cfg_cols) + " | total |",
           "|---" * (len(cfg_cols) + 3) + "|"]
    for lane in lanes_decl:
        path = lane.get("path", "")
        row = [path, lane.get("level", "")]
        total = 0
        for col in cfg_cols:
            n = _lane_count(path, cards, col)
            total += n
            row.append(str(n) if n else ".")
        row.append(str(total))
        md.append("| " + " | ".join(row) + " |")
    md.append("")

    blocked = [c for c in cards if c.get("state") == "blocked"]
    if blocked:
        md += ["## Blocked", ""]
        for card in _cards_sorted(blocked):
            md.append(f"- **{card.get('id')}** {card.get('title')}. {card.get('note', '')}".rstrip())
        md.append("")

    (ROOT / "BOARD.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    INDEX.mkdir(exist_ok=True)
    payload = {
        "generated": stamp,
        "counts": {col: len(by_col.get(col, [])) for col in cfg_cols},
        "total": len(cards),
        "lanes": [{"path": l.get("path"), "level": l.get("level"), "title": l.get("title"),
                   "counts": {col: _lane_count(l.get("path", ""), cards, col)
                              for col in cfg_cols}}
                  for l in lanes_decl],
        "cards": [dict(c, file=str(p.relative_to(ROOT))) for p, c in all_cards()],
    }
    (INDEX / "board.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                                      encoding="utf-8")
    print(f"index: wrote BOARD.md and index/board.json ({len(cards)} cards, stamp {stamp})")
    return 0


def _matches(card: dict, args) -> bool:
    if getattr(args, "column", None) and card.get("state") != args.column:
        return False
    lane = getattr(args, "lane", None)
    if lane:
        keys = {l.get("path") for l in lanes_under(lane)}
        if card.get("lane") not in keys:
            return False
    if getattr(args, "owner", None) and card.get("owner") != args.owner:
        return False
    if getattr(args, "awaiting", None) and card.get("awaiting") != args.awaiting:
        return False
    return True


def cmd_list(args) -> int:
    cards = [c for _, c in all_cards() if _matches(c, args)]
    order = columns()
    cards.sort(key=lambda c: (order.index(c.get("state", ""))
                              if c.get("state") in order else 99, c.get("id", "")))
    if not cards:
        print("(no cards match)")
        return 0
    print(f"{'id':8} {'column':9} {'lane':22} {'awaiting':9} title")
    for card in cards:
        print(f"{card.get('id', ''):8} {card.get('state', ''):9} "
              f"{card.get('lane', ''):22} {(card.get('awaiting') or '-'):9} "
              f"{card.get('title', '')}")
    print(f"\n{len(cards)} card(s)")
    return 0


def cmd_show(args) -> int:
    found = card_by_id(args.card_id)
    if not found:
        print(f"no card {args.card_id}", file=sys.stderr)
        return 1
    path, card = found
    print(f"file: {path.relative_to(ROOT)}")
    for key in CARD_ORDER:
        if key in card:
            print(f"{key:10} {card[key]}")
    return 0


def cmd_lanes(args) -> int:
    cards = [c for _, c in all_cards()]
    for lane in lanes():
        path = lane.get("path", "")
        depth = path.count("/")
        label = ("  " * depth) + path.split("/")[-1]
        own = len([c for c in cards if c.get("lane") == path])
        rolled = _lane_count(path, cards)
        print(f"{label:28} {lane.get('level', ''):9} {own:3d} own {rolled:3d} rolled  "
              f"{lane.get('title', '')}")
    return 0


def cmd_stale(args) -> int:
    """What needs a human. An activity reminder, not a gate."""
    days = args.days
    cards = [c for _, c in all_cards()]

    def age_days(card: dict) -> float:
        stamp = card.get("updated") or card.get("created") or ""
        try:
            return (time.time() - time.mktime(time.strptime(stamp, "%Y-%m-%d"))) / 86400
        except (ValueError, TypeError):
            return float("inf")

    rulings = [c for c in cards if c.get("awaiting") == "operator"]
    blocked = [c for c in cards if c.get("state") == "blocked"]
    quiet = [c for c in cards if c.get("state") in ACTIVE_COLUMNS and age_days(c) > days]

    def emit(title: str, rows: list[dict]) -> None:
        if not rows:
            return
        print(f"{title} ({len(rows)})")
        for card in sorted(rows, key=age_days, reverse=True):
            print(f"  {card.get('id', ''):7} {card.get('state', ''):8} "
                  f"{(card.get('lane') or '-'):20} {card.get('title', '')}  [{age_days(card):.0f}d]")
        print()

    emit("OUTSTANDING RULINGS (awaiting the operator)", rulings)
    emit("BLOCKED", blocked)
    emit(f"GONE QUIET (in flight, no update in {days}d)", quiet)
    if not (rulings or blocked or quiet):
        print(f"stale: nothing needs a human. {len(cards)} cards clean.")
    return 0


def cmd_new_project(args) -> int:
    ident = slug(args.name)
    path = PROJECTS / ident / "project.toml"
    if path.exists():
        print(f"project {ident} already exists", file=sys.stderr)
        return 1
    if args.lane:
        ok, why = lane_is_valid(args.lane)
        if not ok:
            print(f"lane {why}", file=sys.stderr)
            return 1
    fields = {"name": args.name, "id": ident, "owner": args.owner, "tier": 1,
              "lane": args.lane or "", "status": "active", "repo": args.repo or "",
              "location": args.location or "", "summary": args.summary or "",
              "created": today(), "updated": today()}
    write_project(path, fields)
    print(f"created projects/{ident}/project.toml")
    return 0


def cmd_new_card(args) -> int:
    if args.column not in columns():
        print(f"unknown column {args.column!r}; columns are {', '.join(columns())}",
              file=sys.stderr)
        return 1
    ok, why = lane_is_valid(args.lane)
    if not ok:
        print(f"lane {why}", file=sys.stderr)
        return 1
    if args.project and args.project not in project_slugs():
        print(f"unknown project {args.project!r}", file=sys.stderr)
        return 1
    if args.horizon and args.horizon not in horizons():
        print(f"unknown horizon {args.horizon!r}", file=sys.stderr)
        return 1
    if args.awaiting and args.awaiting not in awaiting_values():
        print(f"unknown awaiting value {args.awaiting!r}", file=sys.stderr)
        return 1
    breaches = floor_breaches(" ".join([args.title, args.note or ""] + list(args.subtask or [])))
    if breaches:
        print(f"style floor breached in the text you passed: {', '.join(sorted(set(breaches)))}",
              file=sys.stderr)
        return 1

    existing = [p.stem for p, _ in all_cards()]
    cid = next_id("c", existing)
    fields = {"id": cid, "title": args.title, "lane": args.lane,
              "project": args.project or "", "state": args.column, "owner": args.owner,
              "tier": args.tier, "horizon": args.horizon or "",
              "awaiting": args.awaiting or "", "platform": "", "workers": [],
              "models": [], "subtasks": list(args.subtask or []),
              "links": list(args.link or []), "blocked_by": list(args.blocked_by or []),
              "created": today(), "updated": today(), "note": args.note or ""}
    path = CARDS / args.column / f"{cid}.toml"
    write_card(path, fields)
    print(f"created cards/{args.column}/{cid}.toml  ({cid})")
    return 0


def cmd_move(args) -> int:
    found = card_by_id(args.card_id)
    if not found:
        print(f"no card {args.card_id}", file=sys.stderr)
        return 1
    path, card = found
    if args.column not in columns():
        print(f"unknown column {args.column!r}", file=sys.stderr)
        return 1
    dest = CARDS / args.column / path.name
    if dest == path:
        print(f"{args.card_id} is already in {args.column}")
        return 0
    git_mv(path, dest)
    card["state"] = args.column
    card["updated"] = today()
    if args.note:
        card["note"] = args.note
    if args.column in terminal_columns() and card.get("awaiting"):
        card["awaiting"] = ""
    write_card(dest, card)
    print(f"moved {args.card_id}: {path.parent.name} -> {args.column}")
    return 0


def cmd_set(args) -> int:
    found = card_by_id(args.card_id)
    if not found:
        print(f"no card {args.card_id}", file=sys.stderr)
        return 1
    path, card = found
    changed = []
    if args.note is not None:
        card["note"] = args.note
        changed.append("note")
    if args.owner is not None:
        card["owner"] = args.owner
        changed.append("owner")
    if args.awaiting is not None:
        value = "" if args.awaiting in ("clear", "-", "none") else args.awaiting
        if value and value not in awaiting_values():
            print(f"unknown awaiting value {value!r}", file=sys.stderr)
            return 1
        card["awaiting"] = value
        changed.append(f"awaiting={value or 'cleared'}")
    if args.horizon is not None:
        if args.horizon and args.horizon not in horizons():
            print(f"unknown horizon {args.horizon!r}", file=sys.stderr)
            return 1
        card["horizon"] = args.horizon
        changed.append(f"horizon={args.horizon}")
    if args.tier is not None:
        if args.tier not in (1, 2, 3):
            print("tier must be 1, 2 or 3", file=sys.stderr)
            return 1
        card["tier"] = args.tier
        changed.append(f"tier={args.tier}")
    if not changed:
        print("nothing to change (use --note, --owner, --awaiting, --horizon, --tier)")
        return 1
    breaches = floor_breaches(" ".join([str(card.get("title", "")), str(card.get("note", ""))]))
    if breaches:
        print(f"style floor breached: {', '.join(sorted(set(breaches)))}", file=sys.stderr)
        return 1
    card["updated"] = today()
    write_card(path, card)
    print(f"updated {args.card_id}: {', '.join(changed)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="board", description="the DMF project board's one tool")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("validate").set_defaults(fn=cmd_validate)
    sub.add_parser("index").set_defaults(fn=cmd_index)
    sub.add_parser("lanes").set_defaults(fn=cmd_lanes)

    p = sub.add_parser("list")
    p.add_argument("--column")
    p.add_argument("--lane", help="a lane path; includes everything nested under it")
    p.add_argument("--owner")
    p.add_argument("--awaiting")
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("show")
    p.add_argument("card_id")
    p.set_defaults(fn=cmd_show)

    p = sub.add_parser("stale")
    p.add_argument("--days", type=int, default=7)
    p.set_defaults(fn=cmd_stale)

    p = sub.add_parser("new-project")
    p.add_argument("--name", required=True)
    p.add_argument("--owner", default="operator")
    p.add_argument("--lane")
    p.add_argument("--summary")
    p.add_argument("--repo")
    p.add_argument("--location")
    p.set_defaults(fn=cmd_new_project)

    p = sub.add_parser("new-card")
    p.add_argument("--title", required=True)
    p.add_argument("--lane", required=True)
    p.add_argument("--project", default="")
    p.add_argument("--column", default="inbox")
    p.add_argument("--owner", default="operator")
    p.add_argument("--tier", type=int, default=1)
    p.add_argument("--horizon")
    p.add_argument("--awaiting")
    p.add_argument("--subtask", action="append")
    p.add_argument("--link", action="append")
    p.add_argument("--blocked-by", dest="blocked_by", action="append")
    p.add_argument("--note")
    p.set_defaults(fn=cmd_new_card)

    p = sub.add_parser("move")
    p.add_argument("card_id")
    p.add_argument("column")
    p.add_argument("--note")
    p.set_defaults(fn=cmd_move)

    p = sub.add_parser("set")
    p.add_argument("card_id")
    p.add_argument("--note")
    p.add_argument("--owner")
    p.add_argument("--awaiting", help="operator, seat, external, or clear")
    p.add_argument("--horizon")
    p.add_argument("--tier", type=int)
    p.set_defaults(fn=cmd_set)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
