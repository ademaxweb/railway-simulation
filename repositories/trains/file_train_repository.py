from pathlib import Path
import json
from models.trains import Train, create_train_from_dict
from .train_repository import TrainRepository


class FileTrainRepository(TrainRepository):
    _base_path: Path

    def __init__(self, base_path: str | Path):
        self._base_path = Path(base_path)

        if not self._base_path.exists():
            raise FileNotFoundError(f"Не найден путь для репозитория поездов: {self._base_path}")

    def get_all(self) -> list[Train]:
        trains: list[Train] = []

        for file in sorted(self._base_path.glob("*.json")):
            with file.open("r", encoding="utf-8") as f:
                data = json.load(f)

            trains.append(create_train_from_dict(data))

        return trains
