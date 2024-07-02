import pygame
import random
from Utils import load_image, add_apple_values, draw_dialogue_box, choose_color
from Board import Board

class GameApp:
    def __init__(self):
        pygame.init()
        self.WIDTH = 1000
        self.HEIGHT = 900
        self.FPS = 60
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        pygame.display.set_caption("Knight Sweeper")
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.big_font = pygame.font.Font('freesansbold.ttf', 50)
        self.timer = pygame.time.Clock()
        self.board = Board(self.screen, self.font)
        self.player = choose_color(self.screen, self.font, self.WIDTH, self.HEIGHT)
        self.AI = 'dark green' if self.player == 'dark red' else 'dark red'
        self.run_game()

    def run_game(self):
        self.board.draw_golden_apples()
        self.board.update_options()
        run = True
        while run:
            self.timer.tick(self.FPS)
            self.screen.fill('light gray')
            self.board.draw_board()
            self.board.draw_pieces()
            self.board.draw_captured_values()

            if not self.board.is_putting_poison_done:
                self.board.draw_poisoned_apples()

            if self.board.can_add_values:
                self.board.add_apple_values()
                self.board.can_add_values = False

            if self.board.is_golden_eaten:
                choice = self.board.draw_dialogue_box(self.screen, self.font, self.WIDTH, self.HEIGHT)
                if choice == 'shield':
                    self.board.update_shield()
                elif choice == 'clues':
                    self.board.draw_golden_clues()
                self.board.is_golden_eaten = False

            if self.board.selection != 100 and not self.board.is_game_over:
                valid_moves = self.board.check_valid_moves()
                if len(valid_moves) > 0:
                    self.board.draw_valid(valid_moves)
                else:
                    self.board.check_game_over()
            
            pygame.display.flip()
            self.board.handle_events()

if __name__ == "__main__":
    GameApp()
