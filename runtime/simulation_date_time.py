class SimDate:

    def __init__(self, sim_time: float):
        total = int(sim_time)
        self.h = total // 3600
        self.m = (total % 3600) // 60
        self.s = total % 60

    def __str__(self):
        return f"{self.h:02d}:{self.m:02d}:{self.s:02d}"

    def to_dict(self) -> dict:
        return {
            "h": self.h,
            "m": self.m,
            "s": self.s
        }