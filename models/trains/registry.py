from typing import Dict, Type

from .train_type import TrainType
from .train import Train

TRAIN_REGISTRY: Dict[TrainType, Type[Train]] = {}

def register_train_class(train_type: TrainType):
    def decorator(cls: Type[Train]) -> Type[Train]:
        TRAIN_REGISTRY[train_type] = cls
        return cls
    return decorator
