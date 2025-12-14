from .station import Station
from .dto import StationConfig, station_config_from_dict

def create_station(o: StationConfig) -> Station:
    return Station(o)

def create_station_from_dict(d: dict) -> Station:
    station_dto = station_config_from_dict(d)
    return create_station(station_dto)