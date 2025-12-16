from utils import ID, Window
from models.stations import Station
from models.segments import Segment
from typing import List
from .dto import RouteConfig, RouteStationConfig
from .route_stage import RouteStage



class Route:

    def __init__(self, o: RouteConfig):
        # Идентификатор
        self._id: ID = ID()
        #
        self._stages: List[RouteStage] = []

        sw = Window(2)
        for s in o.stations:
            pass



    @property
    def id(self) -> ID:
        return self._id