#!/usr/bin/env python3
"""Check records against the boundaries the authoring skills state.

The skills state two boundaries that a record decides rather than a reviewer
judges. An ExecPlan that carries an unaccepted deviation records it in its
Decision log and enters ``BLOCKED``; it may not claim ``ACTIVE`` or
``COMPLETE`` until the deviation is accepted. A handoff states its approval
state, its readiness classification, the stable identifiers downstream work
inherits, and the route back when an assumption fails.

The governing sentences are read from the shipped skills rather than repeated
here, so a skill whose rule has been removed or softened fails the check
instead of quietly dropping the obligation.

Usage::

    python scripts/check_workflow_boundary.py status RECORD...
    python scripts/check_workflow_boundary.py handoff RECORD...

A diagnostic is printed as ``path: message``. The exit status is 1 when any
diagnostic is reported, including one about the skills themselves.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

DEFAULT_SKILLS_ROOT = Path(__file__).resolve().parent.parent / "skills"

_HEADING = re.compile(r"^(#{2,6})\s+(\S.*?)\s*$", re.MULTILINE)
_STATUS = re.compile(r"^Status:\s*([A-Za-z]+)", re.MULTILINE)
_STATUSES = frozenset({"DRAFT", "ACTIVE", "BLOCKED", "COMPLETE"})
_UNACCEPTED_DEVIATION = re.compile(
    r"proposed; not approved|proposal pending acceptance|pending acceptance"
    r"|not approved",
    re.IGNORECASE,
)
_FENCE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
_DECISION_STATEMENT = re.compile(r"Decision:\s*(?!<)[^<\n]{20,}", re.IGNORECASE)
_APPROVAL_STATE = re.compile(
    r"\b(?:not accepted|accepted revision|approv(?:al|ed))\b", re.IGNORECASE
)
_READINESS = re.compile(
    r"ready for (?:technical )?design|bounded discovery|\bblocked\b", re.IGNORECASE
)
_STABLE_ID = re.compile(r"\bTOR-[A-Z]+-\d+\b")
_FEEDBACK_ROUTE = re.compile(
    r"\bfeedback\b(?!\s*(?:route|path|channel)?\s*[:.-]?\s*"
    r"(?:none|nil|n/?a|not\s+(?:applicable|stated|provided|specified|available)"
    r"|absent|tbd|unknown)\b)",
    re.IGNORECASE,
)

#: Each rule the checks below depend on, with the sentence that states it.
_RULES = (
    (
        Path("tech-design-doc/SKILL.md"),
        "records the deviation in",
        "an executing ExecPlan records the deviation in its Decision log",
    ),
    (
        Path("tech-design-doc/SKILL.md"),
        "enters `BLOCKED`",
        "an executing ExecPlan enters BLOCKED",
    ),
    (
        Path("tech-design-doc/SKILL.md"),
        "before `COMPLETE`",
        "the approved resolution is recorded before COMPLETE",
    ),
    (
        Path("terms-of-reference-doc/SKILL.md"),
        "approval state, stable IDs",
        "a handoff supplies its approval state and stable IDs",
    ),
    (
        Path("terms-of-reference-doc/SKILL.md"),
        "Distinguish ready-for-design",
        "a handoff distinguishes its readiness classifications",
    ),
    (
        Path("terms-of-reference-doc/SKILL.md"),
        "Feedback route.",
        "a handoff names its feedback route",
    ),
)


def _normalise(text: str) -> str:
    """Return ``text`` with runs of whitespace collapsed to single spaces."""
    return " ".join(text.split())


def _sections(text: str) -> list[tuple[str, str]]:
    """Return each heading's title and region, respecting heading levels."""
    headings = list(_HEADING.finditer(text))
    sections: list[tuple[str, str]] = []
    for index, heading in enumerate(headings):
        level = len(heading.group(1))
        end = len(text)
        for later in headings[index + 1 :]:
            if len(later.group(1)) <= level:
                end = later.start()
                break
        sections.append((heading.group(2), text[heading.end() : end]))
    return sections


def _section_named(text: str, needle: str) -> str:
    """Return the region of the first heading whose title names ``needle``."""
    for title, region in _sections(text):
        if needle.lower() in title.lower():
            return region
    return ""


