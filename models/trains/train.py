
from .wagon import *
from enum import Enum

class TrainType(Enum):
    NULL = 0
    PASSENGER = 1
    EXPRESS = 2
    FREIGHT = 3
    LONG_DISTANCE = 4

    def __str__(self):
        match self:
            case TrainType.PASSENGER:
                return "Пассажирский"
            case TrainType.EXPRESS:
                return "Экспресс"
            case TrainType.FREIGHT:
                return "Грузовой"
            case TrainType.LONG_DISTANCE:
                return "Дальнего следования"
            case _:
                return "Null"

class Train:

    # Уникальный идентификатор
    id:int = 0
    # Тип поезда
    type:TrainType = TrainType.NULL
    # Вагоны
    wagons:list[Wagon] = list()
    # Скорость поезда
    velocity:float = 0.0
    # Максимальная скорость поезда
    max_velocity:float = 0.0

    # Constructor
    def __init__(self, train_type: TrainType, max_velocity: float):
        self.id:int = utils.generate_int_id()
        self.type = train_type
        self.max_velocity = max_velocity

    def __str__(self):
        wagons_str = "---".join(list(map(lambda w: str(w), self.wagons)))

        return f"<{str(self.type)} поезд № {self.id} ({ round(self.velocity, 2)} км/ч)]---{wagons_str}"


    # Добавить вагон
    def add_wagon(self, wagon:Wagon):
        self.wagons.append(wagon)

    # Установить сокрость
    def set_velocity(self, velocity: float):
        self.velocity = velocity



class PassengerTrain(Train):
    def __init__(self, wagon_count: int, wagon_capacity: int):
        super().__init__(TrainType.PASSENGER, 100)

        for _ in range(wagon_count):
            self.add_wagon(create_wagon(wagon_capacity))