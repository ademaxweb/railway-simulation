from typing import Iterable, Tuple

from models.events.time_events import (
    TimeMarkerReached,
    RushHourStarted,
    RushHourEnded,
)


class RushHourRuntime:
    """
    Управляет режимом «час-пик» на основе интервалов времени суток.

    Интервалы задаются в секундах внутри суток:
    [(start_sec, end_sec), ...]
    где start_sec <= t < end_sec  → час-пик
    """

    DAY_SECONDS: int = 24 * 3600

    def __init__(
        self,
        event_manager,
        intervals: Iterable[Tuple[int, int]],
    ):
        self.event_manager = event_manager

        # интервалы час-пика (в секундах суток)
        self._intervals: list[Tuple[int, int]] = list(intervals)

        self._is_rush: bool = False

        event_manager.subscribe(
            TimeMarkerReached,
            self._on_time_marker,
        )

    @property
    def is_rush(self) -> bool:
        return self._is_rush

    def _on_time_marker(self, event: TimeMarkerReached) -> None:
        # время внутри суток
        day_time: int = int(event.sim_time) % self.DAY_SECONDS

        in_rush: bool = any(
            start <= day_time < end
            for start, end in self._intervals
        )

        if in_rush and not self._is_rush:
            self._is_rush = True
            self.event_manager.emit(RushHourStarted())

        elif not in_rush and self._is_rush:
            self._is_rush = False
            self.event_manager.emit(RushHourEnded())
