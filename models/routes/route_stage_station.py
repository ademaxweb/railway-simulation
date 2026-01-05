from .route_stage import RouteStage
from models.stations import Station

class RouteStageStation(RouteStage):
    def __init__(self, station: Station, stop_time: float):
        self.station = station
        self.stop_time = stop_time

    def to_dict(self) -> dict:
        return {
            "id": self.station.id,
            "type": "station"
        }