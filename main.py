import pygame
import random
from Agent import MinimaxAgent

pygame.init()

##########################################################################
# SCREEN DISPLAY
##########################################################################
# Set screen dimensions and create a display surface
WIDTH = 1000
HEIGHT = 900
FPS = 60
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Knight Sweeper")
font = pygame.font.Font('freesansbold.ttf', 20)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()


##########################################################################
# GAME VARIABLES
##########################################################################
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
is_putting_poison_done = False
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


##########################################################################
# GAME IMAGES
##########################################################################
# load in game pieces
apple_scale = (50, 50)
knight_scale = (80, 80)

# Load and scale images
def load_image(path, scale):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, scale)

# Load and scale all game pieces
red_apple = load_image('assets/red_apple.png', apple_scale)
red_knight = load_image('assets/red_knight.png', knight_scale)
green_knight = load_image('assets/green_knight.png', knight_scale)
green_apple = load_image('assets/green_apple.png', apple_scale)
red_poisoned_apple = load_image('assets/red_poisoned_apple.png', apple_scale)
green_poisoned_apple = load_image('assets/green_poisoned_apple.png', apple_scale)
gold_apple = load_image('assets/gold_apple.png', apple_scale)

# Organize images into lists
red_images = [red_knight, red_apple, red_poisoned_apple, gold_apple]
green_images = [green_knight, green_apple, green_poisoned_apple, gold_apple]
piece_list = ['knight', 'apple', 'poison', 'golden']

# check variables / flashing the counter
def add_apple_values():
    """
    Assigns random values to apples for both red and green teams.
    Values are assigned randomly between 2 and 9, with the exception
    that a value of 1 is assigned if an adjacent square contains an apple.

    Parameters:
    Non

    Returns:
    None
    """
    global red_apple_values, green_apple_values, red_golden_locations, green_golden_locations, green_locations, red_locations

    def is_valid_position(pos, poisoned_locations, player):
        x, y = pos
        # Check if position is out of bounds (negative positions)
        if x < 0 or y < 0 or x > 7 or y > 7:
            return False
        # Check if position is in poisoned locations, golden apples locations, or horse location
        if player == 'red':
            forbidden_locations = set(poisoned_locations) | set(red_golden_locations) | {(0, 0)} | set(green_locations)

        else:
            forbidden_locations = set(poisoned_locations) | set(green_golden_locations) | {(7, 7)} | set(red_locations)
 
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
        
    # Get adjacent cells for red poisoned apples
    red_poisoned_adjacent_cells = get_adjacent_cells(red_poison_locations, 'red')
    for idx, cell in enumerate(red_poisoned_adjacent_cells):
        if idx == 4:
            break
        for pos in cell:
            if pos not in red_apple_values:
                red_apple_values[pos] = 1
                break
    
    if len(red_apple_values) < 4: 
        for i in range(4-len(red_apple_values)):
            for pos in list(set(red_poisoned_adjacent_cells[0] + red_poisoned_adjacent_cells[1] + red_poisoned_adjacent_cells[2] + red_poisoned_adjacent_cells[3])):
                if pos not in red_apple_values:
                    red_apple_values.update({pos: 1})
                    break

    red_apple_values.update({loc: random.randint(2, 9) for loc in red_apples_locations if loc not in red_apple_values})

    
    # Get adjacent cells for green poisoned apples
    green_poisoned_adjacent_cells = get_adjacent_cells(green_poison_locations, 'green')
    for idx, cell in enumerate(green_poisoned_adjacent_cells):
        if idx == 4:
            break
        for pos in cell:
            if pos not in green_apple_values:
                green_apple_values[pos] = 1
                break
                    
    if len(green_apple_values) < 4: 
        for i in range(4-len(green_apple_values)):
            for pos in list(set(green_poisoned_adjacent_cells[0] + green_poisoned_adjacent_cells[1] + green_poisoned_adjacent_cells[2] + green_poisoned_adjacent_cells[3])):
                if pos not in green_apple_values:
                    green_apple_values.update({pos: 1})
                    break

    green_apple_values.update({loc: random.randint(2, 9) for loc in green_apples_locations if loc not in green_apple_values})



