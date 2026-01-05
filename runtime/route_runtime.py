from models.routes.route_stage import RouteStage
from runtime.event_manager import EventManager
from runtime.stage_runtime import StageRuntime
from models.routes.route import Route
from models.trains.train import Train
from models.routes.route_stage_station import RouteStageStation
from models.routes.route_stage_segment import RouteStageSegment
from models.events.train_events import (
    TrainFinishedSegment,
    TrainArrivedAtStation,
    TrainFinishedStationWait,
    TrainDepartedFromStation,
)


class RouteRuntime:
    def __init__(self, route: Route, train: Train, event_manager: EventManager):
        self.route = route
        self.train = train
        self.event_manager = event_manager

        self.stage_index = 0
        self.stage_runtime = None
        self.finished = False

        event_manager.subscribe(TrainFinishedSegment, self._on_finished_segment)
        event_manager.subscribe(TrainFinishedStationWait, self._on_finished_station_wait)

        # стартуем с первой стадии
        self._enter_stage(self.route.stages[0])

    @property
    def current_stage(self) -> StageRuntime | None:
        return self.stage_runtime

    def _enter_stage(self, stage):
        if isinstance(stage, RouteStageStation):
            self.train.set_speed(0.0)
            self.event_manager.emit(
                TrainArrivedAtStation(self.train, stage.station)
            )

        elif isinstance(stage, RouteStageSegment):
            speed = min(self.train.max_speed, stage.segment.max_speed)
            self.train.set_speed(speed)
            self.event_manager.emit(
                TrainDepartedFromStation(self.train, stage.segment.station_from)
            )

        self.stage_runtime = StageRuntime(
            stage,
            self.train,
            self.event_manager
        )

    def _on_finished_segment(self, event: TrainFinishedSegment):
        if event.train is not self.train:
            return

        self.stage_index += 1

        if self.stage_index >= len(self.route.stages):
            self.finished = True
            return

        self._enter_stage(self.route.stages[self.stage_index])

    def _on_finished_station_wait(self, event: TrainFinishedStationWait):
        if event.train is not self.train:
            return

        self.stage_index += 1

        if self.stage_index >= len(self.route.stages):
            self.finished = True
            return

        self._enter_stage(self.route.stages[self.stage_index])

    def advance(self, dt: float) -> None:
        remaining: float = dt

        while remaining > 0.0 and not self.finished:
            remaining = self.stage_runtime.advance(remaining)

    def __str__(self):
        return str(self.stage_runtime)
