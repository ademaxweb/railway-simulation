from models.events.time_events import TimeMarkerReached, NewDayMarker

class TimeModeRuntime:
    DAY_SECONDS = 24 * 3600

    def __init__(
        self,
        event_manager,
        info_interval: float = 3600.0,
    ):
        self.event_manager = event_manager

        self._info_interval: float = info_interval
        self._next_info_mark: float = info_interval
        self._last_day_time: float = 0.0

    def advance(self, sim_time: float) -> None:
        day_time: float = sim_time % self.DAY_SECONDS

        # --- начало новых суток ---
        if day_time < self._last_day_time:
            self.event_manager.emit(
                TimeMarkerReached(0.0)
            )
            self.event_manager.emit(
                NewDayMarker()
            )
            self._next_info_mark = self._info_interval

        self._last_day_time = day_time

        # --- временные маркеры ---
        while day_time >= self._next_info_mark:
            self.event_manager.emit(
                TimeMarkerReached(self._next_info_mark)
            )
            self._next_info_mark += self._info_interval
