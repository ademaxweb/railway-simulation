from models.events.event import Event
from runtime.simdata.sim_data import SimData

class SimulationDataUpdate(Event):
    def __init__(self, sim_data: SimData):
        self.sim_data: SimData = sim_data
        super().__init__()