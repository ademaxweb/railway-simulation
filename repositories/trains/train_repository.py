from abc import ABC, abstractmethod
from typing import Iterable
from models.trains import Train


class TrainRepository(ABC):
    @abstractmethod
    def get_all(self) -> Iterable[Train]:
        pass