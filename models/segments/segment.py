from .dto import SegmentConfig
from utils import ID


class Segment:

    def __init__(self, cfg: SegmentConfig):
        self._id: ID = ID()
        self._to = cfg.station_to
        self._from = cfg.station_from
        self._distance: float = cfg.distance
        self._max_speed: float = cfg.max_speed


    def __repr__(self):
        return f"{self._from.name}--- {self._distance:.2f}км ---> {self._to.name}"