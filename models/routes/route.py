from typing import List
from .route_stage import RouteStage

class Route:
    def __init__(self, stages: List[RouteStage]):
        self.stages = stages

    def __len__(self):
        return len(self.stages)
