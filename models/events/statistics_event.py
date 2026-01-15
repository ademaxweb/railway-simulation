from models.events.event import Event
from models.statistics.statistics_data_daily import StatisticsDataDaily
from models.trains import Train
from typing import List
from runtime.simulation_date_time import SimDate


class TrainsStatistics(Event):
    def __init__(self, trains: List[Train]):
        self.trains = trains
        super().__init__()

class DelayStatistics(Event):
    def __init__(self, delays: List[float]):
        self.delays = delays
        super().__init__()

class SaveStatistics(Event):
    def __init__(self, sim_date: SimDate):
        self.date = sim_date
        super().__init__()

class SaveDailyStatistics(Event):
    def __init__(self, sim_date: SimDate, stats: StatisticsDataDaily):
        self.date = sim_date
        self.stats = stats
        super().__init__()