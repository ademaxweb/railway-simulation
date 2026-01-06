class SimDate:
    DAY_SECONDS = 24 * 60 * 60

    def __init__(self, sim_time: float):
        total = int(sim_time)
        day_time = total % SimDate.DAY_SECONDS

        self.abs_h = total // 3600
        self.abs_m = (total % 3600) // 60
        self.abs_s = total % 60

        self.h = day_time // 3600
        self.m = day_time % 3600 // 60
        self.s = day_time % 60

    def __str__(self):
        return f"{self.h:02d}:{self.m:02d}:{self.s:02d}"

    def to_dict(self) -> dict:
        return {
            "h": self.h,
            "m": self.m,
            "s": self.s,
            "abs_h": self.abs_h,
            "abs_m": self.abs_m,
            "abs_s": self.abs_s,
        }