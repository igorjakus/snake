import pygame
import toml

from sys import exit
from snake import Snake
from apple import Apple


KEYBOARD = {
    pygame.K_w: 'up',
    pygame.K_UP: 'up',

    pygame.K_a: 'left',
    pygame.K_LEFT: 'left',

    pygame.K_d: 'right',
    pygame.K_RIGHT: 'right',

    pygame.K_s: 'down',
    pygame.K_DOWN: 'down',
}


class Game:
    def __init__(self):
        pygame.init()
        self.load_settings()
        self.screen = pygame.display.set_mode(self.window)
        pygame.display.set_caption("Snake, Igor Jakus")

        self.pause = True
        self.delta = 0.0
        self.clock = pygame.time.Clock()

        self.apple = Apple()
        self.snake = Snake(self.apple)

    def run_game(self):
        while True:
            self.delta += self.clock.tick() / self.game_speed
            while self.delta > 1 / 20.0:
                self._check_events()

                # snake behavior
                if not self.pause:
                    self.snake.move()
                    if self.snake.check_lose():
                        self.snake.reset()
                        self.apple.set_random_position()
                        self.pause = True

                self._update_screen()
                self.delta = 0.0

    def load_settings(self):
        with open('settings.toml') as file:
            settings = toml.load(file)
            self.unit = settings['unit']
            self.window = (self.unit * 40, self.unit * 40)
            self.game_speed = 1000.0 / settings['speed']
            self.bg_color = tuple(settings['bg_color'])
            self.snake_color = tuple(settings['snake_color'])
            self.apple_color = tuple(settings['apple_color'])

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

    def _handle_keydown(self, event):
        # Changing direction
        if event.key in KEYBOARD:
            if self.snake.change_direction(KEYBOARD[event.key]):
                self.pause = False

        # Pausing snake movement
        elif event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
            self.pause = True

    def _blit_snake(self):
        rect_size = (self.unit, self.unit)
        for part in self.snake.body:
            position = (part.x * self.unit, part.y * self.unit)
            pygame.draw.rect(self.screen, self.snake_color,
                             (*position, *rect_size))

    def _blit_apple(self):
        rect_size = (self.unit, self.unit)
        position = (self.apple.x * self.unit, self.apple.y * self.unit)
        pygame.draw.rect(self.screen, self.apple_color,
                         (*position, *rect_size))

    def _blit_score(self):
        # scaling font size
        WINDOW_TO_FONT_SIZE_RATIO = 28.5
        font_size = int(self.window[0] // WINDOW_TO_FONT_SIZE_RATIO)
        font = pygame.font.Font('fonts/RobotoMono.ttf', font_size)
        text = font.render(f'score: {self.snake.score}', True, (255, 255, 255))

        # scaling text position
        TEXT_POSITION_RATIO = 0.75
        text_positon = (int(self.window[0]*TEXT_POSITION_RATIO), 0)
        self.screen.blit(text, text_positon)

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self._blit_snake()
        self._blit_apple()
        self._blit_score()
        pygame.display.flip()


# Running the game
if __name__ == '__main__':
    game = Game()
    game.run_game()
