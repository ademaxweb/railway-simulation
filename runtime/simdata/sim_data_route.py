from models.routes.route_stage import RouteStage
from models.trains.train import Train


class SimDataRoute:

    def __init__(self, stage: RouteStage, progress: float, train: Train):
        self._stage: RouteStage = stage
        self._train: Train = train
        self._stage_progress: float = progress


    def to_dict(self) -> dict:
        return {
            "train": self._train.to_dict(),
            "stage": self._stage.to_dict(),
            "stage_progress": round(self._stage_progress, 2)
        }