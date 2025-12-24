import time
from typing import List

from runtime.route_runtime import RouteRuntime
from runtime.station_runtime import StationRuntime
from runtime.passengers_generator import PassengersGenerator
from runtime.event_manager import EventManager
from runtime.statistics_runtime import StatisticsRuntime
from runtime.time_mode_runtime import TimeModeRuntime
from runtime.rush_hour_runtime import RushHourRuntime
from runtime.train_generator import TrainGenerator, TrainGeneratorConfig
from runtime.simulation_date_time import SimDate

from models.routes.route import Route
from models.trains import Train, TrainConfig
from models.stations import Station
from models.events.train_events import TrainGenerated
from models.events.statistics_event import TrainsStatistics, SaveStatistics



class Simulation:

    def __init__(self, render_interval: float = 0.1, start_time: float = 0):
        # статистика

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
        self._statistics_runtime = StatisticsRuntime(self.event_manager)


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
        last_save_stats: float = self.sim_time

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
            if self.sim_time - last_save_stats >= 2 * 60:
                self.collect_statistics()
                self.event_manager.emit(SaveStatistics(SimDate(self.sim_time)))
                last_save_stats = self.sim_time

            # --- вывод ---
            if render:
                if now - last_render >= self.render_interval:
                    self.render()
                    last_render = now




    # ---------- статистика -------------------
    def collect_statistics(self):
        self.event_manager.emit(
            TrainsStatistics(
                list(map(lambda rr: rr.train, self._route_runtimes))
            )
        )

    # ---------- обработчики событий ----------

    def _on_train_generated(self, event: TrainGenerated) -> None:
        self.add_route(event.route, event.train)

    # ---------- вывод ---------

    def render(self) -> None:
        lines: List[str] = [
            f"T={self.sim_time:7.1f}s ({SimDate(self.sim_time)})"
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
