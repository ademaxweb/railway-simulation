import json
from pathlib import Path
from typing import List
from .station_repository import StationRepository
from models.stations import Station, create_station_from_dict


class FileStationRepository(StationRepository):
    _base_path: Path


    def __init__(self, path: str | Path):
        self._base_path = Path(path)
        if not self._base_path.exists():
            raise FileNotFoundError(f"Не найден путь для репозитория поездов: {self._base_path}")

    def get_all(self) -> List[Station]:
        stations: List[Station] = []

        for file in sorted(self._base_path.glob("*.json")):
            with file.open("r", encoding="utf-8") as f:
                data = json.load(f)

            stations.append(create_station_from_dict(data))

        return stations