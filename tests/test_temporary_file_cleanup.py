"""Behavioural and property coverage for documented temporary-file cleanup."""

from __future__ import annotations

import dataclasses as dc
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from pytest_bdd import given as bdd_given
from pytest_bdd import parsers, scenarios, then, when

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
FEATURES_DIRECTORY = "features/temporary_file_cleanup.feature"


@dc.dataclass(frozen=True)
class CleanupWorkflow:
    """Identify one documented cleanup function and its single artefact."""

    name: str
    skill_path: Path
    function_name: str
    directory_variable: str
    artefact_name: str


@dc.dataclass(frozen=True)
class BoundedCase:
    """Describe one controlled directory value for a cleanup scope check."""

    name: str
    directory_value: str
    invocation_directory: Path
    target_directory: Path | None


@dc.dataclass
class CleanupScenario:
    """Hold one pytest-bdd scenario's isolated fixture and command result."""

    root: Path
    workflow: CleanupWorkflow | None = None
    temporary_directory: Path | None = None
    result: subprocess.CompletedProcess[str] | None = None


WORKFLOWS = (
    CleanupWorkflow(
        name="commit",
        skill_path=Path("skills/commit-message/SKILL.md"),
        function_name="cleanup_commit_message",
        directory_variable="COMMIT_MSG_DIR",
        artefact_name="COMMIT_MSG.md",
    ),
    CleanupWorkflow(
        name="pr",
        skill_path=Path("skills/pr-creation/SKILL.md"),
        function_name="cleanup_pr_body",
        directory_variable="PR_BODY_DIR",
        artefact_name="body.md",
    ),
)
WORKFLOWS_BY_NAME = {workflow.name: workflow for workflow in WORKFLOWS}
BOUNDED_CASE_NAMES = (
    "normal",
    "empty",
    "dot",
    "parent",
    "absolute",
    "whitespace",
    "relative",
    "sibling",
)
SAFE_DIRECTORY_NAMES = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _-",
    min_size=1,
    max_size=16,
)

scenarios(FEATURES_DIRECTORY)


