from runtime.event_manager import EventManager
from runtime.simulation_date_time import SimDate
from models.events.statistics_event import TrainsStatistics as EventTrainsStatistics, SaveStatistics as EventSaveStatistics
from models.statistics.statistics_data import StatisticsData
from pathlib import Path
import json


class StatisticsRuntime:
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager
        self.stats = StatisticsData()
        self._path = Path("stats/trains.json")

        self.event_manager.subscribe(EventSaveStatistics, self._on_save_statistics)

        self.event_manager.subscribe(EventTrainsStatistics, self.stats.set_trains)



    def _append_to_json(self, time: SimDate):
        if self._path.exists():
            with self._path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        data.append({
            "time": time.to_dict(),
            "data": self.stats.to_dict()
        })

        with self._path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)



    def _on_save_statistics(self, event: EventSaveStatistics):
        self._append_to_json(event.date)