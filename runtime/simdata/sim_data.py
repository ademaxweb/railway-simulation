from typing import List

from runtime.route_runtime import RouteRuntime
from .sim_data_route import SimDataRoute
from .sim_data_station import SimDataStation
from ..simulation_date_time import SimDate
from ..station_runtime import StationRuntime


class SimData:
    def __init__(self, sim_time: float):
        self._stations: List[SimDataStation] = []
        self._routes: List[SimDataRoute] = []
        self._time = SimDate(sim_time)
        self._rush_status = False


    def add_route_data(self, rr: RouteRuntime):
        self._routes.append(SimDataRoute(rr.current_stage.stage, rr.current_stage.progress_percentage, rr.train))

    def add_station_data(self, sr: StationRuntime):
        self._stations.append(SimDataStation(sr.station))

    def set_rush_status(self, b: bool):
        self._rush_status = b

    def to_dict(self):
        return {
            "time": self._time.to_dict(),
            "is_rush": self._rush_status,
            "stations": list(map(lambda x: x.to_dict(), self._stations)),
            "routes": list(map(lambda x: x.to_dict(), self._routes)),
        }