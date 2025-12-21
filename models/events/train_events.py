from .event import Event
from models.trains import Train
from models.stations import Station


class TrainFinishedSegment(Event):
    def __init__(self, train: Train):
        self.train = train
        super().__init__()

    def __str__(self):
        return f"TrainFinishedSegment(train={self.train})"


class TrainArrivedAtStation(Event):
    def __init__(self, train: Train, station: Station):
        self.train = train
        self.station = station
        super().__init__()

    def __str__(self):
        return (
            f"TrainArrivedAtStation(train={self.train}, "
            f"station={self.station.name})"
        )


class TrainFinishedStationWait(Event):
    def __init__(self, train: Train):
        self.train = train
        super().__init__()

    def __str__(self):
        return f"TrainFinishedStationWait(train={self.train})"


class TrainDepartedFromStation(Event):
    def __init__(self, train: Train, station: Station):
        self.train = train
        self.station = station
        super().__init__()

    def __str__(self):
        return (
            f"TrainDepartedFromStation(train={self.train}, "
            f"station={self.station.name})"
        )
