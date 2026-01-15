from runtime.event_manager import EventManager
from runtime.simulation_date_time import SimDate
from models.events.statistics_event import TrainsStatistics as EventTrainsStatistics, SaveStatistics as EventSaveStatistics, SaveDailyStatistics as EventSaveDailyStatistics, DelayStatistics as EventDelayStatistics
from models.statistics.statistics_data import StatisticsData
from models.statistics.statistics_data_daily import StatisticsDataDaily
from pathlib import Path
import json

from datetime import datetime as dt


class StatisticsRuntime:
    def __init__(self, event_manager: EventManager):
        now = dt.now()
        formatted = now.strftime("%Y_%m_%d_%H%M")

        self.event_manager = event_manager

        self.stats = StatisticsData()
        self.daily_stats = StatisticsDataDaily()

        self._path = Path(f"stats/trains_{formatted}.json")
        self._daily_path = Path(f"stats/daily_{formatted}.json")

        self.event_manager.subscribe(EventSaveStatistics, self._on_save_statistics)
        self.event_manager.subscribe(EventSaveDailyStatistics, self._on_save_daily_statistics)


        self.event_manager.subscribe(EventTrainsStatistics, self.stats.set_trains)
        self.event_manager.subscribe(EventDelayStatistics, self.stats.set_delays)


    def _append_to_json(self, time: SimDate, daily: bool = False):
        pth = self._daily_path if daily else self._path
        stats =self.daily_stats.to_dict() if daily else self.stats.to_dict()

        if pth.exists():
            with pth.open("r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        data.append({
            "time": time.to_dict(),
            "data": stats
        })

        with pth.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)



    def _on_save_statistics(self, event: EventSaveStatistics):
        self._append_to_json(event.date, False)

    def _on_save_daily_statistics(self, event: EventSaveDailyStatistics):
        self.daily_stats = event.stats
        self._append_to_json(event.date, True)