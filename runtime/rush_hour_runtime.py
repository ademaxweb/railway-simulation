from models.events.time_events import (
    TimeMarkerReached,
    RushHourStarted,
    RushHourEnded,
)


class RushHourRuntime:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self._is_rush: bool = False

        # часы начала и конца
        self._start_hours = {7, 17}
        self._end_hours = {9, 19}

        event_manager.subscribe(
            TimeMarkerReached,
            self._on_time_marker,
        )

    def _on_time_marker(self, event: TimeMarkerReached) -> None:
        total = int(event.sim_time)
        hour = total // 3600

        if hour in self._start_hours and not self._is_rush:
            self._is_rush = True
            self.event_manager.emit(RushHourStarted())

        elif hour in self._end_hours and self._is_rush:
            self._is_rush = False
            self.event_manager.emit(RushHourEnded())
