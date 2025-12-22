import time
from typing import List

from runtime.route_runtime import RouteRuntime
from runtime.station_runtime import StationRuntime
from runtime.passengers_generator import PassengersGenerator
from runtime.event_manager import EventManager
from runtime.time_mode_runtime import TimeModeRuntime
from runtime.rush_hour_runtime import RushHourRuntime


from models.routes.route import Route
from models.trains import Train
from models.stations import Station


class Simulation:
    def __init__(self, render_interval: float = 0.1):
        # симуляционное время (секунды)
        self.sim_time: float = 0.0

        # интервал обновления вывода (реальные секунды)
        self.render_interval: float = render_interval

        # менеджер событий
        self.event_manager: EventManager = EventManager()

        # runtime-объекты
        self._route_runtimes: List[RouteRuntime] = []
        self._station_runtimes: List[StationRuntime] = []

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

    # ---------- запуск симуляции ----------

    def run(self, sim_seconds_per_real_second: float = 1.0) -> None:
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

            # --- вывод ---
            if now - last_render >= self.render_interval:
                #self.render()
                last_render = now

    # ---------- обработчики событий ----------

    # ---------- вывод ----------

    def render(self) -> None:
        lines: List[str] = [
            f"T={self.sim_time:7.1f}s"
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
            end="",
            flush=True,
        )
