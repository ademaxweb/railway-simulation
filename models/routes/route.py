from utils import ID
from models.stations import Station
from models.segments import Segment
from typing import List

class Route:

    def __init__(self):
        self._id: ID = ID()
        self._stations: List[Station] = []
        self._segments: List[Segment] = []


    @property
    def id(self) -> ID:
        return self._id