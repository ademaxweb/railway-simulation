from dataclasses import dataclass
from models.events.statistics_event import DelayStatistics as EventDelayStatistics


@dataclass(frozen=False)
class DelayStatisticsData:
    max_delay: float = 0
    min_delay: float = 0
    total_delay: float = 0
    routes_count: int = 0

    def clear(self):
        self.max_delay = 0
        self.min_delay = 0
        self.total_delay = 0

    @property
    def avg_delay(self):
        if self.routes_count == 0:
            return 0

        return self.total_delay / self.routes_count


    def to_dict(self) -> dict:
        return {
            'max_delay': self.max_delay,
            'min_delay': self.min_delay,
            'avg_delay': self.avg_delay,
            'total_delay': self.total_delay,
        }


def event_to_delay_statistics_data(event: EventDelayStatistics) -> DelayStatisticsData:
    stats = DelayStatisticsData()

    stats.clear()

    if not event.delays:
        return stats

    stats.routes_count = len(event.delays)

    stats.min_delay = event.delays[0]


    for d in event.delays:
        stats.total_delay += d
        stats.max_delay = max(stats.max_delay, d)
        stats.min_delay = min(stats.min_delay, d)


    return stats
