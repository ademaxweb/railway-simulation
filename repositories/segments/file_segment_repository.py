import json
from pathlib import Path
from typing import List
from functools import wraps

from utils import ID
from .segment_repository import SegmentRepository

from repositories.stations import StationRepository
from models.stations import Station
from models.segments import Segment, create_segment_from_dict

def check_loaded(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if not self._is_loaded:
            self._load()

        return f(self, *args, **kwargs)

    return wrapper

class FileSegmentRepository(SegmentRepository):

    def __init__(self, path: str | Path, station_repository: StationRepository):
        self._base_path = Path(path)

        if not self._base_path.exists():
            raise FileNotFoundError(f"Не найден путь для репозитория перегонов: {self._base_path}")


        self._station_repository = station_repository
        self._is_loaded = False

        self._id_registry: dict[ID, Segment] = {}
        self._station_from_registry: dict[Station, dict[Station, Segment]] = {}
        self._station_to_registry: dict[Station, dict[Station, Segment]] = {}

    def _clear(self):
        self._id_registry.clear()
        self._station_from_registry.clear()
        self._station_to_registry.clear()
        self._is_loaded = False


    def _load(self):
        def load_segment(segment_dict: dict):
            segment = create_segment_from_dict(segment_dict, self._station_repository.get_by_id)
            self._id_registry[segment.id] = segment

            # Реестр перегонов по станции отправления
            if segment.station_from not in self._station_from_registry:
                self._station_from_registry[segment.station_from] = {}
            self._station_from_registry[segment.station_from][segment.station_to] = segment

            # Реестр перегонов по станции прибытия
            if segment.station_to not in self._station_to_registry:
                self._station_to_registry[segment.station_to] = {}
            self._station_to_registry[segment.station_to][segment.station_from] = segment

        self._clear()

        for file in sorted(self._base_path.glob("*.json")):
            with file.open("r", encoding="utf-8") as f:
                data = json.load(f)

                if isinstance(data, list):
                    for o in data:
                        load_segment(o)
                else:
                    load_segment(data)

        self._is_loaded = True


    # Получить все перегоны
    @check_loaded
    def get_all(self) -> List[Segment]:
        return list(self._id_registry.values())

    # Получить перегон по ID
    @check_loaded
    def get_by_id(self, segment_id: ID) -> Segment | None:
        return self._id_registry.get(segment_id)

    @check_loaded
    def get_from_station(self, station: Station) -> List[Segment]:
        if station in self._station_from_registry:
            return list(self._station_from_registry[station].values())

        return []

    @check_loaded
    def get_to_station(self, station: Station) -> List[Segment]:
        if station in self._station_to_registry:
            return list(self._station_to_registry[station].values())

        return []


    @check_loaded
    def get_between_stations(self, from_station: Station, to_station: Station) -> Segment | None:
        segments_from = self._station_from_registry.get(from_station)
        if not segments_from:
            return None

        return segments_from.get(to_station)
