from models.stations import Station

class SimDataStation:
    def __init__(self, s: Station):
        self._station = s

    def to_dict(self) -> dict:
        return {
            "id": self._station.id,
            "persons_count": self._station.persons_count
        }
