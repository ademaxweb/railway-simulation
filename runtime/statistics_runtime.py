from dataclasses import dataclass, field
from runtime.event_manager import EventManager
from runtime.simulation_date_time import SimDate
from models.events.statistics_event import TrainsStatistics as EventTrainsStatistics, SaveStatistics as EventSaveStatistics
from pathlib import Path
import json


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


@dataclass(frozen=False)
class StatisticsData:
    trains: TrainsStatisticsData = field(default_factory=TrainsStatisticsData)

    def clear(self):
        self.trains.clear()

    def to_dict(self) -> dict:
        return {
            "trains" : self.trains.to_dict()
        }



class StatisticsRuntime:
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager
        self.stats = StatisticsData()
        self.event_manager.subscribe(EventTrainsStatistics, self._on_trains_statistics)
        self.event_manager.subscribe(EventSaveStatistics, self._on_save_statistics)

        self._path = Path("stats/trains.json")


    def _append_to_json(self, time: SimDate):
        if self._path.exists():
            with self._path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        data.append({
            "time": time.to_dict(),
            "data": self.stats.to_dict()
        })

        with self._path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)



    def _on_trains_statistics(self, event: EventTrainsStatistics):
        self.stats.trains.clear()

        if not event.trains:
            return

        self.stats.trains.trains_count = len(event.trains)


        first_train = event.trains[0]

        self.stats.trains.min_persons = first_train.person_count
        self.stats.trains.min_speed = first_train.speed
        self.stats.trains.min_fullness_percentage = first_train.filling_percentage

        for t in event.trains:
            self.stats.trains.total_persons += t.person_count
            self.stats.trains.total_fullness_percentage += t.filling_percentage

            if self.stats.trains.max_speed < t.speed:
                self.stats.trains.max_speed = t.speed

            if self.stats.trains.max_persons < t.person_count:
                self.stats.trains.max_persons = t.person_count

            if self.stats.trains.max_fullness_percentage < t.filling_percentage:
                self.stats.trains.max_fullness_percentage = t.filling_percentage


            if self.stats.trains.min_persons > t.person_count:
                self.stats.trains.min_persons = t.person_count

            if self.stats.trains.min_fullness_percentage > t.filling_percentage:
                self.stats.trains.min_fullness_percentage = t.filling_percentage

            if self.stats.trains.min_speed > t.speed:
                self.stats.trains.min_speed = t.speed

    def _on_save_statistics(self, event: EventSaveStatistics):
        self._append_to_json(event.date)