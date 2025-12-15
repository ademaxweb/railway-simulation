import json
from pathlib import Path
from typing import List, Dict
from .station_repository import StationRepository
from models.stations import Station, create_station_from_dict
from utils import ID
from functools import wraps

def check_loaded(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if not self._is_loaded:
            self._load()

        return f(self, *args, **kwargs)

    return wrapper


class FileStationRepository(StationRepository):
    _is_loaded: bool = False
    _base_path: Path
    _id_registry: Dict[ID, Station] = {}

    def __init__(self, path: str | Path):
        self._is_loaded = False
        self._base_path = Path(path)

        if not self._base_path.exists():
            raise FileNotFoundError(f"Не найден путь для репозитория поездов: {self._base_path}")

        self._load()



    def _clear(self):
        self._id_registry.clear()
        self._is_loaded = False

    def _load(self):
        self._clear()

        for file in sorted(self._base_path.glob("*.json")):
            with file.open("r", encoding="utf-8") as f:
                data = json.load(f)

            station = create_station_from_dict(data)

            self._id_registry[station.id] = station

        self._is_loaded = True


    # Получить все станции
    @check_loaded
    def get_all(self) -> List[Station]:
        return list(self._id_registry.values())

    # Получить станцию по ID
    @check_loaded
    def get_by_id(self, station_id: ID) -> Station | None:
        return self._id_registry.get(station_id)