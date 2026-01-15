from typing import List
from .route_stage import RouteStage
from .route_stage_station import RouteStageStation
from models.stations import Station

class Route:
    def __init__(self, stages: List[RouteStage]):
        self.stages: List[RouteStage] = stages

    def __len__(self):
        return len(self.stages)

    def get_first_station(self) -> RouteStageStation | None:
        def check(stage: RouteStage):
            return isinstance(stage, RouteStageStation)

        stations = filter(check, self.stages)
        return next(stations, None)
