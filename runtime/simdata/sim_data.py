from typing import List

from runtime.route_runtime import RouteRuntime
from .sim_data_route import SimDataRoute
from .sim_data_station import SimDataStation
from ..station_runtime import StationRuntime


class SimData:
    def __init__(self):
        self._stations: List[SimDataStation] = []
        self._routes: List[SimDataRoute] = []

    def add_route_data(self, rr: RouteRuntime):
        self._routes.append(SimDataRoute(rr.current_stage.stage, rr.current_stage.progress_percentage, rr.train))

    def add_station_data(self, sr: StationRuntime):
        self._stations.append(SimDataStation(sr.station))

    def to_dict(self):
        return {
            "stations": list(map(lambda x: x.to_dict(), self._stations)),
            "routes": list(map(lambda x: x.to_dict(), self._routes)),
        }