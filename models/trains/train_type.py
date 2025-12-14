from .train import  Train
from .types import PassengerTrain, ExpressTrain, FreightTrain, LongDistanceTrain, UnknownTrain
from enum import Enum
from typing import Type

class TrainType(str, Enum):
    UNKNOWN = "unknown"
    PASSENGER = "passenger"
    EXPRESS = "express"
    FREIGHT = "freight"
    LONG_DISTANCE = "long_distance"

    def __str__(self):
        return {
            TrainType.UNKNOWN: "Unknown",
            TrainType.PASSENGER: "Пассажирский",
            TrainType.EXPRESS: "Экспресс",
            TrainType.FREIGHT: "Грузовой",
            TrainType.LONG_DISTANCE: "Дальнего следования",
        }[self]

    @classmethod
    def from_str(cls, s: str) -> "TrainType":
        try:
            return cls(s.lower())
        except ValueError:
            return cls.UNKNOWN


    def train_class(self) -> Type[Train]:
        return {
            TrainType.UNKNOWN: UnknownTrain,
            TrainType.PASSENGER: PassengerTrain,
            TrainType.EXPRESS: ExpressTrain,
            TrainType.FREIGHT: FreightTrain,
            TrainType.LONG_DISTANCE: LongDistanceTrain,
        }[self]

