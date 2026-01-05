from abc import ABC, abstractmethod


class RouteStage(ABC):
    pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass