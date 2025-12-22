from models.routes.route import Route
from models.trains import Train, create_train
from models.trains.dto import TrainConfig
from dataclasses import dataclass
from typing import List
import random
from models.events.train_events import TrainGenerated
from runtime.event_manager import EventManager


@dataclass(frozen=True)
class TrainGeneratorConfig:
    route: Route
    train_configs: List[TrainConfig]
    interval: int
    event_manager: EventManager

class TrainGenerator:
    def __init__(self, cfg: TrainGeneratorConfig):
        self.route = cfg.route
        self.configs = cfg.train_configs
        self.interval = cfg.interval
        self.event_manager = cfg.event_manager

        self._elapsed: float = 0.0

    def advance(self, dt: float) -> None:
        self._elapsed += dt

        while self._elapsed >= self.interval:
            self._elapsed -= self.interval

            train: Train = create_train(random.choice(self.configs))

            self.event_manager.emit(TrainGenerated(train, self.route))