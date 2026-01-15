from models.routes.route_stage import RouteStage
from models.routes.route_stage_station import RouteStageStation
from models.trains.train import Train
from runtime.route_runtime import RouteRuntime


class SimDataRoute:

    def __init__(self, rr: RouteRuntime):
        self._stage: RouteStage = rr.current_stage.stage
        self._train: Train = rr.train
        self._stage_progress: float = rr.current_stage.progress_percentage
        self._total_delay: float = rr.total_delay


    def to_dict(self) -> dict:
        return {
            "train": self._train.to_dict(),
            "stage": self._stage.to_dict(),
            "stage_progress": round(self._stage_progress, 2),
            "delay": self._total_delay
        }