def draw_board():
    """
    Draws the main game board, including grid lines, status text, and board borders.

    Parameters:
    None

    Returns:
    None
    """
    for i in range(32):
        pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
        pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 100], 5)
        pygame.draw.rect(screen, 'gold', [800, 0, 200, HEIGHT], 5)
        
        if is_putting_poison_done:
            status_text = ['Red: Select a Piece to Move!', 'Red: Select a Destination',
                        'Green: Select a Piece to Move!', 'Green: Select a Destination']
            screen.blit(font.render(status_text[turn_step], True, 'black'), (20, 820))
        else:
            status_text = ['Red: Choose where to put the poison apple', 'Green: Choose where to put the poison apple']
            screen.blit(font.render(status_text[turn_step_putting_poison], True, 'black'), (20, 820))
        
        # if players have shield
        golden_text = None
        if count_red_shield > 0 and turn_step == 1:
            golden_text = f"Red: You have {count_red_shield} shield!"
        elif count_green_shield > 0 and turn_step == 3:
            golden_text = f"Green: You have {count_green_shield} shield!"
            
        screen.blit(font.render(golden_text, True, 'black'), (20, 860))
            
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
            
    # Loop through red golden clue positions and draw blue highlight
    for pos in red_golden_clue_pos:
        x, y = pos
        pygame.draw.rect(screen, 'dark gray', (x * 100 + 1, y * 100 + 1, 98, 98))
    
    # Loop through green golden clue positions and draw blue highlight
    for pos in green_golden_clue_pos:
        x, y = pos
        pygame.draw.rect(screen, 'dark gray', (x * 100 + 1, y * 100 + 1, 98, 98))
        
def draw_pieces():
    """
    Draws the game pieces on the board, including highlighting the selected piece.

    Parameters:
    None

    Returns:
    None
    """
    for i in range(len(red_pieces)):
        index = piece_list.index(red_pieces[i])
        x, y = red_locations[i]
        if red_pieces[i] == 'knight':
            screen.blit(red_images[index], (x * 100 + 10, y * 100 + 10))
        else:
            screen.blit(red_images[index], (x * 100 + 22, y * 100 + 30))
            value = red_apple_values.get((x, y), 0)
            screen.blit(font.render(str(value), True, 'white'), (x * 100 + 40, y * 100 + 40))
        if turn_step < 2 and selection == i and red_pieces[i] == 'knight':
            pygame.draw.rect(screen, 'yellow', [red_locations[i][0] * 100 + 1, red_locations[i][1] * 100 + 1, 
                             100, 100], 2)

    for i in range(len(green_pieces)):
        index = piece_list.index(green_pieces[i])
        x, y = green_locations[i]
        if green_pieces[i] == 'knight':
            screen.blit(green_images[index], (x * 100 + 10, y * 100 + 10))
        else:
            screen.blit(green_images[index], (x * 100 + 22, y * 100 + 30))
            value = green_apple_values.get((x, y), 0)
            screen.blit(font.render(str(value), True, 'white'), (x * 100 + 40, y * 100 + 40))
        if turn_step >= 2 and selection == i and green_pieces[i] == 'knight':
            pygame.draw.rect(screen, 'green', [green_locations[i][0] * 100 + 1, green_locations[i][1] * 100 + 1, 
                             100, 100], 5)

def draw_golden_apples():
    """
    Randomly selects two locations for golden apples from red and green locations, excluding the knights' initial positions, 
    and updates the respective pieces lists to include golden apples.

    Parameters:
    None

    Returns:
    None
    """
    global red_golden_locations, green_golden_locations

    # Randomly choose two locations from red_locations excluding (0,0)
    red_golden_locations = random.sample([loc for loc in red_locations if loc != (0,0)], 2)

    # Randomly choose two locations from green_locations excluding (7,7)
    green_golden_locations = random.sample([loc for loc in green_locations if loc != (7,7)], 2)
    
    for i in range(2):
        red_golden_index = red_locations.index(red_golden_locations[i])
        red_pieces[red_golden_index] = 'golden'
        
        green_golden_index = green_locations.index(green_golden_locations[i])
        green_pieces[green_golden_index] = 'golden'

        

