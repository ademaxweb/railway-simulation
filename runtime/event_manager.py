from collections import defaultdict
from typing import Callable, Type


class EventManager:
    def __init__(self):
        self._subs = defaultdict(list)

    def subscribe(self, event_type: Type, handler: Callable):
        self._subs[event_type].append(handler)

    def emit(self, event):
        for handler in self._subs[type(event)]:
            handler(event)
