from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=False)
class StatisticsDataDaily:
    total_persons: int = 0
    by_stations: list = field(default_factory=list)
    max_delay: float = 0
    min_delay: float = 0

    def to_dict(self):
        return {
            'total_persons': self.total_persons,
            'by_stations': self.by_stations,
            'max_delay': self.max_delay,
            'min_delay': self.min_delay
        }