def draw_poisoned_apples():
    """
    Allows players to place poisoned apples on the board during the initial setup phase.

    Parameters:
    None

    Returns:
    None
    """
    global is_putting_poison_done, turn_step_putting_poison, can_add_values, green_golden_locations, red_golden_locations, green_poison_locations, red_poison_locations
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
        
            # red to put poison
            if turn_step_putting_poison == 0 and click_coords in red_locations and click_coords != (0, 0) and click_coords not in red_golden_locations and click_coords not in red_poison_locations:
                red_poison_locations.append(click_coords)
                red_piece_index = red_locations.index(click_coords)
                red_pieces[red_piece_index] = 'poison'
                
                if len(red_poison_locations) == 4:
                    turn_step_putting_poison = 1
                    
            elif turn_step_putting_poison == 1 and click_coords in green_locations and click_coords != (7, 7) and click_coords not in green_golden_locations and click_coords not in green_poison_locations:
                green_poison_locations.append(click_coords)
                green_piece_index = green_locations.index(click_coords)
                green_pieces[green_piece_index] = 'poison'
                
                if len(green_poison_locations) == 4:
                    is_putting_poison_done = True
                    can_add_values = True



# check valid knight moves
def check_knight(position, color):
    """
    Checks for valid knight moves from a given position.

    Parameters:
    position (tuple): The current position of the knight.
    color (str): The color of the knight, either 'red' or 'green'.
    
    Returns:
    moves_list (list): A list of valid move positions for the knight.
    """
    moves_list = []
    if color == 'red':
        enemies_list = green_locations
        friends_list = red_locations
    else:
        enemies_list = red_locations
        friends_list = green_locations
    
    
    # 8 squares to check for knight, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if (target in friends_list or target in enemies_list) and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list

# check for valid moves for just selected piece
def check_valid_moves():
    """
    Checks for valid moves for the currently selected piece.

    Parameters:
    None
    
    Returns:
    valid_options (list): A list of valid move positions for the selected piece.
    """
    if turn_step < 2: 
        options_list = red_options
    else:
        options_list = green_options
    valid_options = options_list[selection]
    return valid_options


def check_options(pieces, locations, turn):
    """
    Generates a list of valid moves for all pieces of a given color.

    Parameters:
    pieces (list): A list of pieces for the current player.
    locations (list): A list of current positions for the pieces.
    turn (str): The color of the current player, either 'red' or 'green'.
    
    Returns:
    all_moves_list (list): A list containing lists of valid move positions for each piece.
    """
    moves_list = []
    all_moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == 'knight':
            moves_list = check_knight(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list



# draw valid moves
def draw_valid(moves):
    """
    Draws the valid moves for the selected piece on the board.

    Parameters:
    moves (list): A list of valid move positions for the selected piece.
    
    Returns:
    None
    """
    color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)
    
# draw captured values on the side
def draw_captured_values():
    """
    Calculates and displays the total values of captured apples for the current player on the right side of the screen.

    Parameters:
    None

    Returns:
    None
    """

    red_score = sum(red_captured_values)        
    green_score = sum(green_captured_values)
    
    score_text = f"Round: {round_counter} \nScores:\nred = {red_score}\ngreen = {green_score}"
    
    lines = score_text.split('\n')
    y_offset = 20
    for line in lines:
        screen.blit(font.render(line, True, 'black'), (820, y_offset))
        y_offset += 60


def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press enter to restart!', True, 'white'), (210, 240))
    
    
def draw_dialogue_box():
    """
    Draws a dialogue box asking the user to choose between a shield or clues about the poison location.

    Parameters:
    None

    Returns:
    str: The choice made by the user ('shield' or 'clues').
    """
    # Define dialogue box dimensions and position
    box_width = 400
    box_height = 200
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2

    # Define text options and their positions
    congrats_text = font.render(f"You have eaten a golden apple!", True, 'black')
    choose_text = font.render(f"Choose an option:", True, 'black')
    shield_text = font.render("1. Shield", True, 'black')
    clues_text = font.render("2. Clues about poison", True, 'black')

    # Create rectangles for clickable areas
    shield_rect = pygame.Rect(box_x + 50, box_y + 100, shield_text.get_width(), shield_text.get_height())
    clues_rect = pygame.Rect(box_x + 50, box_y + 140, clues_text.get_width(), clues_text.get_height())


    # Draw the dialogue box and text options
    pygame.draw.rect(screen, 'white', [box_x, box_y, box_width, box_height])
    pygame.draw.rect(screen, 'black', [box_x, box_y, box_width, box_height], 3)
    screen.blit(congrats_text, (box_x + 50, box_y + 20))
    screen.blit(choose_text, (box_x + 50, box_y + 60))
    screen.blit(shield_text, (box_x + 50, box_y + 100))
    screen.blit(clues_text, (box_x + 50, box_y + 140))

    pygame.display.flip()
    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if shield_rect.collidepoint(mouse_pos):
                    return 'shield'
                elif clues_rect.collidepoint(mouse_pos):
                    return 'clues'
    
    
