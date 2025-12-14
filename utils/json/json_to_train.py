from models.trains import Train, TrainType
import json


def json_to_train(data: str)->Train:
    train_data: dict = json.loads(data)

    train_type = TrainType.from_str(train_data.get('train_type', 'unknown'))
    train_class = train_type.train_class()

    return train_class(
        wagon_count=train_data.get('wagon_count', 0),
        wagon_capacity=train_data.get('wagon_capacity', 0),
        model_name=train_data.get('model', 'unknown'),
        max_speed=train_data.get('max_speed', 0),
    )