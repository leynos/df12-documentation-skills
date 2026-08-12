"""Behavioural coverage for complete documented temporary-file workflows."""

from __future__ import annotations

import dataclasses as dc
import re
import shutil
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from cmd_mox import CmdMox
    from cmd_mox.ipc import Invocation

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
pytest_plugins = ("cmd_mox.pytest_plugin",)


@dc.dataclass(frozen=True)
class _DocumentedWorkflow:
    """Describe one complete workflow block and its external command."""

    name: str
    skill_path: Path
    directory_variable: str
    cleanup_function: str
    artefact_name: str
    command_name: str
    command_calls: int
    failure_subcommand: str


@dc.dataclass(frozen=True)
class _WorkflowCase:
    """Describe one success, failure, or absent-artefact workflow case."""

    name: str
    expected_status: int
    remove_artefact: bool


WORKFLOWS = (
    _DocumentedWorkflow(
        name="commit",
        skill_path=Path("skills/commit-message/SKILL.md"),
        directory_variable="COMMIT_MSG_DIR",
        cleanup_function="cleanup_commit_message",
        artefact_name="COMMIT_MSG.md",
        command_name="git",
        command_calls=4,
        failure_subcommand="commit",
    ),
    _DocumentedWorkflow(
        name="pr",
        skill_path=Path("skills/pr-creation/SKILL.md"),
        directory_variable="PR_BODY_DIR",
        cleanup_function="cleanup_pr_body",
        artefact_name="body.md",
        command_name="gh",
        command_calls=1,
        failure_subcommand="pr",
    ),
)
CASES = (
    _WorkflowCase(name="success", expected_status=0, remove_artefact=False),
    _WorkflowCase(name="failure", expected_status=1, remove_artefact=False),
    _WorkflowCase(name="absent-success", expected_status=0, remove_artefact=True),
    _WorkflowCase(name="absent-failure", expected_status=1, remove_artefact=True),
)


def _extract_documented_workflow(workflow: _DocumentedWorkflow) -> str:
    """Return the complete documented shell block for ``workflow``."""
    skill_text = (REPOSITORY_ROOT / workflow.skill_path).read_text(encoding="utf-8")
    pattern = re.compile(
        rf"```bash\n(?P<script>(?:(?!```)[\s\S])*?{workflow.directory_variable}=.*?"
        rf"trap - EXIT\n{workflow.cleanup_function}\n)```",
        flags=re.DOTALL,
    )
    match = pattern.search(skill_text)
    if match is None:
        msg = f"Could not extract workflow from {workflow.skill_path}"
        raise AssertionError(msg)
    return match.group("script")


def _find_posix_shell() -> str:
    """Return the shell used for complete documented workflow execution."""
    shell_path = shutil.which("sh")
    if shell_path is None:
        msg = "A POSIX shell is required to execute documented workflows"
        raise AssertionError(msg)
    return shell_path


def _assert_external_command(
    workflow: _DocumentedWorkflow,
    invocations: list[Invocation],
    artefact_path: Path,
) -> None:
    """Assert the documented external command was called with its exact contract."""
    command_arguments = [tuple(invocation.args) for invocation in invocations]
    if workflow.name == "commit":
        assert command_arguments[:3] == [
            ("diff", "--cached"),
            ("diff",),
            ("status", "--short"),
        ], "documented commit preflight commands must run"
        assert command_arguments[3] == ("commit", "-F", str(artefact_path)), (
            "documented commit command must use the temporary message file"
        )
        return
    assert command_arguments == [
        (
            "pr",
            "create",
            "--draft",
            "--title",
            "<title>",
            "--body-file",
            str(artefact_path),
        )
    ], "documented PR command must use the temporary body file"


@pytest.mark.cmd_mox(auto_lifecycle=False)
@pytest.mark.parametrize("workflow", WORKFLOWS, ids=lambda workflow: workflow.name)
@pytest.mark.parametrize("case", CASES, ids=lambda case: case.name)
def test_documented_workflow_cleans_temporary_files(
    tmp_path: Path,
    workflow: _DocumentedWorkflow,
    case: _WorkflowCase,
    cmd_mox: CmdMox,
) -> None:
    """Run each complete workflow through explicit and EXIT-trap cleanup paths."""
    temporary_directory = tmp_path / "temporary"
    sibling_directory = tmp_path / "sibling"
    artefact_path = temporary_directory / workflow.artefact_name
    temporary_directory.mkdir()
    sibling_directory.mkdir()
    (tmp_path / "parent.sentinel").write_text("parent", encoding="utf-8")
    (sibling_directory / "sibling.sentinel").write_text("sibling", encoding="utf-8")
    removed_artefacts: list[Path] = []

    def _external_response(invocation: Invocation) -> tuple[str, str, int]:
        """Return the controlled external-command response for this case."""
        if invocation.args[0] == workflow.failure_subcommand:
            if case.remove_artefact:
                artefact_path.unlink()
                removed_artefacts.append(artefact_path)
            return "", "", case.expected_status
        return "", "", 0

    cmd_mox.mock("mktemp").with_args("-d").returns(stdout=f"{temporary_directory}\n")
    external_command = cmd_mox.mock(workflow.command_name).runs(_external_response)
    external_command.times(workflow.command_calls)
    cmd_mox.replay()

    result = subprocess.run(
        [_find_posix_shell(), "-ec", _extract_documented_workflow(workflow)],
        capture_output=True,
        check=False,
        cwd=tmp_path,
        text=True,
    )

    cmd_mox.verify()
    _assert_external_command(workflow, external_command.invocations, artefact_path)
    assert result.returncode == case.expected_status, (
        "documented workflow must return its mocked command status"
    )
    assert not temporary_directory.exists(), "temporary directory must be removed"
    assert (tmp_path / "parent.sentinel").is_file(), "parent sentinel must remain"
    assert (sibling_directory / "sibling.sentinel").is_file(), (
        "sibling sentinel must remain"
    )
    assert sibling_directory.is_dir(), "sibling directory must remain"
    if case.remove_artefact:
        assert removed_artefacts == [artefact_path], (
            "absent-artefact case must remove the generated artefact before cleanup"
        )
