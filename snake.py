DIRECT_DICT = {"left": (-1, 0), "right": (1, 0),
               "up": (0, -1), "down": (0, 1)}

OPPOSITES = {"left": "right", "right": "left",
             "up": "down", "down": "up"}


class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def position(self):
        return self.x, self.y


class Snake:
    def __init__(self, apple):
        self._setup_body()
        self.apple = apple
        self.direction = None
        self.score = 0

    def _setup_body(self):
        MIDDLE_OF_SCREEN = (19, 19)
        self.body = [Square(*MIDDLE_OF_SCREEN)]

    def reset(self):
        self._setup_body()
        self.score = 0

    def change_direction(self, direction):
        if len(self.body) == 1 or self.direction != OPPOSITES[direction]:
            self.direction = direction
            return True
        return False

    def move(self):
        move_x, move_y = DIRECT_DICT[self.direction]
        x = self.body[0].x + move_x
        y = self.body[0].y + move_y
        self.body.insert(0, Square(x, y))

        if self.eat_apple():
            self.score += 1
        else:
            self.body.pop()

    def eat_apple(self):
        head = self.body[0]
        if head.position() == self.apple.position():
            self.apple.set_random_position()
            return True

    def _hit_own_body(self):
        head = self.body[0]
        for part in self.body[1:]:
            if head.position() == part.position():
                return True
        return False

    def _hit_screen(self):
        x, y = self.body[0].position()
        if x < 0 or x >= 40:
            return True
        elif y < 0 or y >= 40:
            return True
        else:
            return False

    def check_lose(self):
        return self._hit_own_body() or self._hit_screen()
