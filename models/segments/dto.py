import json
from dataclasses import dataclass
from models.stations import Station
from typing import Dict, Any
from utils import ID
from typing import Callable

@dataclass(frozen=True)
class SegmentConfig:
    station_from: Station | None
    station_to: Station | None
    distance: float
    max_speed: float


def segment_config_from_dict(d: Dict[str, Any], get_station_by_id: Callable[[ID], Station | None]) -> SegmentConfig:
    station_from_id = ID(int(d.get("station_from")))
    station_to_id = ID(int(d.get("station_to")))

    return SegmentConfig(
        station_from=get_station_by_id(station_from_id),
        station_to=get_station_by_id(station_to_id),
        distance=float(d.get("distance")),
        max_speed=float(d.get("max_speed"))
    )

def segment_config_from_json(s: str, get_station_by_id: Callable[[ID], Station | None]) -> SegmentConfig:
    return segment_config_from_dict(json.loads(s), get_station_by_id)