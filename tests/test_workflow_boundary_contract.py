"""Contract: the workflow-boundary validator decides the documented boundaries.

The two skills state boundaries that a record can be decided against rather
than judged: a plan that carries an unaccepted deviation must not claim
`COMPLETE`, and a handoff must state its approval state, its readiness, the
stable identifiers downstream work inherits, and the route back when an
assumption fails. ``scripts/check_workflow_boundary.py`` decides those
boundaries; this module drives it through its command line, so the test depends
only on the interface a contributor uses.

The fixtures are derived from the forms the skills document. The record
fixtures use the `Status` line and `Decision log` section the ExecPlan contract
defines; the handoff fixtures use the revision, approval state, stable IDs,
readiness classification, and feedback route that `terms-of-reference-doc`
requires. One test copies the two skills, deletes a governing sentence from the
copy, and asserts that the validator then fails, so the check cannot pass by
forgetting the rule it is deciding.

They do not execute either skill. Whether an agent obeys the guidance remains
the subject of the scenarios themselves, which are manual evidence; a passing
check here says only that the recorded output satisfies the stated boundary.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/check_workflow_boundary.py"
SKILLS = ROOT / "skills"
ARTEFACTS = ROOT / "docs/validation/2026-11-19-agent-scenarios"


def _run(
    check: str, record: Path, skills_root: Path = SKILLS
) -> subprocess.CompletedProcess[str]:
    """Return the validator's result for one record."""
    return subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--skills-root",
            str(skills_root),
            check,
            str(record),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def _fixture(tmp_path: Path, text: str) -> Path:
    """Write one record fixture and return its path."""
    path = tmp_path / "record.md"
    path.write_text(text, encoding="utf-8")
    return path


def _published(*parts: str) -> Path:
    """Return the path of one published artefact."""
    return ARTEFACTS.joinpath(*parts)


def test_the_published_plan_blocks_on_its_recorded_deviation(
    tmp_path: Path,
) -> None:
    """The C3 plan is blocked, and claiming completion is reported."""
    plan = _published("c3-271b0f8", "execplan-library-api-rename.md.txt")

    accepted = _run("status", plan)

    assert accepted.returncode == 0
    assert accepted.stdout == ""
    assert accepted.stderr == ""

    completed = _fixture(
        tmp_path,
        plan.read_text(encoding="utf-8").replace(
            "Status: BLOCKED", "Status: COMPLETE", 1
        ),
    )
    rejected = _run("status", completed)

    assert rejected.returncode == 1
    assert (
        "COMPLETE with an unaccepted deviation in the Decision log" in rejected.stdout
    )


def test_the_published_revision_record_blocks_on_its_deviation() -> None:
    """The second C3 record is blocked for the reason its Decision log states."""
    record = _published("c3-29cd658", "execplan-record.md.txt")

    result = _run("status", record)

    assert result.returncode == 0
    assert result.stdout == ""


def test_both_published_c3_handoffs_state_their_boundaries() -> None:
    """Each C3 run's handoff names approval, readiness, IDs, and feedback."""
    first = _published("c3-271b0f8", "terms-of-reference.md.txt")
    second = _published("c3-29cd658", "terms-of-reference.md.txt")

    assert _run("handoff", first).returncode == 0
    assert _run("handoff", second).returncode == 0


def test_a_handoff_without_a_feedback_route_is_reported(tmp_path: Path) -> None:
    """A handoff that drops the route back for a failed assumption is reported."""
    record = _fixture(
        tmp_path,
        (
            "## Handoff\n\n"
            "Accepted revision: none. Ready for design. TOR-GOAL-001 is inherited.\n"
        ),
    )

    result = _run("handoff", record)

    assert result.returncode == 1
    assert result.stdout == f"{record}: handoff does not state its feedback route\n"


def test_a_handoff_that_names_no_feedback_route_is_reported(tmp_path: Path) -> None:
    """A label naming an absent route does not state a route."""
    record = _fixture(
        tmp_path,
        (
            "## Handoff\n\n"
            "Accepted revision: none. Ready for design. TOR-GOAL-001 is inherited.\n"
            "Feedback route: none.\n"
        ),
    )

    result = _run("handoff", record)

    assert result.returncode == 1
    assert "handoff does not state its feedback route" in result.stdout


def test_a_blocked_plan_without_a_recorded_deviation_is_reported(
    tmp_path: Path,
) -> None:
    """A blocked plan whose Decision log records no deviation is reported."""
    record = _fixture(
        tmp_path, "Status: BLOCKED\n\n## Decision log\n\n- D1. Renamed the module.\n"
    )

    result = _run("status", record)

    assert result.returncode == 1
    assert (
        "BLOCKED without a Decision log entry recording an unaccepted deviation"
        in result.stdout
    )


def test_an_active_plan_with_an_unaccepted_deviation_is_reported(
    tmp_path: Path,
) -> None:
    """An executing plan may not carry a deviation that is still unaccepted."""
    record = _fixture(
        tmp_path,
        (
            "Status: ACTIVE\n\n## Decision log\n\n"
            "- D1. Decision: renamed the module. Status: proposal pending acceptance.\n"
        ),
    )

    result = _run("status", record)

    assert result.returncode == 1
    assert "ACTIVE with an unaccepted deviation in the Decision log" in result.stdout


def test_a_template_only_deviation_is_reported(tmp_path: Path) -> None:
    """A fenced placeholder does not count as a recorded Decision log entry."""
    record = _fixture(
        tmp_path,
        (
            "Status: BLOCKED\n\n## Decision log\n\n"
            "Add one entry:\n\n"
            "```plaintext\n"
            "- D-<next free>. Decision: <what was decided>.\n"
            "  Status: proposal pending acceptance.\n"
            "```\n"
        ),
    )

    result = _run("status", record)

    assert result.returncode == 1
    assert (
        "BLOCKED without a Decision log entry recording an unaccepted deviation"
        in result.stdout
    )


def test_an_unknown_status_is_reported(tmp_path: Path) -> None:
    """A plan outside the documented status vocabulary is reported."""
    record = _fixture(
        tmp_path,
        "Status: PENDING\n\n## Decision log\n\n- D1. Proposed; not approved.\n",
    )

    result = _run("status", record)

    assert result.returncode == 1
    assert "unknown status PENDING" in result.stdout


def test_a_skill_that_drops_its_rule_fails_the_check(tmp_path: Path) -> None:
    """Deleting the BLOCKED rule from a copied skill fails the validator."""
    skills_root = tmp_path / "skills"
    for name in ("tech-design-doc", "terms-of-reference-doc"):
        (skills_root / name).mkdir(parents=True)
        source = SKILLS / name / "SKILL.md"
        (skills_root / name / "SKILL.md").write_text(
            source.read_text(encoding="utf-8"), encoding="utf-8"
        )
    record = _fixture(
        tmp_path,
        (
            "## Handoff\n\n"
            "Accepted revision: 7. Ready for design. TOR-GOAL-001 is inherited.\n"
            "Feedback route: the ToR decision authority.\n"
        ),
    )

    intact = _run("handoff", record, skills_root)

    assert intact.returncode == 0
    assert intact.stdout == ""

    drifted = skills_root / "tech-design-doc/SKILL.md"
    drifted.write_text(
        drifted.read_text(encoding="utf-8").replace(
            "enters `BLOCKED`", "enters a blocked state"
        ),
        encoding="utf-8",
    )

    rejected = _run("handoff", record, skills_root)

    assert rejected.returncode == 1
    assert "no longer states that an executing ExecPlan enters BLOCKED" in (
        rejected.stdout
    )
