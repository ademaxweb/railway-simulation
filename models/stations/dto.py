import json
from dataclasses import dataclass
from typing import Dict, Any
from utils import ID


@dataclass(frozen=True)
class StationConfig:
    id: ID
    name: str
    capacity: int


def station_config_from_dict(d: Dict[str, Any]) -> StationConfig:
    return StationConfig(
        id=ID(int(d.get("id", 0))),
        name=d.get("name", ""),
        capacity=int(d.get("capacity", 0)),
    )

def station_config_from_json(s: str) -> StationConfig:
    return station_config_from_dict(json.loads(s))