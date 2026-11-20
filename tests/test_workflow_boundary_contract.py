"""Contract: published scenario artefacts satisfy the documented boundaries.

The two skills state boundaries that a record can be decided against rather
than judged: a plan that carries an unaccepted deviation must not claim
`COMPLETE`, and a handoff must state its approval state, its readiness, the
stable identifiers downstream work inherits, and the route back when an
assumption fails. These checks read the artefacts published under
``docs/validation``, so the evidence a reader can inspect is the evidence the
suite decides, and a regression in either the recorded output or the check is a
failing test.

They do not execute either skill. Whether an agent obeys the guidance remains
the subject of the scenarios themselves, which are manual evidence; a passing
check here says only that the recorded output satisfies the stated boundary.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTEFACTS = ROOT / "docs/validation/2026-11-19-agent-scenarios"

_HEADING = re.compile(r"^(#{2,6})\s+(\S.*?)\s*$", re.MULTILINE)
_STATUS = re.compile(r"^Status:\s*([A-Za-z]+)", re.MULTILINE)
_STATUSES = frozenset({"DRAFT", "ACTIVE", "BLOCKED", "COMPLETE"})
_UNACCEPTED_DEVIATION = re.compile(
    r"proposed; not approved|proposal pending acceptance|pending acceptance"
    r"|not approved",
    re.IGNORECASE,
)
_APPROVAL_STATE = re.compile(
    r"\b(?:not accepted|accepted revision|approv(?:al|ed))\b", re.IGNORECASE
)
_READINESS = re.compile(
    r"ready for (?:technical )?design|bounded discovery|\bblocked\b", re.IGNORECASE
)
_STABLE_ID = re.compile(r"\bTOR-[A-Z]+-\d+\b")
_FEEDBACK_ROUTE = re.compile(r"\bfeedback\b", re.IGNORECASE)


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


def _status_problems(text: str) -> list[str]:
    """Return boundary violations in a plan or revision record."""
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
    elif status == "COMPLETE" and _UNACCEPTED_DEVIATION.search(decision_log):
        problems.append("COMPLETE with an unaccepted deviation in the Decision log")
    elif status == "BLOCKED" and not _UNACCEPTED_DEVIATION.search(decision_log):
        problems.append(
            "BLOCKED without a Decision log entry recording an unaccepted deviation"
        )
    return problems


def _handoff_problems(text: str) -> list[str]:
    """Return the elements a documented traceable handoff must state."""
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


def _artefact(*parts: str) -> str:
    """Return one published artefact as text."""
    return ARTEFACTS.joinpath(*parts).read_text(encoding="utf-8")


def test_the_published_plan_blocks_on_its_recorded_deviation() -> None:
    """The C3 plan is blocked, and claiming completion is reported."""
    text = _artefact("c3-271b0f8", "execplan-library-api-rename.md.txt")

    assert _status_problems(text) == []

    completed = text.replace("Status: BLOCKED", "Status: COMPLETE", 1)

    assert _status_problems(completed) == [
        "COMPLETE with an unaccepted deviation in the Decision log"
    ]


def test_the_published_revision_record_blocks_on_its_deviation() -> None:
    """The second C3 record is blocked for the reason its Decision log states."""
    text = _artefact("c3-29cd658", "execplan-record.md.txt")

    assert _status_problems(text) == []


def test_both_published_c3_handoffs_state_their_boundaries() -> None:
    """Each C3 run's handoff names approval, readiness, IDs, and feedback."""
    first = _artefact("c3-271b0f8", "terms-of-reference.md.txt")
    second = _artefact("c3-29cd658", "terms-of-reference.md.txt")

    assert _handoff_problems(first) == []
    assert _handoff_problems(second) == []


def test_a_handoff_without_a_feedback_route_is_reported() -> None:
    """A handoff that drops the route back for a failed assumption is reported."""
    text = (
        "## Handoff\n\n"
        "Accepted revision: none. Ready for design. TOR-GOAL-001 is inherited.\n"
    )

    assert _handoff_problems(text) == ["handoff does not state its feedback route"]


def test_a_blocked_plan_without_a_recorded_deviation_is_reported() -> None:
    """A blocked plan whose Decision log records no deviation is reported."""
    text = "Status: BLOCKED\n\n## Decision log\n\n- D1. Renamed the module.\n"

    assert _status_problems(text) == [
        "BLOCKED without a Decision log entry recording an unaccepted deviation"
    ]


def test_an_unknown_status_is_reported() -> None:
    """A plan outside the documented status vocabulary is reported."""
    text = "Status: PENDING\n\n## Decision log\n\n- D1. Proposed; not approved.\n"

    assert _status_problems(text) == ["unknown status PENDING"]
