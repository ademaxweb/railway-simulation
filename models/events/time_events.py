from models.events.event import Event


# ---------- бизнес-события ----------

class RushHourStarted(Event):
    def __str__(self) -> str:
        return "RushHourStarted"


class RushHourEnded(Event):
    def __str__(self) -> str:
        return "RushHourEnded"


# ---------- информационные события ----------

class TimeMarkerReached(Event):
    def __init__(self, sim_time: float):
        self.sim_time = sim_time
        super().__init__()

    def __str__(self) -> str:
        total = int(self.sim_time)
        h = total // 3600
        m = (total % 3600) // 60
        s = total % 60
        return f"TimeMarkerReached({h:02d}:{m:02d}:{s:02d})"
