import pytest

from domain.enums import RunStatus
from domain.exceptions import InvalidRunTransition
from domain.run import Run


def test_run_is_created_with_default_values():
    run = Run()

    assert run.status == RunStatus.CREATED
    assert run.id is not None
    assert run.created_at is not None
    assert run.started_at is None
    assert run.finished_at is None


def test_run_can_transition_to_running():
    run = Run()

    run.transition_to(RunStatus.RUNNING)

    assert run.status == RunStatus.RUNNING
    assert run.started_at is not None


def test_run_can_be_paused_and_resumed():
    run = Run()

    run.transition_to(RunStatus.RUNNING)
    original_started_at = run.started_at

    run.transition_to(RunStatus.PAUSED)
    run.transition_to(RunStatus.RUNNING)

    assert run.status == RunStatus.RUNNING
    assert run.started_at == original_started_at


def test_completed_run_cannot_be_restarted():
    run = Run()

    run.transition_to(RunStatus.RUNNING)
    run.transition_to(RunStatus.COMPLETED)

    with pytest.raises(InvalidRunTransition):
        run.transition_to(RunStatus.RUNNING)

    assert run.status == RunStatus.COMPLETED


def test_created_run_can_be_cancelled():
    run = Run()

    run.transition_to(RunStatus.CANCELLED)

    assert run.status == RunStatus.CANCELLED
    assert run.finished_at is not None
