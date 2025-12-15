from .segment import Segment
from .dto import SegmentConfig, segment_config_from_dict
from typing import Callable
from utils import ID
from models.stations import Station

def create_segment(o: SegmentConfig) -> Segment:
    return Segment(o)

def create_segment_from_dict(d: dict, get_station_by_id: Callable[[ID], Station | None]) -> Segment:
    segment_dto = segment_config_from_dict(d, get_station_by_id)
    return create_segment(segment_dto)