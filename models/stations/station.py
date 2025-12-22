from utils import ID
from .dto import StationConfig

class Station:
    def __init__(self, cfg: StationConfig):
        # Идентификатор
        self._id: ID = cfg.id
        # Название
        self._name: str = cfg.name
        # Вместимость станции
        self._cap: int = cfg.capacity
        # Текущая заполненность
        self._person_count: int = 0

    @property
    def id(self) -> ID:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def capacity(self) -> int:
        return self._cap

    @property
    def persons_count(self) -> int:
        return self._person_count

    @property
    def fullness_percentage(self) -> float:
        if self._cap <= 0:
            return 0
        return self._person_count / self._cap * 100

    # Задать вместимость
    def set_capacity(self, capacity: int):
        self._cap = capacity

    # Добавить людей
    def add_person(self, count: int = 1) -> int:
        available = self._cap - self._person_count

        if available < 1:
            return 0

        adding = min(available, count)
        self._person_count += adding

        return adding

    # Уменьшить кол-во людей
    def remove_person(self, count: int = 1) -> int:
        if self._person_count < 1:
            return 0

        removed = min(count, self._person_count)
        self._person_count -= removed

        return removed

    def string(self)->str:
        persons_str = f"{self._person_count}/{self._cap} ({(self._person_count / self._cap * 100):.2f}%)"
        return f"[<#{self._id}> Станция {self._name} {persons_str}]"

    def __repr__(self) -> str:
        return self.string()