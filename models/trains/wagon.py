from utils import ID

class Wagon:


    # Constructor
    def __init__(self, capacity: int = 0):
        # Идентифкатор
        self._id: ID = ID()
        # Вместимость
        self._cap: int = capacity
        # Текущая заполненость
        self._person_count: int = 0

    # Получить идентификатор вгона
    @property
    def id(self) -> ID:
        return self._id

    # Получить вместимость вагона
    @property
    def cap(self) -> int:
        return self._cap

    # Получить кол-во людей в вагоне
    @property
    def person_count(self) -> int:
        return self._person_count

    def set_capacity(self, c: int) -> None:
        self._cap = c

    # Впустить людей в вагон
    def add_person(self, count:int = 1) -> int:
        available = self._cap - self._person_count

        # Если вагон больше не может вместить людей
        if available < 1:
            return 0

        # Добавляемое кол-во людей
        adding = min(available, count)

        self._person_count += 1

        return adding

    # Выпустить людей из вагона
    def remove_person(self, count:int = 1) -> int:
        # Если в вагоне не осталось людей
        if self._person_count < 1:
            return 0

        # Убавляемое кол-во людей
        removing = min(count, self._person_count)

        self._person_count -= removing

        return removing

    # ASCII визуализация
    def string(self) -> str:
        return f"[Вагон №{self._id} ({self._person_count}/{self._cap})]"