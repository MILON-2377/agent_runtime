from domain.enums import RunStatus
from domain.exceptions import InvalidRunTransition
from domain.run import Run

run = Run()
run.transition_to(RunStatus.RUNNING)
run.transition_to(RunStatus.COMPLETED)

try:
    run.transition_to(RunStatus.RUNNING)
    raise AssertionError("Expected InvalidRunTransition")
except InvalidRunTransition as exc:
    print("Correctly rejected:", exc)

assert run.status == RunStatus.COMPLETED

print("Invalid transition tests passed.")
