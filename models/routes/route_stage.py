from utils import ID
from enum import Enum
from models.stations import Station
from models.segments import Segment
from .dto import RouteStationConfig

class RouteStageType(Enum):
    SEGMENT = 1
    STATION = 2

class RouteStage:
    def __init__(self, t: RouteStageType):
        self._id: ID = ID()
        self._type: RouteStageType = t


class RouteStageSegment(RouteStage):
    def __init__(self, s: Segment):
        self._segment: Segment = s
        super().__init__(RouteStageType.SEGMENT)


class RouteStageStation(RouteStage):
    def __init__(self, cfg: RouteStationConfig):
        self._station: Station = cfg.station
        self._base_stop_time: int = cfg.base_stop_time
        
        super().__init__(RouteStageType.STATION)
