from ..train_type import TrainType
from ..train import Train


class UnknownTrain(Train):
    def __init__(self, wagon_count: int, wagon_capacity: int, model_name: str = ""):
        super().__init__(
            t=TrainType.UNKNOWN,
            max_speed=0,
            model_name=model_name,
            wagon_count=wagon_count,
            wagon_capacity=wagon_capacity
        )