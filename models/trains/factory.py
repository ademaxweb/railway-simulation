import json
from typing import Any, Dict

from . import Train, TrainType, UnknownTrain
from .registry import TRAIN_REGISTRY

def train_from_dict(data: Dict[str, Any]) -> Train:
    train_type = TrainType.from_str(data.get("type", "unknown"))
    train_class = TRAIN_REGISTRY.get(train_type, UnknownTrain)

    return train_class(
        wagon_count=data.get("wagon_count", 0),
        wagon_capacity=data.get("wagon_capacity", 0),
        model_name=data.get("model_name", "unknown"),
        max_speed=data.get("max_speed", 0.0),
    )

def train_from_json(json_data: str) -> Train:
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON for train") from e

    return train_from_dict(data)
