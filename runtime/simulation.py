import time
from typing import List

from runtime.route_runtime import RouteRuntime
from runtime.simdata.sim_data import SimData
from runtime.station_runtime import StationRuntime
from runtime.passengers_generator import PassengersGenerator
from runtime.event_manager import EventManager
from runtime.statistics_runtime import StatisticsRuntime
from runtime.time_mode_runtime import TimeModeRuntime
from runtime.rush_hour_runtime import RushHourRuntime
from runtime.train_generator import TrainGenerator, TrainGeneratorConfig, TrainsSchedule, ScheduledTrainGenerator
from runtime.simulation_date_time import SimDate

from models.routes.route import Route
from models.trains import Train, TrainConfig
from models.stations import Station
from models.events.train_events import TrainGenerated
from models.events.statistics_event import TrainsStatistics, SaveStatistics
from models.events.simulation_data_event import SimulationDataUpdate



class Simulation:

    def __init__(self, render_interval: float = 0.1, start_time: float = 0):


        # симуляционное время (секунды)
        self.start_time: float = start_time
        self.sim_time: float = start_time

        # интервал обновления вывода (реальные секунды)
        self.render_interval: float = render_interval

        # менеджер событий
        self.event_manager: EventManager = EventManager()

        # runtime-объекты
        self._route_runtimes: List[RouteRuntime] = []
        self._station_runtimes: List[StationRuntime] = []
        self._train_generators: List[TrainGenerator] = []
        self._train_scheduled_generators: List[ScheduledTrainGenerator] = []
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

    # ---------- EventManager  ----------
    def get_event_manager(self) -> EventManager:
        return self.event_manager

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
        unload_min: float = 0.0,
        unload_max: float = 0.3,
    ) -> None:
        self._station_runtimes.append(
            StationRuntime(
                station=station,
                generator=generator,
                event_manager=self.event_manager,
                unload_min=unload_min,
                unload_max=unload_max,
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

    def add_train_scheduled_generator(self, schedule: TrainsSchedule) -> None:
        self._train_scheduled_generators.append(
            ScheduledTrainGenerator(schedule=schedule, event_manager=self.event_manager)
        )

    # ---------- запуск симуляции ----------

    def run(self, sim_seconds_per_real_second: float = 1.0, render: bool = True) -> None:
        last_tick: float = time.perf_counter()
        last_render: float = last_tick
        last_save_stats: float = self.sim_time

        # МАКСИМАЛЬНЫЙ допустимый шаг симуляции
        max_dt_sim: float = 0.5  # не больше 0.5 секунд за раз

        min_dt_real = 0.001

        while True:
            now: float = time.perf_counter()
            dt_real: float = now - last_tick

            if dt_real < min_dt_real:
                time.sleep(min_dt_real - dt_real)
                now = time.perf_counter()
                dt_real = now - last_tick

            last_tick = now

            # Сколько симуляционного времени должно пройти
            target_sim_dt: float = dt_real * sim_seconds_per_real_second

            # Разбиваем на куски не больше max_dt_sim
            remaining_sim_dt = target_sim_dt
            while remaining_sim_dt > 0:
                step_dt = min(max_dt_sim, remaining_sim_dt)

                self.sim_time += step_dt
                remaining_sim_dt -= step_dt

                # --- обновление всех систем с малым шагом ---
                self._time_mode_runtime.advance(self.sim_time)

                for runtime in list(self._route_runtimes):
                    runtime.advance(step_dt)
                    if runtime.finished:
                        self._route_runtimes.remove(runtime)

                for sr in self._station_runtimes:
                    sr.advance(step_dt, self.sim_time)

                for tg in self._train_generators:
                    tg.advance(step_dt)

                for stg in self._train_scheduled_generators:
                    stg.advance(sim_time=self.sim_time)

                if self.sim_time - last_save_stats >= 5 * 60:
                    self.collect_statistics()
                    self.event_manager.emit(SaveStatistics(SimDate(self.sim_time)))
                    last_save_stats = self.sim_time

            # --- вывод ---
            if now - last_render >= self.render_interval:
                if render:
                    self.render()

                sim_data = SimData(sim_time=self.sim_time)
                sim_data.set_rush_status(self._rush_hour_runtime.is_rush)

                for rr in list(self._route_runtimes):
                    sim_data.add_route_data(rr)

                for sr in self._station_runtimes:
                    sim_data.add_station_data(sr)

                self.event_manager.emit(SimulationDataUpdate(sim_data))
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
