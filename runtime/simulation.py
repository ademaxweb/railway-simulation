import time
from runtime.event_manager import EventManager
from runtime.route_runtime import RouteRuntime


class Simulation:
    def __init__(self, render_interval=0.1):
        self.sim_time = 0.0
        self.render_interval = render_interval
        self.event_manager = EventManager()
        self._runtimes = []

    def add_route(self, route, train):
        self._runtimes.append(
            RouteRuntime(route, train, self.event_manager)
        )

    def run(self, sim_seconds_per_real_second: float = 1.0) -> None:
        last_tick = time.time()
        last_render = last_tick

        while self._runtimes:
            now = time.time()

            dt_real = now - last_tick
            last_tick = now

            dt_sim = dt_real * sim_seconds_per_real_second
            self.sim_time += dt_sim

            for runtime in list(self._runtimes):
                runtime.advance(dt_sim)
                if runtime.finished:
                    self._runtimes.remove(runtime)

            if now - last_render >= self.render_interval:
                self.render()
                last_render = now

    def render(self) -> None:
        if not self._runtimes:
            return

        lines = [f"T={self.sim_time:7.1f}s"]

        for runtime in self._runtimes:
            lines.append(
                f"  {runtime.train.string_short()} {runtime}"
            )

        output = "\n".join(lines)

        print(
            "\033[H\033[J" + output, end="\n"
        )

