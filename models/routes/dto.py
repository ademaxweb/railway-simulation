from models.stations import Station
from dataclasses import dataclass
from typing import List, Dict, Any
from repositories.stations import StationRepository
from utils import ID

@dataclass
class RouteStationConfig:
    station: Station
    base_stop_time: int

@dataclass
class RouteConfig:
    name: str
    stations: List[RouteStationConfig]


def route_station_config_from_dict(d: Dict[str, Any], repo: StationRepository) -> RouteStationConfig:
    station_id = ID(int(d.get("station_id")))

    return RouteStationConfig(
        station=repo.get_by_id(station_id),
        base_stop_time=int(d.get("base_stop_time", 0)),
    )

def route_config_from_dict(d: Dict[str, Any], repo: StationRepository) -> RouteConfig:
    stations = [route_station_config_from_dict(s, repo) for s in d.get("stations", [])]

    return RouteConfig(
        name=d.get("name", ""),
        stations=stations
    )