from .generate_int_id import generate_int_id


class ID:
    __v: int = 0

    def __init__(self, v: int = 0):
        if v == 0:
            self.generate()
        else:
            self.__v = v

    def generate(self):
        self.__v = generate_int_id()

    def __str__(self):
        return str(self.__v)

    def __eq__(self, other):
        return self.__v == other.__v

    def __bool__(self):
        return self.__v != 0

    def __repr__(self):
        return str(self.__v)

    def __hash__(self):
        return hash(self.__v)

    def value(self):
        return self.__v