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
            seed: int = None
    ):
        self.base_rate = base_rate
        self.amplitude = amplitude
        self.rush_multiplier = rush_multiplier
        self.variation = variation

        # Используем отдельный генератор для каждой станции
        if seed is None:
            seed = random.randint(0, 2 ** 32 - 1)
        self._random = random.Random(seed)

        self._rush_factor = 1.0  # Убрали _accumulator, т.к. он не нужен для Пуассона

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
        rate *= 1.0 + self._random.uniform(-self.variation, self.variation)

        return max(0.0, rate)

    def generate(self, dt: float, sim_time: float) -> int:
        """
        Генерирует количество пассажиров за интервал dt
        Использует распределение Пуассона
        """
        # Получаем интенсивность (среднее количество пассажиров в секунду)
        rate_per_second = self.rate_at_time(sim_time)

        # Ожидаемое количество пассажиров за интервал dt
        lambda_param = rate_per_second * dt

        # Для очень маленьких lambda (редкие события)
        if lambda_param < 1e-10:
            return 0

        # Генерация по распределению Пуассона
        return self._poisson(lambda_param)

    def _poisson(self, lambda_param: float) -> int:
        """
        Генерация случайной величины по распределению Пуассона
        Алгоритм Кнута для малых lambda, аппроксимация для больших
        """
        if lambda_param < 30:
            # Алгоритм Кнута для малых lambda
            L = math.exp(-lambda_param)
            k = 0
            p = 1.0

            while True:
                k += 1
                p *= self._random.random()
                if p <= L:
                    break

            return k - 1
        else:
            # Аппроксимация нормальным распределением для больших lambda
            # Более эффективно для больших значений
            mean = lambda_param
            std = math.sqrt(lambda_param)

            # Генерируем нормально распределенное значение
            value = self._random.gauss(mean, std)

            # Пуассон не может быть отрицательным
            value = max(0.0, value)

            # Округляем до целого (для Пуассона это дискретное распределение)
            return int(round(value))

    # Альтернативная, более простая реализация Пуассона
    def _poisson_simple(self, lambda_param: float) -> int:
        """
        Более простая реализация через сумму экспоненциальных распределений
        Хорошо работает для любых lambda
        """
        if lambda_param <= 0:
            return 0

        L = math.exp(-lambda_param)
        k = 0
        p = 1.0

        while p > L:
            k += 1
            p *= self._random.random()

        return k - 1