from .route_stage import RouteStage
from models.segments import Segment

class RouteStageSegment(RouteStage):
    def __init__(self, segment: Segment):
        self.segment = segment

    def to_dict(self) -> dict:
        return {
            "id": self.segment.id,
            "type": "segment"
        }