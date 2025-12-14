from abc import ABC, abstractmethod
from typing import Iterable
from models.stations import Station

class StationRepository(ABC):
    @abstractmethod
    def get_all(self) -> Iterable[Station]:
        pass