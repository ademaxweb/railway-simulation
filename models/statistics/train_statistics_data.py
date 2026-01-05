from dataclasses import dataclass
from models.events.statistics_event import TrainsStatistics as EventTrainsStatistics


@dataclass(frozen=False)
class TrainsStatisticsData:
    trains_count: int = 0
    total_persons: int = 0
    total_fullness_percentage: float = 0
    total_speed: float = 0

    max_speed: float = 0
    max_fullness_percentage: float = 0
    max_persons: int = 0

    min_speed: float = 0
    min_fullness_percentage: float = 0
    min_persons: int = 0

    def clear(self):
        self.trains_count = 0
        self.total_persons = 0
        self.total_fullness_percentage = 0
        self.total_speed = 0
        self.max_speed = 0
        self.max_fullness_percentage = 0
        self.max_persons = 0
        self.min_speed = 0
        self.min_fullness_percentage = 0
        self.min_persons = 0

    @property
    def avg_persons_in_train(self) -> float:
        if self.trains_count <= 0:
            return 0
        return self.total_persons / self.trains_count

    @property
    def avg_fullness_percentage(self) -> float:
        if self.trains_count <= 0:
            return 0

        return self.total_fullness_percentage / self.trains_count

    @property
    def avg_speed(self) -> float:
        if self.trains_count <= 0:
            return 0

        return self.total_speed / self.trains_count

    def to_dict(self) -> dict:
        return {
            "trains_count": round(self.trains_count, 2),
            "total_persons": round(self.total_persons, 2),
            "avg_persons_in_train": round(self.avg_persons_in_train, 2),
            "avg_fullness_percentage": round(self.avg_fullness_percentage, 2),
            "avg_speed": round(self.avg_speed, 2),
            "max_speed": round(self.max_speed, 2),
            "max_fullness_percentage": round(self.max_fullness_percentage, 2),
            "max_persons": round(self.max_persons, 2),
            "min_speed": round(self.min_speed, 2),
            "min_fullness_percentage": round(self.min_fullness_percentage, 2),
            "min_persons": round(self.min_persons, 2)
        }


def event_to_train_statistics_data(event: EventTrainsStatistics) -> TrainsStatisticsData:
    stats = TrainsStatisticsData()

    stats.clear()

    if not event.trains:
        return stats

    stats.trains_count = len(event.trains)

    first_train = event.trains[0]

    stats.min_persons = first_train.person_count
    stats.min_speed = first_train.speed
    stats.min_fullness_percentage = first_train.filling_percentage

    for t in event.trains:
        stats.total_persons += t.person_count
        stats.total_fullness_percentage += t.filling_percentage

        if stats.max_speed < t.speed:
            stats.max_speed = t.speed

        if stats.max_persons < t.person_count:
            stats.max_persons = t.person_count

        if stats.max_fullness_percentage < t.filling_percentage:
            stats.max_fullness_percentage = t.filling_percentage

        if stats.min_persons > t.person_count:
            stats.min_persons = t.person_count

        if stats.min_fullness_percentage > t.filling_percentage:
            stats.min_fullness_percentage = t.filling_percentage

        if stats.min_speed > t.speed:
            stats.min_speed = t.speed

    return stats
