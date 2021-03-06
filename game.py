import pygame
from sys import exit
from settings import Settings
from snake import Snake, Apple

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
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.window)
        pygame.display.set_caption("Snake Game - Python 3, Igor Jakus")

        self.game_speed = 1000.0 / self.settings.game_speed
        self.delta = 0.0
        self.clock = pygame.time.Clock()
        self.pause = True

        self.snake = Snake(self)
        self.apple = Apple(self)

    def run_game(self):
        while True:
            self.delta += self.clock.tick() / self.game_speed
            while self.delta > 1 / 20.0:
                self._check_events()
                if not self.pause:
                    self.snake.move()
                if self.snake.check_lose():
                    self.snake.reset()
                    self.apple.move()   
                    self.pause = True   
                self.snake.check_apple(self.apple)
                self._update_screen()
                self.delta = 0.0

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.handle_quit()

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)

    @staticmethod
    def handle_quit():
        exit()

    def handle_keydown(self, event):
        # Changing direction
        if event.key in KEYBOARD:
            if self.snake.change_direction(KEYBOARD[event.key]):
                self.pause = False

        # Pausing snake movement
        elif event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
            self.pause = True


    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.snake.blitme()
        self.apple.blitme()
        pygame.display.flip()


# Running the game
if __name__ == '__main__':
    game = Game()
    game.run_game()
