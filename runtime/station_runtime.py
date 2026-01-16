import random
from typing import Dict
from dataclasses import dataclass
from models.trains import Train
from models.stations import Station
from models.events.time_events import RushHourStarted, RushHourEnded, NewDayMarker
from models.events.train_events import (
    TrainArrivedAtStation,
    TrainDepartedFromStation,
    TrainFinishedUnloading,
    TrainFinishedStationWait
)
from runtime.event_manager import EventManager
from runtime.passengers_generator import PassengersGenerator
from utils import ID

@dataclass
class TrainOnStation:
    is_waiting_finished = False
    is_boarding_finished = False
    is_unloading_finished = False

    total_delay: float = 0

    @property
    def is_finished(self) -> bool:
        return (
            self.is_waiting_finished and
            self.is_boarding_finished and
            self.is_unloading_finished
        )

    def finish_waiting(self):
        self.is_waiting_finished = True

    def finish_boarding(self):
        self.is_boarding_finished = True

    def finish_unloading(self):
        self.is_unloading_finished = True

    def add_delay(self, v: float):
        self.total_delay += v

    def to_dict(self) -> dict:
        return {
            "is_waiting_finished": self.is_waiting_finished,
            "is_boarding_finished": self.is_boarding_finished,
            "is_unloading_finished": self.is_unloading_finished,
            "is_finished": self.is_finished,
            "total_delay": round(self.total_delay, 2)
        }



class StationRuntime:
    # -------- параметры модели --------
    DOORS_PER_WAGON: int = 2
    PERSONS_PER_DOOR_PER_SEC: float = 0.6

    BOARDING_VARIATION: float = 0.25



    # -------- инициализация --------

    def __init__(self, station: Station, generator: PassengersGenerator, event_manager: EventManager, unload_min: float = 0.0, unload_max: float = 0.3):
        self.station = station
        self.generator = generator
        self.event_manager = event_manager

        # train -> accumulator
        self._unloading_trains: Dict[Train, float] = {}
        self._boarding_trains: Dict[Train, float] = {}

        self._unload_min: float = unload_min
        self._unload_max: float = unload_max

        # сколько ещё нужно высадить
        self._unload_targets: Dict[Train, int] = {}

        self._trains: Dict[Train, TrainOnStation] = {}

        self.total_boarded = 0

        # -------- подписки --------
        event_manager.subscribe(RushHourStarted, generator.on_rush_started)
        event_manager.subscribe(RushHourEnded, generator.on_rush_ended)

        event_manager.subscribe(TrainArrivedAtStation, self._on_train_arrived)
        event_manager.subscribe(TrainFinishedUnloading, self._on_train_finished_unloading)
        event_manager.subscribe(TrainDepartedFromStation, self._on_train_departed)

        event_manager.subscribe(TrainFinishedStationWait, self._on_train_finished_station_wait)

    def get_train_on_station(self, train: Train) -> TrainOnStation | None:
        return self._trains.get(train)

    def get_trains(self) -> Dict[Train, TrainOnStation]:
        return self._trains
    # -------- события --------

    def _on_train_arrived(self, event: TrainArrivedAtStation) -> None:
        if event.station is not self.station:
            return

        train = event.train


        percent = random.uniform(
            self._unload_min,
            self._unload_max,
        )

            # print(f"{self.station.name} {percent}")

        to_unload = int(train.person_count * percent)

        self._trains[train] = TrainOnStation()
        self._unloading_trains[train] = 0.0
        self._unload_targets[train] = to_unload

        if to_unload <= 0:
            self.event_manager.emit(TrainFinishedUnloading(event.train, event.station))

    def _on_train_finished_unloading(self, event: TrainFinishedUnloading) -> None:
        if event.station is not self.station:
            return

        train = event.train

        # высадка завершена
        self._unloading_trains.pop(train)
        self._unload_targets.pop(train)
        self._trains[train].finish_unloading()

        # начало посадки
        self._boarding_trains[event.train] = 0.0

    def _on_train_departed(self, event: TrainDepartedFromStation) -> None:
        if event.station is not self.station:
            return

        train = event.train

        self._unloading_trains.pop(train, None)
        self._boarding_trains.pop(train, None)
        self._unload_targets.pop(train, None)
        self._trains.pop(train, None)

    def _on_train_finished_station_wait(self, event: TrainFinishedStationWait) -> None:
        if event.station is not self.station:
            return

        train = event.train

        self._trains[train].finish_waiting()
    # -------- симуляция --------

    def advance(self, dt: float, sim_time: float) -> None:
        """ генерация пассажиров на станции """

        self._process_trains(dt)

        generated = self.generator.generate(dt, sim_time)

        if generated > 0:
            if self.station.persons_count > 220:
                factor = random.uniform(0, 1)
            else: factor = 1

            if factor > 0.85:
                self.station.add_person(generated)



    # -------- поезда на станции --------
    def _process_trains(self, dt:float) -> None:
        self._process_unloading(dt)
        self._process_boarding(dt)

        for train in list(self._trains.keys()):
            if self._trains[train].is_finished:
                self.event_manager.emit(TrainDepartedFromStation(train, self.station))

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

            if self._trains[train].is_waiting_finished:
                self._trains[train].add_delay(dt)

            if self._unload_targets[train] <= 0:
                self.event_manager.emit(
                    TrainFinishedUnloading(train, self.station)
                )

    # -------- посадка --------

    def _process_boarding(self, dt: float) -> None:
        for train in list(self._boarding_trains.keys()):
            wagon_count = train.wagons_count
            if wagon_count == 0:
                continue

            if self.station.persons_count == 0 or train.person_count >= train.capacity:
                self._trains[train].finish_boarding()

            if self._trains[train].is_waiting_finished:
                self._trains[train].add_delay(dt)

            base_rate = (
                wagon_count
                * self.DOORS_PER_WAGON
                * self.PERSONS_PER_DOOR_PER_SEC
            )

            noise = random.uniform(
                1.0 - self.BOARDING_VARIATION,
                1.0,
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

            self.total_boarded += boarded

            self.station.remove_person(boarded)


            self._boarding_trains[train] -= boarded

    # -------- вывод --------

    def __str__(self) -> str:
        return (
            f"{self.station.name}: "
            f"{self.station.persons_count}/{self.station.capacity}"
        )