def _records_unaccepted_deviation(region: str) -> bool:
    """Return whether the Decision log records an unaccepted deviation.

    A fenced block is the plan format's template, so it counts as a recorded
    entry only when it states a concrete decision. A placeholder-only template
    is illustrative, and its "pending acceptance" marks the form, not an entry.

    Parameters
    ----------
    region : str
        The text of the Decision log section.

    Returns
    -------
    bool
        Whether the section records a deviation awaiting acceptance.

    """
    prose = _FENCE.sub("", region)
    if _UNACCEPTED_DEVIATION.search(prose):
        return True
    return any(
        _UNACCEPTED_DEVIATION.search(block)
        and _DECISION_STATEMENT.search(block) is not None
        for block in _FENCE.findall(region)
    )


def status_problems(text: str) -> list[str]:
    """Return the boundary violations in a plan or revision record.

    Parameters
    ----------
    text : str
        The record to check.

    Returns
    -------
    list[str]
        One message per violation, empty when the record satisfies the rule.

    """
    match = _STATUS.search(text)
    if match is None:
        return ["no Status line"]
    status = match.group(1).upper()
    problems = []
    if status not in _STATUSES:
        problems.append(f"unknown status {status}")
    decision_log = _section_named(text, "Decision log")
    if not decision_log:
        problems.append("no Decision log")
    elif status in {"ACTIVE", "COMPLETE"} and _records_unaccepted_deviation(
        decision_log
    ):
        problems.append(f"{status} with an unaccepted deviation in the Decision log")
    elif status == "BLOCKED" and not _records_unaccepted_deviation(decision_log):
        problems.append(
            "BLOCKED without a Decision log entry recording an unaccepted deviation"
        )
    return problems


def handoff_problems(text: str) -> list[str]:
    """Return the elements a documented traceable handoff must state.

    Parameters
    ----------
    text : str
        The record to check.

    Returns
    -------
    list[str]
        One message per missing element, empty when the handoff is complete.

    """
    handoff = _section_named(text, "Handoff")
    if not handoff:
        return ["no handoff section"]
    required = (
        ("approval state", _APPROVAL_STATE),
        ("readiness classification", _READINESS),
        ("stable identifier", _STABLE_ID),
        ("feedback route", _FEEDBACK_ROUTE),
    )
    return [
        f"handoff does not state its {label}"
        for label, pattern in required
        if pattern.search(handoff) is None
    ]


def skill_rule_problems(skills_root: Path) -> list[str]:
    """Return the documented rules the shipped skills no longer state.

    Parameters
    ----------
    skills_root : Path
        Directory holding the shipped skill directories.

    Returns
    -------
    list[str]
        One message per missing rule, empty when every rule is present.

    """
    problems: list[str] = []
    for relative, fragment, description in _RULES:
        path = skills_root / relative
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
            problems.append(f"{path}: cannot read the skill: {error.strerror}")
            continue
        if fragment not in _normalise(text):
            problems.append(f"{path}: no longer states that {description}")
    return problems


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    """Return the parsed command line."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--skills-root",
        type=Path,
        default=DEFAULT_SKILLS_ROOT,
        help="directory holding the shipped skills (default: %(default)s)",
    )
    subparsers = parser.add_subparsers(dest="kind", required=True)
    for kind, description in (
        ("status", "check plan and revision records"),
        ("handoff", "check handoff sections"),
    ):
        subparser = subparsers.add_parser(kind, help=description)
        subparser.add_argument("files", nargs="+", type=Path, metavar="RECORD")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the requested check over each record and report diagnostics.

    Parameters
    ----------
    argv : Sequence[str] | None
        Arguments to parse, defaulting to ``sys.argv[1:]``.

    Returns
    -------
    int
        ``0`` when nothing is reported, ``1`` otherwise.

    """
    args = _parse_args(sys.argv[1:] if argv is None else argv)
    check = status_problems if args.kind == "status" else handoff_problems
    problems = skill_rule_problems(args.skills_root)
    for path in args.files:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
            problems.append(f"{path}: cannot read the record: {error.strerror}")
            continue
        problems.extend(f"{path}: {message}" for message in check(text))
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
