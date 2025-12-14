from ..train_type import TrainType
from ..dto import TrainConfig
from ..train import Train
from ..registry import register_train_class

@register_train_class(TrainType.LONG_DISTANCE)
class LongDistanceTrain(Train):
    def __init__(self, cfg: TrainConfig):
        super().__init__(cfg)
