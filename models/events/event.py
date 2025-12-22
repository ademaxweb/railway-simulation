from abc import ABC
from typing import Any


class Event:
    def __init__(self):
        # Временный отладочный вывод
        # print(f"[EVENT] {self}")
        pass
    def __str__(self) -> str:
        return self.__class__.__name__
