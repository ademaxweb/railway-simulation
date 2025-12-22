import random
from typing import Dict
import math
from models.trains import Train
from models.stations import Station
from models.events.time_events import RushHourStarted, RushHourEnded
from models.events.train_events import (
    TrainArrivedAtStation,
    TrainDepartedFromStation,
    TrainFinishedUnloading,
    TrainFinishedStationWait
)
from runtime.event_manager import EventManager
from runtime.passengers_generator import PassengersGenerator


class StationRuntime:
    # -------- параметры модели --------
    DOORS_PER_WAGON: int = 2
    PERSONS_PER_DOOR_PER_SEC: float = 1.2

    BOARDING_VARIATION: float = 0.25

    UNLOAD_PERCENT_MIN: float = 0.02
    UNLOAD_PERCENT_MAX: float = 0.2

    # -------- инициализация --------

    def __init__(self, station: Station, generator: PassengersGenerator, event_manager: EventManager):
        self.station = station
        self.generator = generator
        self.event_manager = event_manager

        # train -> accumulator
        self._unloading_trains: Dict[Train, float] = {}
        self._boarding_trains: Dict[Train, float] = {}

        # сколько ещё нужно высадить
        self._unload_targets: Dict[Train, int] = {}

        # -------- подписки --------
        event_manager.subscribe(RushHourStarted, generator.on_rush_started)
        event_manager.subscribe(RushHourEnded, generator.on_rush_ended)

        event_manager.subscribe(TrainArrivedAtStation, self._on_train_arrived)
        event_manager.subscribe(TrainFinishedUnloading, self._on_train_finished_unloading)
        event_manager.subscribe(TrainDepartedFromStation, self._on_train_departed)

        event_manager.subscribe(TrainFinishedStationWait, self._on_train_finished_station_wait)

    # -------- события --------

    def _on_train_arrived(self, event: TrainArrivedAtStation) -> None:
        if event.station is not self.station:
            return

        train = event.train

        percent = random.uniform(
            self.UNLOAD_PERCENT_MIN,
            self.UNLOAD_PERCENT_MAX,
        )

        to_unload = int(train.person_count * percent)

        if to_unload > 0:
            self._unloading_trains[train] = 0.0
            self._unload_targets[train] = to_unload
        else:
            self.event_manager.emit(TrainFinishedUnloading(event.train, event.station))

    def _on_train_finished_unloading(self, event: TrainFinishedUnloading) -> None:
        if event.station is not self.station:
            return

        self._boarding_trains[event.train] = 0.0

    def _on_train_departed(self, event: TrainDepartedFromStation) -> None:
        if event.station is not self.station:
            return

        train = event.train

        self._unloading_trains.pop(train, None)
        self._boarding_trains.pop(train, None)
        self._unload_targets.pop(train, None)

    def _on_train_finished_station_wait(self, event: TrainFinishedStationWait) -> None:
        train = event.train
        self._unloading_trains.pop(train, None)
        self._boarding_trains.pop(train, None)
        self._unload_targets.pop(train, None)
    # -------- симуляция --------

    def advance(self, dt: float, sim_time: float) -> None:
        # генерация пассажиров на станции
        generated = self.generator.generate(dt, sim_time)

        if generated > 0:
            if self.station.fullness_percentage > 80:
                factor = random.uniform(0, 1)
            else: factor = 1

            if factor > 0.85:
                self.station.add_person(generated)

        self._process_unloading(dt)

        self._process_boarding(dt)

    # -------- высадка --------

    def _process_unloading(self, dt: float) -> None:
        for train in list(self._unloading_trains.keys()):
            wagon_count = train.wagons_count
            if wagon_count == 0:
                continue

            rate = (
                wagon_count
                * self.DOORS_PER_WAGON
                * self.PERSONS_PER_DOOR_PER_SEC
            )

            self._unloading_trains[train] += rate * dt

            to_unload = int(self._unloading_trains[train])
            remaining = self._unload_targets[train]

            actual = min(to_unload, remaining)
            if actual <= 0:
                continue

            unloaded = train.remove_person(actual)
            # self.station.add_person(unloaded)

            self._unloading_trains[train] -= unloaded
            self._unload_targets[train] -= unloaded

            if self._unload_targets[train] <= 0:
                # высадка завершена
                self._unloading_trains.pop(train)
                self._unload_targets.pop(train)

                self.event_manager.emit(
                    TrainFinishedUnloading(train, self.station)
                )

    # -------- посадка --------

    def _process_boarding(self, dt: float) -> None:
        for train in list(self._boarding_trains.keys()):
            wagon_count = train.wagons_count
            if wagon_count == 0:
                continue

            base_rate = (
                wagon_count
                * self.DOORS_PER_WAGON
                * self.PERSONS_PER_DOOR_PER_SEC
            )

            noise = random.uniform(
                1.0 - self.BOARDING_VARIATION,
                1.0 + self.BOARDING_VARIATION,
            )

            rate = base_rate * noise
            self._boarding_trains[train] += rate * dt

            to_board = int(self._boarding_trains[train])
            if to_board <= 0:
                continue

            available = min(to_board, self.station.persons_count)
            if available <= 0:
                continue

            boarded = train.add_person(available)
            self.station.remove_person(boarded)

            self._boarding_trains[train] -= boarded

    # -------- вывод --------

    def __str__(self) -> str:
        return (
            f"{self.station.name}: "
            f"{self.station.persons_count}/{self.station.capacity}"
        )
