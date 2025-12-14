import json
from dataclasses import dataclass
from typing import Any, Dict

from .train_type import TrainType

@dataclass(frozen=True)
class TrainConfig:
    type: TrainType
    wagon_count: int
    wagon_capacity: int
    model_name: str
    max_speed: float


def train_config_from_dict(d: Dict[str, Any]) -> TrainConfig:
    return TrainConfig(
        type=TrainType.from_str(d.get("type", "unknown")),
        wagon_count=int(d.get("wagon_count", 0)),
        wagon_capacity=int(d.get("wagon_capacity", 0)),
        model_name=d.get("model_name", ""),
        max_speed=float(d.get("max_speed", 0)),
    )

def train_config_from_json(s: str) -> TrainConfig:
    return train_config_from_dict(json.loads(s))