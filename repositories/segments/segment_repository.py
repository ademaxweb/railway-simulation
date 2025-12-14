from abc import ABC, abstractmethod
from typing import Iterable
from models.segments import Segment


class SegmentRepository(ABC):
    @abstractmethod
    def get_all(self) -> Iterable[Segment]:
        pass