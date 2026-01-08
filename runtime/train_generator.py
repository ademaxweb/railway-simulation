from models.routes.route import Route
from models.trains import Train, create_train
from models.trains.dto import TrainConfig
from dataclasses import dataclass
from typing import List, Dict
import random
from models.events.train_events import TrainGenerated
from runtime.event_manager import EventManager
from models.events.time_events import NewDayMarker



@dataclass(frozen=True)
class ScheduleTime:
    """Время в расписании"""
    hour: int
    minute: int
    second: int = 0

    def to_seconds(self) -> int:
        """Конвертирует в секунды от начала дня (0-86399)"""
        return self.hour * 3600 + self.minute * 60 + self.second

    def __str__(self) -> str:
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"

    @classmethod
    def from_seconds(cls, seconds: int) -> 'ScheduleTime':
        """Создает из секунд от начала дня"""
        seconds = seconds % (24 * 3600)  # Обеспечиваем 0-86399
        return cls(
            hour=seconds // 3600,
            minute=(seconds % 3600) // 60,
            second=seconds % 60
        )


@dataclass
class TrainScheduleEntry:
    """Запись в расписании: какой поезд, по какому маршруту и когда отправляется"""
    route: Route
    train_config: TrainConfig
    departure_time: ScheduleTime  # Время отправления с первой станции
    is_departed: bool = False

class TrainsSchedule:
    """Полное расписание на день"""
    def __init__(self, schedule: List[TrainScheduleEntry]):
        self.all_entries: List[TrainScheduleEntry] = schedule

        self._schedule: Dict[ScheduleTime, List[TrainScheduleEntry]] = {}

        for s in schedule:
            if not s.departure_time in self._schedule:
                self._schedule[s.departure_time] = []

            self._schedule[s.departure_time].append(s)

    def get_entries_at_seconds(self, seconds: float | int) -> List[TrainScheduleEntry]:
        return self.get_entries_at_time(ScheduleTime.from_seconds(int(seconds)))

    def get_entries_at_time(self, time: ScheduleTime) -> List[TrainScheduleEntry]:
        if not time in self._schedule:
            return []
        return self._schedule[time]

    def reset_departs(self):
        for e in self.all_entries:
            e.is_departed = False


class ScheduledTrainGenerator:
    def __init__(self, schedule: TrainsSchedule, event_manager: EventManager):
        self._schedule = schedule
        self._event_manager = event_manager
        self._last_processed_second = -1

        self._event_manager.subscribe(NewDayMarker, self._on_new_day)

    def advance(self, sim_time: float) -> None:
        """
        Проверяет, нужно ли отправить поезда в текущую секунду.
        Вызывается на каждом шаге симуляции.
        """
        current_second = int(sim_time)
        day_second = current_second % (60 * 60 * 24)

        # Проверяем только если это новая секунда
        if day_second == self._last_processed_second:
            return

        self._last_processed_second = day_second

        entries = self._schedule.get_entries_at_seconds(day_second)

        for entry in entries:
            if not entry.is_departed:
                self._dispatch_train(entry)
                entry.is_departed = True

    def _dispatch_train(self, entry: TrainScheduleEntry) -> None:
        """Отправляет поезд по расписанию"""
        train = create_train(entry.train_config)
        self._event_manager.emit(TrainGenerated(train, entry.route))

    def _on_new_day(self, e: NewDayMarker):
        self._schedule.reset_departs()
        self._last_processed_second = -1



@dataclass(frozen=True)
class TrainGeneratorConfig:
    route: Route
    train_configs: List[TrainConfig]
    interval: int
    event_manager: EventManager

class TrainGenerator:
    def __init__(self, cfg: TrainGeneratorConfig):
        self.route = cfg.route
        self.configs = cfg.train_configs
        self.interval = cfg.interval
        self.event_manager = cfg.event_manager

        self._elapsed: float = 0.0

    def advance(self, dt: float) -> None:
        self._elapsed += dt

        while self._elapsed >= self.interval:
            self._elapsed -= self.interval

            train: Train = create_train(random.choice(self.configs))

            self.event_manager.emit(TrainGenerated(train, self.route))