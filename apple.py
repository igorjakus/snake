from random import randint


class Apple:
    def __init__(self):
        self.x, self.y = self._rand_pos()

    def set_random_position(self):
        self.x, self.y = self._rand_pos()

    def position(self):
        return self.x, self.y

    @staticmethod
    def _rand_pos():
        return randint(0, 39), randint(0, 39)
