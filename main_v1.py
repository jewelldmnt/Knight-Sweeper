import pygame
import random
from Agent import MinimaxAgent

pygame.init()

class Game:
    def __init__(self):
        self.WIDTH = 1000
        self.HEIGHT = 900
        self.FPS = 60
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        pygame.display.set_caption("Knight Sweeper")
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.big_font = pygame.font.Font('freesansbold.ttf', 50)
        self.timer = pygame.time.Clock()
        self.initialize_game()

    def initialize_game(self):
        self.red_pieces = ['knight'] + ['apple'] * 31
        self.red_locations = [(x, y) for y in range(8) for x in range(4)]
        self.red_apples_locations = self.red_locations[1:]
        self.extra_red_apple = {}
        self.red_apple_clues_pos = []

        self.green_pieces = ['apple'] * 31 + ['knight']
        self.green_locations = [(x, y) for y in range(8) for x in range(4, 8)]
        self.green_apples_locations = self.green_locations[:-1]
        self.extra_green_apple = {}
        self.green_apple_clues_pos = []

        self.red_captured_values = []
        self.green_captured_values = []

        self.turn_step = 0
        self.turn_step_putting_poison = 0
        self.selection = 100
        self.valid_moves = []
        self.is_putting_poison_done = False
        self.can_add_values = False
        self.winner = None
        self.is_game_over = False
        self.round_counter = 1
        self.is_golden_eaten = False
        self.count_red_shield = 0
        self.count_green_shield = 0
        self.is_red_clue = False
        self.red_golden_clue_pos = []
        self.is_green_clue = False
        self.green_golden_clue_pos = []

        self.red_apple_values = {}
        self.green_apple_values = {}
        self.red_poison_locations = []
        self.green_poison_locations = []
        self.red_golden_locations = []
        self.green_golden_locations = []

        self.apple_scale = (50, 50)
        self.knight_scale = (80, 80)
        self.load_images()
        
        self.run_game()

    def load_images(self):
        def load_image(path, scale):
            image = pygame.image.load(path)
            return pygame.transform.scale(image, scale)

        self.red_apple = load_image('assets/red_apple.png', self.apple_scale)
        self.red_knight = load_image('assets/red_knight.png', self.knight_scale)
        self.green_knight = load_image('assets/green_knight.png', self.knight_scale)
        self.green_apple = load_image('assets/green_apple.png', self.apple_scale)
        self.red_poisoned_apple = load_image('assets/red_poisoned_apple.png', self.apple_scale)
        self.green_poisoned_apple = load_image('assets/green_poisoned_apple.png', self.apple_scale)
        self.gold_apple = load_image('assets/gold_apple.png', self.apple_scale)

        self.red_images = [self.red_knight, self.red_apple, self.red_poisoned_apple, self.gold_apple]
        self.green_images = [self.green_knight, self.green_apple, self.green_poisoned_apple, self.gold_apple]
        self.piece_list = ['knight', 'apple', 'poison', 'golden']

    def add_apple_values(self):
        def is_valid_position(pos, poisoned_locations, player):
            x, y = pos
            if x < 0 or y < 0 or x > 7 or y > 7:
                return False
            if player == 'red':
                forbidden_locations = set(poisoned_locations) | set(self.red_golden_locations) | {(0, 0)} | set(self.green_locations)
            else:
                forbidden_locations = set(poisoned_locations) | set(self.green_golden_locations) | {(7, 7)} | set(self.red_locations)
            return pos not in forbidden_locations

        def get_adjacent_cells(poisoned_locations, player):
            adjacent_cells = []
            for loc in poisoned_locations:
                x, y = loc
                adjacent_positions = [
                    (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
                    (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)
                ]
                adj_cells_for_loc = [
                    pos for pos in adjacent_positions
                    if is_valid_position(pos, poisoned_locations, player)
                ]
                adj_cells_for_loc.sort(
                    key=lambda cell: len([
                        c for c in adjacent_positions if is_valid_position(c, poisoned_locations, player)
                    ])
                )
                random.shuffle(adj_cells_for_loc)
                adjacent_cells.append(adj_cells_for_loc)
            return adjacent_cells

        red_poisoned_adjacent_cells = get_adjacent_cells(self.red_poison_locations, 'red')
        for idx, cell in enumerate(red_poisoned_adjacent_cells):
            if idx == 4:
                break
            for pos in cell:
                if pos not in self.red_apple_values:
                    self.red_apple_values[pos] = 1
                    break

        if len(self.red_apple_values) < 4:
            for i in range(4-len(self.red_apple_values)):
                for pos in list(set(red_poisoned_adjacent_cells[0] + red_poisoned_adjacent_cells[1] + red_poisoned_adjacent_cells[2] + red_poisoned_adjacent_cells[3])):
                    if pos not in self.red_apple_values:
                        self.red_apple_values.update({pos: 1})
                        break

        self.red_apple_values.update({loc: random.randint(2, 9) for loc in self.red_apples_locations if loc not in self.red_apple_values})

        green_poisoned_adjacent_cells = get_adjacent_cells(self.green_poison_locations, 'green')
        for idx, cell in enumerate(green_poisoned_adjacent_cells):
            if idx == 4:
                break
            for pos in cell:
                if pos not in self.green_apple_values:
                    self.green_apple_values[pos] = 1
                    break

        if len(self.green_apple_values) < 4:
            for i in range(4-len(self.green_apple_values)):
                for pos in list(set(green_poisoned_adjacent_cells[0] + green_poisoned_adjacent_cells[1] + green_poisoned_adjacent_cells[2] + green_poisoned_adjacent_cells[3])):
                    if pos not in self.green_apple_values:
                        self.green_apple_values.update({pos: 1})
                        break

        self.green_apple_values.update({loc: random.randint(2, 9) for loc in self.green_apples_locations if loc not in self.green_apple_values})

    def draw_board(self):
        for i in range(32):
            pygame.draw.rect(self.screen, 'gray', [0, 800, self.WIDTH, 100])
            pygame.draw.rect(self.screen, 'gold', [0, 800, self.WIDTH, 100], 5)
            pygame.draw.rect(self.screen, 'gold', [800, 0, 200, self.HEIGHT], 5)

            if self.is_putting_poison_done:
                status_text = ['Red: Select a Piece to Move!', 'Red: Select a Destination',
                            'Green: Select a Piece to Move!', 'Green: Select a Destination']
                self.screen.blit(self.font.render(status_text[self.turn_step], True, 'black'), (20, 820))
            else:
                status_text = ['Red: Choose where to put the poison apple', 'Green: Choose where to put the poison apple']
                self.screen.blit(self.font.render(status_text[self.turn_step_putting_poison], True, 'black'), (20, 820))

            golden_text = None
            if self.count_red_shield > 0 and self.turn_step == 1:
                golden_text = f"Red: You have {self.count_red_shield} shield!"
            elif self.count_green_shield > 0 and self.turn_step == 3:
                golden_text = f"Green: You have {self.count_green_shield} shield!"
            self.screen.blit(self.font.render(golden_text, True, 'black'), (20, 860))

            for i in range(9):
                pygame.draw.line(self.screen, 'black', (0, 100 * i), (800, 100 * i), 2)
                pygame.draw.line(self.screen, 'black', (100 * i, 0), (100 * i, 800), 2)

        for pos in self.red_golden_clue_pos:
            x, y = pos
            pygame.draw.rect(self.screen, 'dark gray', (x * 100 + 1, y * 100 + 1, 98, 98))

        for pos in self.green_golden_clue_pos:
            x, y = pos
            pygame.draw.rect(self.screen, 'dark gray', (x * 100 + 1, y * 100 + 1, 98, 98))

        for loc, val in self.red_apple_values.items():
            self.draw_apple(loc, val, 'red')

        for loc, val in self.green_apple_values.items():
            self.draw_apple(loc, val, 'green')

        self.draw_pieces(self.red_pieces, self.red_locations, self.red_poison_locations, self.red_golden_locations, self.red_knight, self.red_poisoned_apple, self.red_apple, self.gold_apple)
        self.draw_pieces(self.green_pieces, self.green_locations, self.green_poison_locations, self.green_golden_locations, self.green_knight, self.green_poisoned_apple, self.green_apple, self.gold_apple)

    def draw_apple(self, loc, val, color):
        x, y = loc
        text = self.font.render(str(val), True, 'black')
        self.screen.blit(text, (x * 100 + 35, y * 100 + 35))

    def draw_pieces(self, pieces, locations, poison_locations, golden_locations, knight_image, poisoned_apple_image, apple_image, golden_apple_image):
        for count, piece in enumerate(pieces):
            if piece == 'knight':
                self.screen.blit(knight_image, (locations[count][0] * 100 + 10, locations[count][1] * 100 + 10))
            elif piece == 'apple' and locations[count] in poison_locations:
                self.screen.blit(poisoned_apple_image, (locations[count][0] * 100 + 25, locations[count][1] * 100 + 25))
            elif piece == 'apple' and locations[count] in golden_locations:
                self.screen.blit(golden_apple_image, (locations[count][0] * 100 + 25, locations[count][1] * 100 + 25))
            elif piece == 'apple':
                self.screen.blit(apple_image, (locations[count][0] * 100 + 25, locations[count][1] * 100 + 25))

    def run_game(self):
        running = True
        while running:
            self.timer.tick(self.FPS)
            self.screen.fill('light gray')
            self.draw_board()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    Game()
