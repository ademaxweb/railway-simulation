from enum import Enum

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
