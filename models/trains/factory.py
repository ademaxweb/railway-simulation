from .dto import TrainConfig, train_config_from_dict
from .registry import TRAIN_REGISTRY

def create_train(o: TrainConfig):
    train_class = TRAIN_REGISTRY[o.type]
    return train_class(o)

def create_train_from_dict(d: dict):
    train_dto = train_config_from_dict(d)
    return create_train(train_dto)