from .generate_int_id import generate_int_id


class ID:
    __v: int = 0

    def __init__(self):
        self.generate()

    def generate(self):
        self.__v = generate_int_id()

    def __str__(self):
        return str(self.__v)

    def __eq__(self, other):
        return self.__v == other.__v

    def __bool__(self):
        return self.__v != 0

    def value(self):
        return self.__v