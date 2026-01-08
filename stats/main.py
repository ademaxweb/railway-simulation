import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

JSON_PATH = Path("stats/trains.json")
OUTPUT_DIR = Path("stats/plots")
METRIC_KEYS = ['trains_count', 'total_persons', 'avg_persons_in_train', 'avg_fullness_percentage', 'avg_speed',
               'max_speed', 'max_fullness_percentage', 'max_persons', 'min_speed', 'min_fullness_percentage',
               'min_persons']


def load_metrics(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_time_label(t: dict) -> str:
    return f'{t["h"]:02d}:{t["m"]:02d}'  # Убрали секунды для краткости


def plot_metric(data: list, metric_key: str):
    times = []
    values = []

    # Собираем данные
    for item in data:
        times.append(build_time_label(item["time"]))
        values.append(item["data"]["trains"][metric_key])

    OUTPUT_DIR.mkdir(exist_ok=True)

    plt.figure(figsize=(12, 6))

    # Построение графика
    plt.plot(times, values, marker="o", markersize=3, linewidth=1)
    plt.xlabel("Time")
    plt.ylabel(metric_key)
    plt.title(f"{metric_key} over time")
    plt.grid(True, alpha=0.3)

    # Настройка меток времени
    n_points = len(times)

    # Вариант 1: Каждые N записей (например, каждые 15 минут если записи каждые 2 минуты)
    interval = max(1, n_points // 24)  # Показываем примерно 24 метки
    if interval < 10:
        interval = max(1, n_points // 12)  # Если мало точек, покажем 12 меток

    # Показываем только некоторые метки
    show_indices = list(range(0, n_points, interval))

    # Убедимся что последняя точка тоже показана
    if n_points - 1 not in show_indices:
        show_indices.append(n_points - 1)

    # Создаем метки
    x_labels = []
    for i in range(n_points):
        if i in show_indices:
            x_labels.append(times[i])
        else:
            x_labels.append('')

    plt.xticks(range(n_points), x_labels, rotation=45, ha='right')

    # Вариант 2: Показывать только каждый час
    # hourly_indices = []
    # for i, time_str in enumerate(times):
    #     # Проверяем, заканчивается ли время на :00 (каждый час)
    #     if time_str.endswith(':00'):
    #         hourly_indices.append(i)
    #
    # # Создаем метки только для часовых отметок
    # x_labels = []
    # for i in range(n_points):
    #     if i in hourly_indices:
    #         x_labels.append(times[i])
    #     else:
    #         x_labels.append('')
    #
    # plt.xticks(range(n_points), x_labels, rotation=45, ha='right')

    # Вариант 3: Автоматический выбор меток Matplotlib
    # plt.gca().xaxis.set_major_locator(plt.MaxNLocator(15))  # Макс 15 меток
    # plt.xticks(rotation=45, ha='right')

    plt.tight_layout()

    output_path = OUTPUT_DIR / f"{metric_key}.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved plot to {output_path}")


def main():
    data = load_metrics(JSON_PATH)
    print(f"Total data points: {len(data)}")

    # Выводим информацию о временном диапазоне
    if data:
        first_time = build_time_label(data[0]["time"])
        last_time = build_time_label(data[-1]["time"])
        print(f"Time range: {first_time} - {last_time}")

    for mk in METRIC_KEYS:
        plot_metric(data, mk)


if __name__ == "__main__":
    main()