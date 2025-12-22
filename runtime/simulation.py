import time
from typing import List

from runtime.route_runtime import RouteRuntime
from runtime.station_runtime import StationRuntime
from runtime.passengers_generator import PassengersGenerator
from runtime.event_manager import EventManager
from runtime.time_mode_runtime import TimeModeRuntime
from runtime.rush_hour_runtime import RushHourRuntime
from runtime.train_generator import TrainGenerator, TrainGeneratorConfig


from models.routes.route import Route
from models.trains import Train, TrainConfig
from models.stations import Station
from models.events.train_events import TrainGenerated

from dataclasses import dataclass

@dataclass(frozen=False)
class SimulationStats:
    persons_in_trains: int = 0
    persons_in_trains_percents: float = 0
    trains_count: int = 0


    @property
    def avg_persons_in_trains(self) -> float:
        if self.trains_count <= 0:
            return 0
        return self.persons_in_trains / self.trains_count

    @property
    def avg_persons_in_trains_percents(self) -> float:
        if self.trains_count <= 0:
            return 0
        return self.persons_in_trains_percents / self.trains_count

    def clear(self):
        self.persons_in_trains = 0
        self.trains_count = 0
        self.persons_in_trains_percents = 0


class Simulation:

    def __init__(self, render_interval: float = 0.1, start_time: float = 0):
        # статистика
        self.statistics = SimulationStats()

        # симуляционное время (секунды)
        self.sim_time: float = start_time

        # интервал обновления вывода (реальные секунды)
        self.render_interval: float = render_interval

        # менеджер событий
        self.event_manager: EventManager = EventManager()

        # runtime-объекты
        self._route_runtimes: List[RouteRuntime] = []
        self._station_runtimes: List[StationRuntime] = []
        self._train_generators: List[TrainGenerator] = []

        # runtime временных режимов (час-пик, временные маркеры)
        self._time_mode_runtime: TimeModeRuntime = TimeModeRuntime(
            event_manager=self.event_manager,
            info_interval=60 * 60
        )

        self._rush_hour_runtime = RushHourRuntime(
            self.event_manager,
            intervals=[
                (7 * 3600, 10 * 3600)
            ]
        )

        self.event_manager.subscribe(TrainGenerated, self._on_train_generated)

    # ---------- конфигурация ----------

    def add_route(self, route: Route, train: Train) -> None:
        self._route_runtimes.append(
            RouteRuntime(
                route=route,
                train=train,
                event_manager=self.event_manager,
            )
        )

    def add_station(
        self,
        station: Station,
        generator: PassengersGenerator,
    ) -> None:
        self._station_runtimes.append(
            StationRuntime(
                station=station,
                generator=generator,
                event_manager=self.event_manager,
            )
        )

    def add_train_generator(self, route: Route, train_configs: List[TrainConfig], interval: int = 60) -> None:
        self._train_generators.append(
            TrainGenerator(TrainGeneratorConfig(
                route=route,
                train_configs=train_configs,
                interval=interval,
                event_manager=self.event_manager,
            ))
        )

    # ---------- запуск симуляции ----------

    def run(self, sim_seconds_per_real_second: float = 1.0, render: bool = True) -> None:
        last_tick: float = time.time()
        last_render: float = last_tick

        while True:
            now: float = time.time()

            # реальное прошедшее время
            dt_real: float = now - last_tick
            last_tick = now

            # симуляционное время
            dt_sim: float = dt_real * sim_seconds_per_real_second
            self.sim_time += dt_sim

            # --- интерпретация времени (час-пик, маркеры) ---
            self._time_mode_runtime.advance(self.sim_time)

            # --- обновление маршрутов ---
            for runtime in list(self._route_runtimes):
                runtime.advance(dt_sim)
                if runtime.finished:
                    self._route_runtimes.remove(runtime)

            # --- обновление станций ---
            for sr in self._station_runtimes:
                sr.advance(dt_sim, self.sim_time)

            # --- генерация поездов ---
            for tg in self._train_generators:
                tg.advance(dt_sim)

            # --- сбор статистики ----
            self.collect_statistics()

            # --- вывод ---
            if render:
                if now - last_render >= self.render_interval:
                    self.render()
                    last_render = now

    # ---------- статистика -------------------
    def collect_statistics(self):
        self.statistics.clear()

        for runtime in self._route_runtimes:
            self.statistics.trains_count += 1
            self.statistics.persons_in_trains += runtime.train.person_count
            self.statistics.persons_in_trains_percents += runtime.train.filling_percentage


    # ---------- обработчики событий ----------

    def _on_train_generated(self, event: TrainGenerated) -> None:
        self.add_route(event.route, event.train)

    # ---------- вывод ---------

    def get_time(self):
        total = int(self.sim_time)
        h = total // 3600
        m = (total % 3600) // 60
        s = total % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def render(self) -> None:
        lines: List[str] = [
            f"T={self.sim_time:7.1f}s ({self.get_time()})",
            f"Total persons in trains: {self.statistics.persons_in_trains}",
            f"Avg persons in trains: {self.statistics.avg_persons_in_trains:.2f}",
            f"Avg fullness percentage: {self.statistics.avg_persons_in_trains_percents:.2f}%",
        ]

        # поезда
        for runtime in self._route_runtimes:
            lines.append(
                f"  {runtime.train} | {runtime}"
            )

        # станции
        for sr in self._station_runtimes:
            lines.append(
                f"  [STATION] {sr}"
            )

        print(
            "\033[H\033[J" + "\n".join(lines),
            end="\n",
            flush=True,
        )
