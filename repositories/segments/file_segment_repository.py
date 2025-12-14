import json
from pathlib import Path
from typing import List

from .segment_repository import SegmentRepository
from models.segments import Segment, create_segment_from_dict


class FileSegmentRepository(SegmentRepository):
    _base_path: Path

    def __init__(self, path: str | Path):
        self._base_path = Path(path)

        if not self._base_path.exists():
            raise FileNotFoundError(f"Не найден путь для репозитория перегонов: {self._base_path}")

    def get_all(self) -> List[Segment]:
        segments: list[Segment] = []

        for file in sorted(self._base_path.glob("*.json")):
            with file.open("r", encoding="utf-8") as f:
                data = json.load(f)

                if isinstance(data, list):
                    for o in data:
                        segments.append(create_segment_from_dict(o))
                else:
                    segments.append(create_segment_from_dict(data))

        return segments