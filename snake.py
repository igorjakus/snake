import toml
from random import randint


with open('settings.toml') as file:
    settings = toml.load(file)

unit = settings['unit']
snake_color = tuple(settings['snake_color'])
apple_color = tuple(settings['apple_color'])


DIRECT_DICT = {"left": (-unit, 0), "right": (unit, 0),
               "up": (0, -unit), "down": (0, unit)}

OPPOSITES = {"left": "right", "right": "left",
             "up": "down", "down": "up"}


class Square:
    def __init__(self, x=unit * 19, y=unit * 19):
        self.x = x
        self.y = y

    def position(self):
        return self.x, self.y


class Snake:
    def __init__(self, apple):
        self.body = [Square()]
        self.color = snake_color
        self.score = 0
        self.direction = "up"
        self.apple = apple  # get access to the apple

    def reset(self):
        self.body = [Square()]
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
            self.apple.move()
            return True

    def hit_own_body(self):
        head = self.body[0]
        for part in self.body[1:]:
            if head.position() == part.position():
                return True
        return False

    def hit_screen(self):
        x, y = self.body[0].position()
        if x < 0 or x > unit * 39:
            return True
        elif y < 0 or y > unit * 39:
            return True
        else:
            return False

    def check_lose(self):
        return self.hit_own_body() or self.hit_screen()


class Apple:
    def __init__(self):
        self.x, self.y = self.rand_pos()
        self.color = apple_color

    def move(self):
        self.x, self.y = self.rand_pos()

    def position(self):
        return self.x, self.y

    @staticmethod
    def rand_pos():
        return randint(0, 39) * unit, randint(0, 39) * unit
