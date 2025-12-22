from .event import Event
from models.trains import Train
from models.stations import Station
from models.routes.route import Route

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

class TrainFinishedUnloading(Event):
    def __init__(self, train: Train, station: Station):
        self.train = train
        self.station = station
        super().__init__()

    def __str__(self) -> str:
        return (
            f"TrainFinishedUnloading("
            f"train={self.train}, station={self.station.name})"
        )


class TrainGenerated(Event):
    def __init__(self, train: Train, route: Route):
        self.train = train
        self.route = route
        super().__init__()

    def __str__(self) -> str:
        return (
            f"TrainGenerated("
            f"train={self.train}, route={self.route})"
        )