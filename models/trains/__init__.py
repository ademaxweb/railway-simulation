from .train_type import TrainType
from .dto import TrainConfig, train_config_from_dict
from .wagon import Wagon
from .train import Train
from .types import PassengerTrain, ExpressTrain, FreightTrain, LongDistanceTrain
from .factory import create_train, create_train_from_dict

# Для регистрации в реестре
from . import types as _types

__all__ = [
    "TrainType",
    "TrainConfig",
    "Wagon",
    "Train",
    "create_train",
    "create_train_from_dict",
    "train_config_from_dict",
    "PassengerTrain",
    "ExpressTrain",
    "FreightTrain",
    "LongDistanceTrain",
]
