import json
from pathlib import Path
import matplotlib.pyplot as plt


JSON_PATH = Path("stats/trains.json")
OUTPUT_DIR = Path("stats/plots")
METRIC_KEY = "min_fullness_percentage"


def load_metrics(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_time_label(t: dict) -> str:
    return f'{t["h"]:02d}:{t["m"]:02d}:{t["s"]:02d}'


def plot_metric(data: list, metric_key: str):
    times = []
    values = []

    for item in data:
        times.append(build_time_label(item["time"]))
        values.append(item["data"]["trains"][metric_key])

    OUTPUT_DIR.mkdir(exist_ok=True)

    plt.figure(figsize=(10, 5))
    plt.plot(times, values, marker="o")
    plt.xlabel("Time")
    plt.ylabel(metric_key)
    plt.title(f"{metric_key} over time")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path = OUTPUT_DIR / f"{metric_key}.png"
    plt.savefig(output_path, dpi=150)
    plt.close()

    print(f"Saved plot to {output_path}")


def main():
    data = load_metrics(JSON_PATH)
    plot_metric(data, METRIC_KEY)


if __name__ == "__main__":
    main()
