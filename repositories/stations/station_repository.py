from abc import ABC, abstractmethod
from typing import Iterable
from models.stations import Station
from utils import ID

class StationRepository(ABC):
    @abstractmethod
    def get_by_id(self, station_id: ID) -> Station | None:
        pass


    @abstractmethod
    def get_all(self) -> Iterable[Station]:
        pass

