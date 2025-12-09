import utils

class Wagon:

    id:int = 0
    capacity:int = 0
    people:int = 0


    def __init__(self, capacity:int):
        self.id = utils.generate_int_id()
        self.capacity = capacity

    def __str__(self):
        return f"[Вагон №{self.id} ({self.people}/{self.capacity})]"


def create_wagon(cap:int = 100):
    return Wagon(capacity=cap)