def draw_golden_clues():
    """
    Draws blue highlighting on cells adjacent to the poisoned region that do not have a value of 1.

    Parameters:
    None

    Returns:
    None
    """
    global screen, red_poison_locations, green_poison_locations, red_apple_values, green_apple_values
    
    def is_valid_position(pos, poisoned_locations, player):
        x, y = pos
        # Check if position is out of bounds (negative positions)
        if x < 0 or y < 0 or x > 7 or y > 7:
            return False
        # Check if position is in poisoned locations, golden apples locations, or horse location
        if player == 'red':
            if pos in poisoned_locations or pos == (0, 0) or pos in green_locations or pos in red_golden_clue_pos:
                return False
            if pos in red_apple_values.keys():
                if red_apple_values[pos] == 1:
                    return False
        else:
            if pos in poisoned_locations or pos == (7, 7) or pos in red_locations or pos in green_golden_clue_pos:
                return False   
            if pos in green_apple_values.keys():
                if green_apple_values[pos] == 1:
                    return False
            
        return True
    
    def possible_adjacent_locations(poisoned_locations, player):
        adjacent_cells = []
        for loc in poisoned_locations:
            x, y = loc
            adjacent_positions = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)]
            adj_cells_for_loc = []
            for pos in adjacent_positions:
                if is_valid_position(pos, poisoned_locations, player):
                    adj_cells_for_loc.append(pos)
            adj_cells_for_loc.sort(key=lambda cell: len([c for c in adjacent_positions if is_valid_position(c, poisoned_locations, player)]))
            adjacent_cells.append(adj_cells_for_loc)
        
        for cell in adjacent_cells[0]:
            if cell in adjacent_cells[1]:
                adjacent_cells[1].remove(cell)
                
        return list(set(adjacent_cells[0] + adjacent_cells[1]))
    
    if turn_step in (0,1):
        # Get adjacent cells for red poisoned apples
        red_poisoned_adjacent_cells = possible_adjacent_locations(red_poison_locations, 'red')
        random_clue = random.choice(red_poisoned_adjacent_cells)
        red_golden_clue_pos.append(random_clue)
        if AI_color == 'green':
            print("red to")
            agent.update_clue_probabilities(random_clue)
    else:
        # Get adjacent cells for green poisoned apples
        green_poisoned_adjacent_cells = possible_adjacent_locations(green_poison_locations, 'green')
        random_clue = random.choice(green_poisoned_adjacent_cells)
        green_golden_clue_pos.append(random_clue)
        if AI_color == 'red':
            print("green to")
            agent.update_clue_probabilities(random_clue)
    
