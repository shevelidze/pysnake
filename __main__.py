import sys, pygame
from menu import MenuMode
from game import GameMode

pygame.init()

class PySnake:
    def __init__(self):
        self.display = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        self.menu_mode = MenuMode(self.mode_to_game)
        self.game_mode = GameMode(self.mode_to_menu)
        self.current_mode = self.menu_mode

    def start_loop(self):
        is_running = True
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            self.current_mode.draw_frame(self.display)
            pygame.display.flip()

    def mode_to_game(self):
        self.current_mode = self.game_mode

    def mode_to_menu(self):
        self.current_mode = self.menu_mode

if __name__ == '__main__':
    game = PySnake()
    game.start_loop()
