from dataclasses import dataclass, field
from models.statistics.train_statistics_data import TrainsStatisticsData, event_to_train_statistics_data
from models.events.statistics_event import TrainsStatistics as EventTrainsStatistics

@dataclass(frozen=False)
class StatisticsData:
    trains: TrainsStatisticsData = field(default_factory=TrainsStatisticsData)

    def clear(self):
        self.trains.clear()

    def to_dict(self) -> dict:
        return {
            "trains" : self.trains.to_dict()
        }

    def set_trains(self, event: EventTrainsStatistics):
        self.trains = event_to_train_statistics_data(event)
