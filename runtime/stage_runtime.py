from models.routes.route_stage_station import RouteStageStation
from models.routes.route_stage_segment import RouteStageSegment
from models.events.train_events import (
    TrainFinishedSegment,
    TrainFinishedStationWait,
)


class StageRuntime:
    def __init__(self, stage, train, event_manager):
        self.stage = stage
        self.train = train
        self.event_manager = event_manager
        self.finished = False

        if isinstance(stage, RouteStageStation):
            self.time_left = stage.stop_time

        elif isinstance(stage, RouteStageSegment):
            self.distance_left = stage.segment.distance

    def advance(self, dt: float) -> float:
        if self.finished:
            return dt

        if isinstance(self.stage, RouteStageStation):
            if dt >= self.time_left:
                dt -= self.time_left
                self.finished = True
                self.event_manager.emit(
                    TrainFinishedStationWait(self.train)
                )
                return dt
            else:
                self.time_left -= dt
                return 0.0

        elif isinstance(self.stage, RouteStageSegment):
            speed = self.train.speed
            step = speed * dt / 3600

            if step >= self.distance_left:
                time_spent = self.distance_left / speed * 3600
                dt -= time_spent
                self.finished = True
                self.event_manager.emit(
                    TrainFinishedSegment(self.train)
                )
                return dt
            else:
                self.distance_left -= step
                return 0.0

        return dt

    def __str__(self):
        if isinstance(self.stage, RouteStageStation):
            return (
                f"Стоянка: {self.stage.station.name} | "
                f"{self.time_left:.1f}s"
            )

        return (
            f"Перегон: {self.stage.segment.station_from.name}"
            f" → {self.stage.segment.station_to.name} | "
            f"{self.distance_left:.2f} км"
        )
