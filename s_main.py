import pygame
from Board import Board
from Player import Player

pygame.init()
WIDTH = 1000
HEIGHT = 900
FPS = 60
timer = pygame.time.Clock()

# Define the red pieces and their initial locations
red_pieces = ['knight'] + ['apple'] * 31
red_locations = [(x, y) for y in range(8) for x in range(4)]
red_apples_locations = red_locations[1:]
extra_red_apple = {}
red_apple_clues_pos = []

# Define the green pieces and their initial locations
green_pieces = ['apple'] * 31 + ['knight']
green_locations = [(x, y) for y in range(8) for x in range(4, 8)]
green_apples_locations = green_locations[:-1]
extra_green_apple = {}
green_apple_clues_pos = []

# Lists to keep track of captured pieces for each player
red_captured_values = []
green_captured_values = []

# Turn and game state variables
turn_step = 0   # 0 - red turn no selection; 1 - red turn piece selected; 2 - green turn no selection; 3 - green turn piece selected
turn_step_putting_poison = 0
selection = 100
valid_moves = [] 
can_add_values = False
winner = None
is_game_over = False 
round_counter = 1
is_golden_eaten = False
count_red_shield = 0
count_green_shield = 0
is_red_clue = False
red_golden_clue_pos = []
is_green_clue = False
green_golden_clue_pos = []

# Dictionaries to store apple values
red_apple_values = {}
green_apple_values = {}

# Variables to store poison apple locations
red_poison_locations = []
green_poison_locations = []

# Variables to store golden apple locations
red_golden_locations = []
green_golden_locations = []


board = Board(WIDTH, HEIGHT)
apple_scale = (50, 50)
knight_scale = (80, 80)

# Load and scale all game pieces
red_apple = board.load_image('assets/red_apple.png', apple_scale)
red_knight = board.load_image('assets/red_knight.png', knight_scale)
green_knight = board.load_image('assets/green_knight.png', knight_scale)
green_apple = board.load_image('assets/green_apple.png', apple_scale)
red_poisoned_apple = board.load_image('assets/red_poisoned_apple.png', apple_scale)
green_poisoned_apple = board.load_image('assets/green_poisoned_apple.png', apple_scale)
gold_apple = board.load_image('assets/gold_apple.png', apple_scale)

# Organize images into lists
red_images = [red_knight, red_apple, red_poisoned_apple, gold_apple]
green_images = [green_knight, green_apple, green_poisoned_apple, gold_apple]
piece_list = ['knight', 'apple', 'poison', 'golden']

player = 0 # 0  - human player 1 - AI agent
player = Player()  
human_agent = player.choose_color()
AI_color = 'red' if human_agent == 'dark green' else 'green'
AI_prev_move = (0,0) if human_agent == 'dark green' else (7,7)
red_golden_locations, red_pieces = board.draw_golden_apples(red_apples_locations, red_pieces)
green_golden_locations, green_pieces = board.draw_golden_apples(green_apples_locations, green_pieces)

print(f'Red golden locations: {red_golden_locations}')
print(f'Red pieces: {red_pieces}')
print(f'Green golden locations: {green_golden_locations}')
print(f'Green pieces: {green_pieces}')

# Determine initial options for each play
green_options = player.check_options(green_pieces, green_locations, 'green')
red_options = player.check_options(red_pieces, red_locations, 'red')

running = True
while running:
    timer.tick(FPS)
    board.screen.fill('light gray')
    board.draw_board(turn_step, count_red_shield, count_green_shield)
    board.draw_pieces()
    board.draw_captured_values()
    
    pygame.display.flip()
pygame.quit()