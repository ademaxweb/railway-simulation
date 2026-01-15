from dataclasses import dataclass, field

from models.statistics.delay_statistics_data import DelayStatisticsData, event_to_delay_statistics_data
from models.statistics.train_statistics_data import TrainsStatisticsData, event_to_train_statistics_data
from models.events.statistics_event import TrainsStatistics as EventTrainsStatistics, DelayStatistics as EventDelayStatistics

@dataclass(frozen=False)
class StatisticsData:
    trains: TrainsStatisticsData = field(default_factory=TrainsStatisticsData)
    delays: DelayStatisticsData = field(default_factory=DelayStatisticsData)

    def clear(self):
        self.trains.clear()
        self.delays.clear()

    def to_dict(self) -> dict:
        return {
            "trains" : self.trains.to_dict(),
            "delays": self.delays.to_dict(),
        }

    def set_trains(self, event: EventTrainsStatistics):
        self.trains = event_to_train_statistics_data(event)

    def set_delays(self, event: EventDelayStatistics):
        self.delays = event_to_delay_statistics_data(event)