def extract_cleanup_function(workflow: CleanupWorkflow) -> str:
    """Return the exact shell function documented for ``workflow``."""
    skill_text = (REPOSITORY_ROOT / workflow.skill_path).read_text(encoding="utf-8")
    pattern = re.compile(
        rf"^{workflow.function_name}\(\) \{{\n.*?^\}}",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(skill_text)
    if match is None:
        msg = f"Could not extract {workflow.function_name} from {workflow.skill_path}"
        raise AssertionError(msg)
    return match.group()


def create_guarded_commands(root: Path) -> Path:
    """Create fixture-only shims that reject paths outside ``root``.

    They keep malformed values, especially the empty string, from host paths.
    """
    command_directory = root / "guarded-bin"
    command_directory.mkdir()
    command_script = """#!/bin/sh
set -eu

operand=${1-}
if test -z "$operand"; then
  exit 64
fi
parent=$(dirname "$operand")
base=$(basename "$operand")
absolute=$(CDPATH= cd -P -- "$parent" 2>/dev/null && pwd -P)/$base
case "$absolute" in
  "$TEST_ROOT" | "$TEST_ROOT"/*) ;;
  *) exit 64 ;;
esac
PATH=$SAFE_PATH command COMMAND "$operand"
"""
    for command_name in ("unlink", "rmdir"):
        command_path = command_directory / command_name
        command_path.write_text(
            command_script.replace("COMMAND", command_name), encoding="utf-8"
        )
        command_path.chmod(0o755)
    return command_directory


def run_cleanup(
    workflow: CleanupWorkflow,
    root: Path,
    directory_value: str,
    invocation_directory: Path,
) -> subprocess.CompletedProcess[str]:
    """Execute the extracted shell cleanup function within one safe fixture."""
    command_directory = create_guarded_commands(root)
    environment = os.environ.copy()
    environment.update({
        "CLEANUP_DIRECTORY": directory_value,
        "PATH": f"{command_directory}{os.pathsep}{environment['PATH']}",
        "SAFE_PATH": environment["PATH"],
        "TEST_ROOT": str(root),
    })
    script = "\n".join((
        "set -eu",
        extract_cleanup_function(workflow),
        f'{workflow.directory_variable}="$CLEANUP_DIRECTORY"',
        workflow.function_name,
    ))
    return subprocess.run(
        [find_posix_shell(), "-c", script],
        capture_output=True,
        check=False,
        cwd=invocation_directory,
        env=environment,
        text=True,
    )


def find_posix_shell() -> str:
    """Return the shell used to execute the documented POSIX examples."""
    shell_path = shutil.which("sh")
    if shell_path is None:
        msg = "A POSIX shell is required to execute the documented cleanup examples"
        raise AssertionError(msg)
    return shell_path


def bounded_case_paths(case_name: str, work_directory: Path) -> BoundedCase:
    """Return the controlled directory value and paths for ``case_name``."""
    if case_name == "normal":
        target_directory = Path(
            tempfile.mkdtemp(dir=work_directory, prefix="generated-")
        )
        return BoundedCase(
            name=case_name,
            directory_value=str(target_directory),
            invocation_directory=work_directory,
            target_directory=target_directory,
        )
    if case_name == "empty":
        return BoundedCase(
            name=case_name,
            directory_value="",
            invocation_directory=work_directory,
            target_directory=None,
        )

    target_directory = {
        "absolute": work_directory / "absolute-target",
        "dot": work_directory / "dot-target",
        "parent": work_directory / "parent-target",
        "relative": work_directory / "nested" / "relative-target",
        "sibling": work_directory / "target",
        "whitespace": work_directory / "with whitespace",
    }[case_name]
    directory_value = {
        "absolute": str(target_directory),
        "dot": ".",
        "parent": "..",
        "relative": "nested/relative-target",
        "sibling": str(target_directory),
        "whitespace": str(target_directory),
    }[case_name]
    invocation_directory = {
        "absolute": work_directory,
        "dot": target_directory,
        "parent": target_directory / "nested",
        "relative": work_directory,
        "sibling": work_directory,
        "whitespace": work_directory,
    }[case_name]
    return BoundedCase(
        name=case_name,
        directory_value=directory_value,
        invocation_directory=invocation_directory,
        target_directory=target_directory,
    )


def create_bounded_case(root: Path, case_name: str) -> BoundedCase:
    """Create a non-empty temporary directory for one controlled path value."""
    case_root = root / case_name
    work_directory = case_root / "work"
    sibling_directory = case_root / "sibling"
    work_directory.mkdir(parents=True)
    sibling_directory.mkdir()
    (case_root / "parent.sentinel").write_text("parent", encoding="utf-8")
    (sibling_directory / "sibling.sentinel").write_text("sibling", encoding="utf-8")

    if case_name not in BOUNDED_CASE_NAMES:
        msg = f"Unknown bounded case: {case_name}"
        raise AssertionError(msg)
    case = bounded_case_paths(case_name, work_directory)
    case.invocation_directory.mkdir(parents=True, exist_ok=True)
    if case.target_directory is not None:
        case.target_directory.mkdir(parents=True, exist_ok=True)
    return case


def populate_non_empty_target(
    workflow: CleanupWorkflow, target_directory: Path
) -> None:
    """Add the known artefact and a sentinel that makes ``rmdir`` fail."""
    (target_directory / workflow.artefact_name).write_text("artefact", encoding="utf-8")
    (target_directory / "keep.sentinel").write_text("keep", encoding="utf-8")


def assert_scope_is_preserved(root: Path, case: BoundedCase) -> None:
    """Assert that cleanup retained all sentinels and did not recurse."""
    case_root = root / case.name
    assert (root / "outer.sentinel").is_file()
    assert (case_root / "parent.sentinel").is_file()
    assert (case_root / "sibling" / "sibling.sentinel").is_file()
    assert (case_root / "sibling").is_dir()
    if case.target_directory is not None:
        assert (case.target_directory / "keep.sentinel").is_file()
        assert case.target_directory.is_dir()


@pytest.fixture
def cleanup_scenario(tmp_path: Path) -> CleanupScenario:
    """Provide an isolated fixture for one behavioural cleanup scenario."""
    return CleanupScenario(root=tmp_path)


@bdd_given(parsers.parse('a temporary "{workflow_name}" cleanup fixture'))
def given_temporary_cleanup_fixture(
    cleanup_scenario: CleanupScenario, workflow_name: str
) -> None:
    """Create the known artefact with parent and sibling sentinels."""
    workflow = WORKFLOWS_BY_NAME[workflow_name]
    temporary_directory = cleanup_scenario.root / "temporary"
    sibling_directory = cleanup_scenario.root / "sibling"
    temporary_directory.mkdir()
    sibling_directory.mkdir()
    (cleanup_scenario.root / "parent.sentinel").write_text("parent", encoding="utf-8")
    (sibling_directory / "sibling.sentinel").write_text("sibling", encoding="utf-8")
    (temporary_directory / workflow.artefact_name).write_text(
        "artefact", encoding="utf-8"
    )
    cleanup_scenario.workflow = workflow
    cleanup_scenario.temporary_directory = temporary_directory


@when("the documented cleanup function runs")
def when_documented_cleanup_runs(cleanup_scenario: CleanupScenario) -> None:
    """Execute the extracted function against the scenario's empty target."""
    assert cleanup_scenario.workflow is not None
    assert cleanup_scenario.temporary_directory is not None
    cleanup_scenario.result = run_cleanup(
        cleanup_scenario.workflow,
        cleanup_scenario.root,
        str(cleanup_scenario.temporary_directory),
        cleanup_scenario.root,
    )


@then("the expected Markdown artefact is removed")
def then_expected_artefact_is_removed(cleanup_scenario: CleanupScenario) -> None:
    """Confirm cleanup removed only its known Markdown artefact."""
    assert cleanup_scenario.workflow is not None
    assert cleanup_scenario.temporary_directory is not None
    assert not (
        cleanup_scenario.temporary_directory / cleanup_scenario.workflow.artefact_name
    ).exists()


@then("the empty temporary directory is removed")
def then_empty_temporary_directory_is_removed(
    cleanup_scenario: CleanupScenario,
) -> None:
    """Confirm the documented ``rmdir`` removes an empty temporary directory."""
    assert cleanup_scenario.result is not None
    assert cleanup_scenario.temporary_directory is not None
    assert cleanup_scenario.result.returncode == 0
    assert not cleanup_scenario.temporary_directory.exists()


@then("parent and sibling sentinels remain")
def then_parent_and_sibling_sentinels_remain(cleanup_scenario: CleanupScenario) -> None:
    """Confirm exact cleanup left fixture neighbours untouched."""
    assert (cleanup_scenario.root / "parent.sentinel").is_file()
    assert (cleanup_scenario.root / "sibling" / "sibling.sentinel").is_file()
    assert (cleanup_scenario.root / "sibling").is_dir()


@pytest.mark.parametrize("workflow", WORKFLOWS, ids=lambda workflow: workflow.name)
@pytest.mark.parametrize("case_name", BOUNDED_CASE_NAMES)
def test_cleanup_scope_for_bounded_directory_values(
    tmp_path: Path, workflow: CleanupWorkflow, case_name: str
) -> None:
    """Non-empty bounded cases retain sentinels and record ``rmdir`` failure."""
    (tmp_path / "outer.sentinel").write_text("outer", encoding="utf-8")
    case = create_bounded_case(tmp_path, case_name)
    if case.target_directory is not None:
        populate_non_empty_target(workflow, case.target_directory)

    result = run_cleanup(
        workflow,
        tmp_path,
        case.directory_value,
        case.invocation_directory,
    )

    assert result.returncode != 0
    assert_scope_is_preserved(tmp_path, case)
    if case.target_directory is not None:
        assert not (case.target_directory / workflow.artefact_name).exists()


@given(
    workflow=st.sampled_from(WORKFLOWS),
    directory_name=SAFE_DIRECTORY_NAMES,
)
@settings(max_examples=25, deadline=None)
def test_cleanup_scope_for_generated_directory_names(
    workflow: CleanupWorkflow, directory_name: str
) -> None:
    """Generated names preserve scope; fixture disposal is not under test."""
    with tempfile.TemporaryDirectory(prefix="temporary-cleanup-property-") as directory:
        root = Path(directory)
        case = BoundedCase(
            name="generated",
            directory_value=f"nested/{directory_name}",
            invocation_directory=root / "work",
            target_directory=root / "work" / "nested" / directory_name,
        )
        (root / "outer.sentinel").write_text("outer", encoding="utf-8")
        (root / case.name).mkdir()
        (root / case.name / "parent.sentinel").write_text("parent", encoding="utf-8")
        (root / case.name / "sibling").mkdir()
        (root / case.name / "sibling" / "sibling.sentinel").write_text(
            "sibling", encoding="utf-8"
        )
        assert case.target_directory is not None
        case.invocation_directory.mkdir(parents=True)
        case.target_directory.mkdir(parents=True)
        populate_non_empty_target(workflow, case.target_directory)

        result = run_cleanup(
            workflow,
            root,
            case.directory_value,
            case.invocation_directory,
        )

        assert result.returncode != 0
        assert_scope_is_preserved(root, case)
        assert not (case.target_directory / workflow.artefact_name).exists()
