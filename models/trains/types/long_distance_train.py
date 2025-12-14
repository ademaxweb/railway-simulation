from ..train import Train
from ..train_type import TrainType
from ..registry import register_train_class

@register_train_class(TrainType.LONG_DISTANCE)
class LongDistanceTrain(Train):
    def __init__(
            self,
            wagon_count: int = 0,
            wagon_capacity: int = 0,
            max_speed: float = 80.0,
            model_name: str = "",
    ):
        super().__init__(
            t=TrainType.LONG_DISTANCE,
            max_speed=max_speed,
            model_name=model_name,
            wagon_count=wagon_count,
            wagon_capacity=wagon_capacity
        )
