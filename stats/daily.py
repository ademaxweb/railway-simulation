import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import sys

JSON_PATH = Path(f"stats/{sys.argv[1]}")  # укажите свой путь
print(JSON_PATH)
OUTPUT_DIR = Path("stats/plots")


def load_metrics(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def plot_total_passengers_by_day(data: list):
    """
    Гистограмма общего количества пассажиров по дням
    """
    days = []
    totals = []

    for item in data:
        # abs_h = 24 → День 1, abs_h = 48 → День 2, и т.д.
        day_num = item["time"]["abs_h"] // 24
        days.append(f"День {day_num}")
        totals.append(item["data"]["total_persons"])


    (OUTPUT_DIR / "passengers").mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))

    # Создаем гистограмму
    bars = plt.bar(days, totals, color=['skyblue', 'lightgreen', 'salmon', 'gold', 'violet', 'lightcoral'][:len(days)])

    # Добавляем значения над столбцами
    for bar, total in zip(bars, totals):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(totals) * 0.01,
                 f'{total:,}'.replace(',', ' '), ha='center', va='bottom', fontsize=10)

    plt.xlabel('Дни')
    plt.ylabel('Количество пассажиров')
    plt.title('Общее количество пассажиров по дням')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()

    output_path = OUTPUT_DIR / "passengers" / "total_passengers_by_day.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved plot to {output_path}")


def plot_passengers_by_station_per_day(data: list):
    """
    Групповая гистограмма: пассажиры по станциям для каждого дня
    """
    if not data:
        return

    # Собираем список всех уникальных станций
    all_stations = []
    station_data = {}  # {station_name: [values_for_day1, values_for_day2, ...]}

    # Инициализируем для всех дней
    n_days = len(data)
    days_labels = []

    for i, item in enumerate(data):
        day_num = item["time"]["abs_h"] // 24
        days_labels.append(f"День {day_num}")

        for station_info in item["data"]["by_stations"]:
            station_name = station_info["station"]
            persons = station_info["persons"]

            if station_name not in all_stations:
                all_stations.append(station_name)
                station_data[station_name] = [0] * n_days

            # Заполняем значение для текущего дня
            station_data[station_name][i] = persons



    (OUTPUT_DIR / "passengers").mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(14, 8))

    # Подготавливаем данные для групповой гистограммы
    n_stations = len(all_stations)

    # Позиции для столбцов (по количеству дней)
    x = np.arange(n_days)

    # Ширина столбца
    width = 0.8 / n_stations if n_stations > 0 else 0.1

    # Цвета для станций
    colors = plt.cm.tab20(np.linspace(0, 1, n_stations))

    # Рисуем столбцы для каждой станции
    bars = []
    for i, station in enumerate(all_stations):
        values = station_data[station]
        pos = x + (i - n_stations / 2 + 0.5) * width
        bars.append(ax.bar(pos, values, width, label=station, color=colors[i]))

    # Настройки осей
    ax.set_xlabel('Дни')
    ax.set_ylabel('Количество пассажиров')
    ax.set_title('Пассажиропоток по станциям по дням')
    ax.set_xticks(x)
    ax.set_xticklabels(days_labels)  # Используем корректные метки дней
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    output_path = OUTPUT_DIR / "passengers" / "passengers_by_station_per_day.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Saved plot to {output_path}")


def plot_stacked_passengers_by_day(data: list):
    """
    Сложенная гистограмма: пассажиры по станциям (столбцы сложены)
    """
    if not data:
        return

    days = []

    # Определяем дни
    for item in data:
        day_num = item["time"]["abs_h"] // 24
        days.append(f"День {day_num}")


    # Собираем все станции (предполагаем, что станции одинаковые во всех днях)
    first_day_stations = [s["station"] for s in data[0]["data"]["by_stations"]]
    station_names = first_day_stations

    # Подготавливаем данные для сложенной гистограммы
    station_data = np.zeros((len(station_names), len(days)))

    for day_idx, item in enumerate(data):
        for station_info in item["data"]["by_stations"]:
            station_name = station_info["station"]
            persons = station_info["persons"]
            station_idx = station_names.index(station_name)
            station_data[station_idx, day_idx] = persons

    (OUTPUT_DIR / "passengers").mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 8))

    # Цвета для станций
    colors = plt.cm.tab20c(np.linspace(0, 1, len(station_names)))

    # Рисуем сложенную гистограмму
    bottom_vals = np.zeros(len(days))

    for i, station in enumerate(station_names):
        values = station_data[i]
        ax.bar(days, values, bottom=bottom_vals, label=station, color=colors[i])
        bottom_vals += values

    ax.set_xlabel('Дни')
    ax.set_ylabel('Количество пассажиров')
    ax.set_title('Пассажиропоток по станциям (сложенная гистограмма)')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    output_path = OUTPUT_DIR / "passengers" / "stacked_passengers_by_day.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Saved plot to {output_path}")


def plot_passengers_heatmap(data: list):
    """
    Тепловая карта пассажиропотока по станциям и дням
    """
    if not data:
        return

    days = []
    station_names = []

    # Определяем дни
    for item in data:
        day_num = item["time"]["abs_h"] // 24
        days.append(f"День {day_num}")

    # Собираем все уникальные станции
    station_set = set()
    for item in data:
        for station_info in item["data"]["by_stations"]:
            station_set.add(station_info["station"])

    station_names = sorted(station_set)

    # Создаем матрицу данных
    heatmap_data = np.zeros((len(station_names), len(days)))

    for day_idx, item in enumerate(data):
        for station_info in item["data"]["by_stations"]:
            station_name = station_info["station"]
            persons = station_info["persons"]
            station_idx = station_names.index(station_name)
            heatmap_data[station_idx, day_idx] = persons

    (OUTPUT_DIR / "passengers").mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 8))

    # Создаем тепловую карту
    im = ax.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')

    # Настраиваем оси
    ax.set_xticks(np.arange(len(days)))
    ax.set_yticks(np.arange(len(station_names)))
    ax.set_xticklabels(days)
    ax.set_yticklabels(station_names)

    # Поворачиваем подписи на оси X
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # Добавляем цветовую шкалу
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Количество пассажиров", rotation=-90, va="bottom")

    # Добавляем значения в ячейки
    for i in range(len(station_names)):
        for j in range(len(days)):
            text = ax.text(j, i, f'{int(heatmap_data[i, j]):,}'.replace(',', ' '),
                           ha="center", va="center",
                           color="black" if heatmap_data[i, j] < np.max(heatmap_data) / 2 else "white")

    ax.set_title("Тепловая карта пассажиропотока по станциям и дням")
    plt.tight_layout()

    output_path = OUTPUT_DIR / "passengers" / "passengers_heatmap.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Saved plot to {output_path}")


def main():
    data = load_metrics(JSON_PATH)
    print(f"Total data points: {len(data)}")

    if not data:
        print("No data found!")
        return



    # Проверяем минимальное значение abs_h
    min_abs_h = min(item["time"]["abs_h"] for item in data)

    # Строим все графики
    plot_total_passengers_by_day(data)
    plot_passengers_by_station_per_day(data)
    plot_stacked_passengers_by_day(data)
    plot_passengers_heatmap(data)

    print("\nAll plots generated successfully!")


if __name__ == "__main__":
    main()