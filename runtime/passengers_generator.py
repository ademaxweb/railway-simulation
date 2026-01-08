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
    # def rate_at_time(self, sim_time: float) -> float:
    #     day_time = sim_time % self.DAY_SECONDS
    #
    #     # базовая суточная волна: ночь → min, день → max
    #     sinus = math.sin(
    #         2 * math.pi * (day_time - 6 * 3600) / self.DAY_SECONDS
    #     )
    #
    #     rate = self.base_rate * (1.0 + self.amplitude * sinus)
    #     rate *= self._rush_factor
    #     rate *= 1.0 + self._random.uniform(-self.variation, self.variation)
    #
    #     return max(0.0, rate)

    def rate_at_time(self, sim_time: float) -> float:
        day_time = sim_time % self.DAY_SECONDS
        hour = day_time / 3600
        minute = (day_time % 3600) / 60

        hour_norm = hour if hour >= 2 else hour + 24

        # Коэффициенты для разных периодов (на основе статистики метро)
        if 2.0 <= hour_norm < 4.0:  # Ночь: 2:00-4:00
            coefficient = 0.005 + 0.01 * ((hour_norm - 2.0) / 2.0)  # 5% → 15%

        elif 4.0 <= hour_norm < 6.0:  # Раннее утро: 4:00-6:00
            t = (hour_norm - 4.0) / 2.0
            coefficient = 0.15 + 0.30 * t  # 15% → 45%

        elif 6.0 <= hour_norm < 8.5:  # Утренний пик: 6:00-8:30
            if hour_norm < 7.5:  # До 7:30 - быстрый рост
                t = (hour_norm - 6.0) / 1.5
                coefficient = 0.45 + 0.45 * math.sin(t * math.pi / 2)  # 45% → 90%
            else:  # 7:30-8:30 - вершина пика
                t = (hour_norm - 7.5) / 1.0
                coefficient = 0.90 + 0.10 * (1 - math.cos(t * math.pi)) / 2  # 90% → 100% → 90%

        elif 8.5 <= hour_norm < 10.0:  # После пика: 8:30-10:00
            t = (hour_norm - 8.5) / 1.5
            coefficient = 0.90 - 0.25 * t  # 90% → 65%

        elif 10.0 <= hour_norm < 17.0:  # День: 10:00-17:00
            t = (hour_norm - 10.0) / 7.0
            coefficient = 0.65 - 0.15 * t  # 65% → 50%

        elif 17.0 <= hour_norm < 20.0:  # Вечерний подъем: 17:00-20:00
            if hour_norm < 18.5:  # Рост до 18:30
                t = (hour_norm - 17.0) / 1.5
                coefficient = 0.50 + 0.25 * math.sin(t * math.pi / 2)  # 50% → 75%
            else:  # 18:30-20:00
                t = (hour_norm - 18.5) / 1.5
                coefficient = 0.75 - 0.20 * t  # 75% → 55%

        elif 20.0 <= hour_norm < 24.0:  # Вечер: 20:00-0:00
            t = (hour_norm - 20.0) / 4.0
            coefficient = 0.55 - 0.40 * t  # 55% → 15%

        elif 24.0 <= hour_norm <= 26.0:  # Ночь: 0:00-2:00
            t = (hour_norm - 24.0) / 2.0
            coefficient = 0.15 - 0.10 * t  # 15% → 5%

        else:
            coefficient = 0.05

        rate = self.base_rate * coefficient
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