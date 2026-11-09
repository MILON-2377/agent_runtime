from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from domain.enums import RunStatus
from domain.exceptions import InvalidRunTransition
from domain.transitions import ALLOWED_RUN_TRANSITIONS


@dataclass
class Run:
    id: UUID = field(default_factory=uuid4)

    status: RunStatus = RunStatus.CREATED

    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    started_at: datetime | None = None

    finished_at: datetime | None = None

    def transition_to(self, target_status: RunStatus) -> None:

        allowed_statues = ALLOWED_RUN_TRANSITIONS[self.status]

        if target_status not in allowed_statues:
            raise InvalidRunTransition(
                current_status=self.status.value, target_status=target_status.value
            )

        now = datetime.now(timezone.utc)

        self.status = target_status

        if target_status == RunStatus.RUNNING and self.started_at is None:
            self.started_at = now

        if target_status in {
            RunStatus.COMPLETED,
            RunStatus.FAILED,
            RunStatus.CANCELLED,
            RunStatus.TIMED_OUT,
        }:
            self.finished_at = now
