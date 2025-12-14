from ..train_type import TrainType
from ..train import Train
from ..registry import register_train_class

@register_train_class(TrainType.FREIGHT)
class FreightTrain(Train):
    def __init__(self, wagon_count: int, wagon_capacity: int, model_name: str = ""):
        super().__init__(
            t=TrainType.FREIGHT,
            max_speed=120,
            model_name=model_name,
            wagon_count=wagon_count,
            wagon_capacity=wagon_capacity
        )