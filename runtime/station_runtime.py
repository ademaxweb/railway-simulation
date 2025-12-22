from models.events.time_events import RushHourStarted, RushHourEnded


class StationRuntime:
    def __init__(self, station, generator, event_manager):
        self.station = station
        self.generator = generator

        event_manager.subscribe(RushHourStarted, generator.on_rush_started)
        event_manager.subscribe(RushHourEnded, generator.on_rush_ended)

    def advance(self, dt: float, sim_time: float):
        count = self.generator.generate(dt, sim_time)
        if count > 0:
            self.station.add_person(count)

    def __str__(self):
        return (
            f"{self.station.name}: "
            f"{self.station.persons_count}/{self.station.capacity}"
        )
