from models.events.event import Event
from models.trains import Train
from typing import List
from runtime.simulation_date_time import SimDate


class TrainsStatistics(Event):
    def __init__(self, trains: List[Train]):
        self.trains = trains
        super().__init__()


class SaveStatistics(Event):
    def __init__(self, sim_date: SimDate):
        self.date = sim_date
        super().__init__()