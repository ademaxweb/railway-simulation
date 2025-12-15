from abc import ABC, abstractmethod
from typing import Iterable
from models.segments import Segment
from models.stations import Station
from utils import ID


class SegmentRepository(ABC):
    @abstractmethod
    def get_all(self) -> Iterable[Segment]:
        pass

    @abstractmethod
    def get_by_id(self, segment_id: ID) -> Segment | None:
        pass

    @abstractmethod
    def get_from_station(self, station: Station) -> Iterable[Segment]:
        pass

    @abstractmethod
    def get_to_station(self, station: Station) -> Iterable[Segment]:
        pass

    @abstractmethod
    def get_between_stations(self, from_station: Station, to_station: Station) -> Segment | None:
        pass