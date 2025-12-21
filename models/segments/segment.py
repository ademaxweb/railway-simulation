from .dto import SegmentConfig
from utils import ID
from models.stations import Station

class Segment:

    def __init__(self, cfg: SegmentConfig):
        self._id: ID = ID()
        self._to: Station = cfg.station_to
        self._from: Station = cfg.station_from
        self._distance: float = cfg.distance
        self._max_speed: float = cfg.max_speed


    @property
    def id(self) -> ID:
        return self._id

    @property
    def station_from(self) -> Station:
        return self._from

    @property
    def station_to(self) -> Station:
        return self._to

    @property
    def distance(self) -> float:
        return self._distance

    @property
    def max_speed(self) -> float:
        return self._max_speed

    def __repr__(self):
        return f"{self._from.name}--- {self._distance:.2f}км ---> {self._to.name}"