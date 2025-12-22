import math
import random


class PassengersGenerator:
    DAY_SECONDS = 24 * 3600

    def __init__(
        self,
        base_rate: float,
        amplitude: float = 0.4,
        rush_multiplier: float = 4.0,
        variation: float = 0.1,
    ):
        self.base_rate = base_rate
        self.amplitude = amplitude
        self.rush_multiplier = rush_multiplier
        self.variation = variation

        self._accumulator = 0.0
        self._rush_factor = 1.0

    # --- реакции на события ---
    def on_rush_started(self, event):
        self._rush_factor = self.rush_multiplier

    def on_rush_ended(self, event):
        self._rush_factor = 1.0

    # --- основная логика ---
    def rate_at_time(self, sim_time: float) -> float:
        day_time = sim_time % self.DAY_SECONDS

        # базовая суточная волна: ночь → min, день → max
        sinus = math.sin(
            2 * math.pi * (day_time - 6 * 3600) / self.DAY_SECONDS
        )

        rate = self.base_rate * (1.0 + self.amplitude * sinus)

        rate *= self._rush_factor

        rate *= 1.0 + random.uniform(-self.variation, self.variation)

        return max(0.0, rate)

    def generate(self, dt: float, sim_time: float) -> int:
        self._accumulator += self.rate_at_time(sim_time) * dt

        count = int(self._accumulator)
        self._accumulator -= count

        return count
