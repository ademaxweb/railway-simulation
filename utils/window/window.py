from typing import List, Any

class Window():
    def __init__(self, cap: int = 2):
        self._cap: int = cap
        self._list: List = [None] * cap

    @property
    def cap(self) -> int:
        return self._cap

    @property
    def len(self):
        return len(self._list)

    def push(self, value: Any):
        if self.len < self.cap:
            self._list.append(value)
        else:
            self._list = self._list[1:self.len] + [value]

    def get(self, idx: int):
        return self._list[idx]

    def __repr__(self) -> str:
            return self._list.__repr__()