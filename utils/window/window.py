from typing import List, Any, Generic, TypeVar

T = TypeVar("T")


class Window(Generic[T]):
    def __init__(self, cap: int = 2):
        self._cap: int = cap
        self._list: List[T] = []

    @property
    def cap(self) -> int:
        return self._cap

    @property
    def len(self) -> int:
        return len(self._list)

    @property
    def is_full(self) -> bool:
        return self.len >= self._cap

    def push(self, value: T):
        if self.len >= self.cap:
            self._list.pop(0)

        self._list.append(value)

    def clear(self):
        self._list.clear()

    def get(self, idx: int) -> T:
        return self._list[idx]

    def expand(self, c: int = 1):
        if c < 1:
            return
        self._cap += c

    def shrink(self, c: int):
        if c < 1:
            return

        self._cap = max(1, self._cap - c)

        excess = self.len - self._cap
        if excess > 0:
            self._list = self._list[excess:]

    def __repr__(self) -> str:
        return f"Window(cap={self._cap}, data={self._list})"