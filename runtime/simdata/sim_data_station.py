from models.stations import Station
from runtime.station_runtime import StationRuntime
from utils import ID


class SimDataStation:
    def __init__(self, sr: StationRuntime):
        self._station = sr.station
        self._trains = {}

        trains = sr.get_trains()
        for train in list(trains.keys()):
            self._trains[str(train.id)] = trains[train].to_dict()




    def to_dict(self) -> dict:
        return {
            "id": self._station.id,
            "persons_count": self._station.persons_count,
            "trains": self._trains
        }