def choose_color():
    """
    Function to let the player choose between Red and Green before starting the game.
    Returns:
        str: 'red' if the player chooses Red, 'green' if the player chooses Green.
    """
    colors = ['dark red', 'dark green']
    random.shuffle(colors)  # Shuffle the colors to randomize their positions
    
    while True:
        screen.fill('white')
        text = font.render("Choose your color:", True, 'black')
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(text, text_rect)
        
        card_width, card_height = 200, 100
        card_margin = 50
        card1_button = pygame.Rect(WIDTH // 4 - card_width // 2, HEIGHT // 2, card_width, card_height)
        pygame.draw.rect(screen, 'gray', card1_button)  # Replace with initial hidden color
        pygame.draw.rect(screen, 'black', card1_button, 5)
        
        card2_button = pygame.Rect(3 * WIDTH // 4 - card_width // 2, HEIGHT // 2, card_width, card_height)
        pygame.draw.rect(screen, 'gray', card2_button)  # Replace with initial hidden color
        pygame.draw.rect(screen, 'black', card2_button, 5)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if card1_button.collidepoint(mouse_pos):
                    # Flip card 1 to reveal true color
                    pygame.draw.rect(screen, colors[0], card1_button)
                    pygame.display.flip()
                    pygame.time.wait(1000)  # Optional delay before returning color
                    return colors[0]
                elif card2_button.collidepoint(mouse_pos):
                    # Flip card 2 to reveal true color
                    pygame.draw.rect(screen, colors[1], card2_button)
                    pygame.display.flip()
                    pygame.time.wait(1000)  # Optional delay before returning color
                    return colors[1]


##########################################################################
# MAIN LOOP
##########################################################################
human_agent = 'dark red'
AI_color = 'red' if human_agent == 'dark green' else 'green'
player = 0 # 0  - human player 1 - AI agent
AI_prev_move = (0,0) if human_agent == 'dark green' else (7,7)
draw_golden_apples()

# Determine initial options for each player
green_options = check_options(green_pieces, green_locations, 'green')
red_options = check_options(red_pieces, red_locations, 'red')


run = True
while run:
    timer.tick(FPS)
    screen.fill('light gray')
    draw_board()
    draw_pieces()
    draw_captured_values()
    num_of_poisons = len(red_poison_locations) + len(green_poison_locations)

    if not is_putting_poison_done:
        draw_poisoned_apples()
    
    if can_add_values:
        add_apple_values() 
        can_add_values = False
        if human_agent == 'dark green':
            green_apple_clues_pos = [pos for pos, val in green_apple_values.items() if val == 1]
            agent = MinimaxAgent('red', green_apple_values, green_locations, green_apple_clues_pos, red_poison_locations)
            player = 1
            for clue_pos in green_apple_clues_pos:
                agent.update_clue_probabilities(clue_pos)
            agent.draw_possible_poison_locations(num_of_poisons)
        else:
            red_apple_clues_pos = [pos for pos, val in red_apple_values.items() if val == 1]
            agent = MinimaxAgent('green', red_apple_values, red_locations, red_apple_clues_pos, green_poison_locations)
            player = 0
            for clue_pos in red_apple_clues_pos:
                agent.update_clue_probabilities(clue_pos)
            agent.draw_possible_poison_locations(num_of_poisons)

    if is_golden_eaten:
        choice = draw_dialogue_box()
        if choice == 'shield':
            if turn_step in (0, 1):
                count_green_shield += 1
            else:
                count_red_shield += 1
        elif choice == 'clues':   
            draw_golden_clues()
        is_golden_eaten = False

    if selection != 100 and not is_game_over:
        valid_moves = check_valid_moves()
        if len(valid_moves) > 0:
            draw_valid(valid_moves)
            if turn_step > 1:
                filtered_moves = [move for move in valid_moves if move != AI_prev_move]
                print("green")
                best_move = agent.minimax_action(filtered_moves)
                print(f"Best Move: {best_move}")
            
        else:
            if turn_step in (2, 3) and len(red_locations) < 30:
                winner = 'Green'
                print("no moves left for red")

            elif turn_step in (0, 1) and len(green_locations) < 30:
                winner = 'Red'
                print("no moves left for green")
            is_game_over = True
        
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not is_game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            
            # Red player's turn handling
            if turn_step <= 1:  
                # filtered_moves = [move for move in valid_moves if move != AI_prev_move]
                # if AI_color == 'red':
                #     click_coords = agent.minimax_action(filtered_moves)
                #     print(f"Clicked coords: {click_coords}")
                
                if click_coords in red_locations:
                    selection = red_locations.index(click_coords)                  
                    if red_pieces[selection] == 'knight':  # Only allow selection if it's a knight
                        if turn_step == 0:
                            turn_step = 1
                            
                if click_coords in valid_moves and selection != 100:
                    if len(extra_red_apple) != 0:
                        index = list(extra_red_apple.keys())[0]
                        if extra_red_apple[index] in red_golden_locations:
                            red_pieces.insert(index, 'golden')
                        else:
                            red_pieces.insert(index, 'apple')
                        red_locations.insert(index, extra_red_apple[index])
                        extra_red_apple = {}
                        
                    if click_coords in green_locations:
                        green_piece_idx = green_locations.index(click_coords)
                        if green_pieces[green_piece_idx] == 'knight':
                            winner = "Red"
                            is_game_over = True
                        else:
                            red_captured_values.append(green_apple_values[click_coords])
                        
                        if green_pieces[green_piece_idx] == 'poison':
                            if count_red_shield == 0:
                                winner = "Green"
                                is_game_over = True
                            else:
                                count_red_shield -= 1
                        
                        if green_pieces[green_piece_idx] == 'golden':
                            is_golden_eaten = True

                        green_pieces.pop(green_piece_idx)
                        green_locations.pop(green_piece_idx)

                    elif click_coords in red_locations:
                        red_piece_idx = red_locations.index(click_coords)
                        extra_red_apple = {red_piece_idx: click_coords}
                        if red_pieces[red_piece_idx] == 'poison':
                            winner = 'Green'
                            is_game_over = True
                        red_pieces.pop(red_piece_idx)
                        red_locations.pop(red_piece_idx)
                    
                    red_locations[0] = click_coords
                    red_pieces[0] = 'knight'
                    agent.update_probability(click_coords)
                    agent.draw_possible_poison_locations(num_of_poisons)
                    if AI_color == 'red':
                        AI_prev_move = click_coords
                    
                    green_options = check_options(green_pieces, green_locations, 'green')
                    red_options = check_options(red_pieces, red_locations, 'red')
                    turn_step = 2
                    selection = 100
                    valid_moves = [] 
            
            # Green player's turn handling
            if turn_step > 1: 
                filtered_moves = [move for move in valid_moves if move != AI_prev_move]
                # if AI_color == 'green': 
                #     print("green")
                #     best_move = agent.minimax_action(filtered_moves)
                #     print(f"Best Move: {best_move}")
                    
                if click_coords in green_locations:
                    selection = green_locations.index(click_coords)
                    if green_pieces[selection] == 'knight':  # Only allow selection if it's a knight
                        if turn_step == 2:
                            turn_step = 3
                                                        
                if click_coords in valid_moves and selection != 100:
                    if len(extra_green_apple) != 0:
                        index = list(extra_green_apple.keys())[0]
                        if extra_green_apple[index] in green_golden_locations:
                            green_pieces.insert(index, 'golden')
                        else:
                            green_pieces.insert(index, 'apple')
                        green_locations.insert(index, extra_green_apple[index])
                        extra_green_apple = {}
                    
                    if click_coords in red_locations:
                        red_piece_idx = red_locations.index(click_coords)
                        if red_pieces[red_piece_idx] == 'knight':
                            winner = 'Green'
                            is_game_over = True
                        else:
                            green_captured_values.append(red_apple_values[click_coords])
                        
                        if red_pieces[red_piece_idx] == 'poison':
                            if count_green_shield == 0:
                                winner = "Red"
                                is_game_over = True
                            else:
                                count_green_shield -= 1
                                                
                        if red_pieces[red_piece_idx] == 'golden':
                            is_golden_eaten = True
                        
                        red_pieces.pop(red_piece_idx)
                        red_locations.pop(red_piece_idx)                      
                        
                    elif click_coords in green_locations:
                        green_piece_idx = green_locations.index(click_coords)
                        extra_green_apple = {green_piece_idx: click_coords}
                        if green_pieces[green_piece_idx] == 'poison':
                            winner = 'Red'
                            is_game_over = True
                        green_pieces.pop(green_piece_idx)
                        green_locations.pop(green_piece_idx)
                        
                    round_counter += 1
                    green_locations[-1] = click_coords
                    green_pieces[-1] = 'knight'
                    agent.update_probability(click_coords)
                    agent.draw_possible_poison_locations(num_of_poisons)
                    if AI_color == 'green':
                        AI_prev_move = click_coords
                            
                    green_options = check_options(green_pieces, green_locations, 'green')
                    red_options = check_options(red_pieces, red_locations, 'red')
                    turn_step = 0
                    selection = 100
                    valid_moves = []

            
        if event.type == pygame.KEYDOWN and is_game_over:
            if event.key == pygame.K_RETURN:
                is_game_over = False
                winner = None
            
    # Determine winner and end game conditions
    if winner or round_counter == 10:
        is_game_over = True
        if not winner:
            sum_red_apple_values = sum(red_captured_values)
            sum_green_apple_values = sum(green_captured_values)
            if sum_green_apple_values > sum_red_apple_values:
                winner = 'Green' 
            else:
                winner = 'Red'
        round_counter = 1
        draw_game_over()
        
    pygame.display.flip()
pygame.quit()
