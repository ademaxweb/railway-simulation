from functools import reduce
from typing import List
from .train_type import TrainType
from .dto import TrainConfig
from .wagon import Wagon

from utils import ID

class Train:

    # Constructor
    def __init__(self, cfg: TrainConfig):
        # Идентификатор
        self._id: ID = ID()
        # Параметры поезда
        self._config: TrainConfig = cfg
        # Текущая скорость
        self._speed: float = 0.0
        # Список вагонов
        self._wagons: List[Wagon] = []

        for _ in range(cfg.wagon_count):
            self.add_wagon(Wagon(capacity=cfg.wagon_capacity))

    @property
    def id(self) -> ID:
        return self._id

    @property
    def max_speed(self) -> float:
        return self._config.max_speed

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def train_type(self) -> TrainType:
        return self._config.type

    @property
    def model_name(self) -> str:
        return self._config.model_name

    @property
    def wagons_count(self) -> int:
        return len(self._wagons)

    @property
    def capacity(self) -> int:
        return reduce(lambda cap, w: cap + w.cap, self._wagons, 0)

    @property
    def person_count(self) -> int:
        return reduce(lambda count, w: count + w.person_count, self._wagons, 0)

    @property
    def filling_percentage(self) -> float:
        if self.capacity == 0:
            return 0
        return self.person_count / self.capacity * 100

    def add_wagon(self, wagon: Wagon):
        self._wagons.append(wagon)


    def set_wagon_capacity(self, capacity: int):
        for w in self._wagons:
            w.set_capacity(capacity)

    def set_speed(self, speed: float):
        self._speed = speed

    def add_person(self, count: int = 1) -> int:
        if count <= 0 or not self._wagons:
            return 0

        remaining = count

        for w in self._wagons:
            remaining -= w.add_person(remaining)
            if remaining <= 0:
                break

        return count - remaining

    def remove_person(self, count: int = 1) -> int:
        if count <= 0 or not self._wagons:
            return 0

        remaining = count

        for w in self._wagons:
            removed = w.remove_person(remaining)
            remaining -= removed

            if remaining <= 0:
                break

        return count - remaining

    def string_short(self)->str:
        persons_str = f"{self.person_count}/{self.capacity}({round(self.filling_percentage)}%)"
        speed_str = f"{round(self.speed, 2)}/{round(self.max_speed, 2)} км/ч"
        name_str = f"{self._config.type} поезд {self._config.model_name} №{self._id}"

        return f"<{name_str}  {persons_str}  {speed_str}]"

    def string(self, only_train:bool = False) -> str:
        wagons_str = '=='.join(map(lambda w: w.string(), self._wagons))
        persons_str = f"{self.person_count}/{self.capacity}({round(self.filling_percentage)}%)"
        speed_str = f"{round(self.speed, 2)}/{round(self.max_speed, 2)} км/ч"
        name_str = f"{self._config.type} поезд {self._config.model_name} №{self._id}"


        return f'<{name_str}  {persons_str}  {speed_str}]{"" if only_train else "==="+wagons_str}'

    def __repr__(self) -> str:
        return self.string()

    def __str__(self) -> str:
        return self.string_short()