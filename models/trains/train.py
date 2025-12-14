from functools import reduce

from .wagon import Wagon
from .train_type import TrainType

from utils import ID

class Train:
    # Идентификатор
    _id: ID
    # Тип поезда
    _train_type: TrainType = TrainType.UNKNOWN
    # Название
    _model_name: str = ""
    # Максимальная скорость
    _max_speed: float = 0.0
    # Скорость
    _speed: float = 0.0
    # Список вагонов
    _wagons: list[Wagon] = list()

    # Constructor
    def __init__(
            self,
            t: TrainType = TrainType.UNKNOWN,
            max_speed: float = 80.0,
            model_name: str = "",
            wagon_capacity: int = 0,
            wagon_count: int = 0
    ):
        self._id = ID()
        self._train_type = t
        self._max_speed = max_speed
        self._model_name = model_name

        for _ in range(wagon_count):
            self.add_wagon(Wagon(capacity=wagon_capacity))

    @property
    def id(self) -> ID:
        return self._id

    @property
    def max_speed(self) -> float:
        return self._max_speed

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def train_type(self) -> TrainType:
        return self._train_type

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def capacity(self) -> int:
        return reduce(lambda cap, w: cap + w.cap, self._wagons, 0)

    @property
    def person_count(self) -> int:
        return reduce(lambda count, w: count + w.person_count, self._wagons, 0)

    def add_wagon(self, wagon: Wagon):
        self._wagons.append(wagon)

    def string(self) -> str:
        wagons_str = '=='.join(map(lambda w: w.string(), self._wagons))

        return f'<{self._train_type} Поезд №{self._id} {self.person_count}/{self.capacity} ({round(self.person_count / self.capacity, 1)})]=={wagons_str}'