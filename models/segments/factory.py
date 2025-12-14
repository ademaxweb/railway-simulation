from .segment import Segment
from .dto import SegmentConfig, segment_config_from_dict

def create_segment(o: SegmentConfig) -> Segment:
    return Segment(o)

def create_segment_from_dict(d: dict) -> Segment:
    segment_dto = segment_config_from_dict(d)
    return create_segment(segment_dto)