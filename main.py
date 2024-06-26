import pygame
import random

pygame.init()

WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Knight Sweeper")
font = pygame.font.Font('freesansbold.ttf', 20)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60

##########################################################################
# GAME VARIABLES
##########################################################################
isSecondIter = False
red_pieces = ['knight'] + ['apple'] * 31
red_locations = [(0,0), (1,0), (2,0), (3,0),
                 (0,1), (1,1), (2,1), (3,1),
                 (0,2), (1,2), (2,2), (3,2),
                 (0,3), (1,3), (2,3), (3,3),
                 (0,4), (1,4), (2,4), (3,4),
                 (0,5), (1,5), (2,5), (3,5),
                 (0,6), (1,6), (2,6), (3,6),
                 (0,7), (1,7), (2,7), (3,7)]
red_apples_locations = red_locations[1:]
red_knight_location = (0,0)
extra_red_apple = {}

green_pieces = ['apple'] * 31
green_pieces = green_pieces + ['knight']
green_locations = [(4,0), (5,0), (6,0), (7,0),
                 (4,1), (5,1), (6,1), (7,1),
                 (4,2), (5,2), (6,2), (7,2),
                 (4,3), (5,3), (6,3), (7,3),
                 (4,4), (5,4), (6,4), (7,4),
                 (4,5), (5,5), (6,5), (7,5),
                 (4,6), (5,6), (6,6), (7,6),
                 (4,7), (5,7), (6,7), (7,7)]
green_apples_locations = green_locations[:-2]
green_knight_location = (7,7)
extra_green_apple = {}

captured_pieces_red = []
captured_pieces_green = []

# 0 - red turn no selection; 1 - red turn piece selected; 2 - green turn no selection; 3 - green turn piece selected
turn_step = 0
selection = 100
valid_moves = [] 

# Dictionaries to store apple values
red_apple_values = {}
green_apple_values = {}

##########################################################################
# GAME IMAGES
##########################################################################
# load in game pieces
apple_scale = (50, 50)
apple_scale_small = (30, 30)
knight_scale = (80, 80)
knight_scale_small = (60, 60)

red_apple = pygame.image.load('assets/red_apple.png')
red_apple = pygame.transform.scale(red_apple, apple_scale)
red_apple_small = pygame.transform.scale(red_apple, apple_scale_small)

red_knight = pygame.image.load('assets/red_knight.png')
red_knight = pygame.transform.scale(red_knight, knight_scale)
red_knight_small = pygame.transform.scale(red_knight, knight_scale_small)

green_knight = pygame.image.load('assets/green_knight.png')
green_knight = pygame.transform.scale(green_knight, knight_scale)
green_knight_small = pygame.transform.scale(green_knight, knight_scale_small)

green_apple = pygame.image.load('assets/green_apple.png')
green_apple = pygame.transform.scale(green_apple, apple_scale)
green_apple_small = pygame.transform.scale(green_apple, apple_scale_small)

poisoned_apple = pygame.image.load('assets/poisoned_apple.png')
poisoned_apple = pygame.transform.scale(poisoned_apple, apple_scale)
poisoned_apple_small = pygame.transform.scale(poisoned_apple, apple_scale_small)

gold_apple = pygame.image.load('assets/gold_apple.png')
gold_apple = pygame.transform.scale(gold_apple, apple_scale)
gold_apple_small = pygame.transform.scale(gold_apple, apple_scale_small)

red_images = [red_knight, red_apple]
red_images_small = [red_knight_small, red_apple_small]

green_images = [green_knight, green_apple]
green_images_small = [green_knight_small, green_apple_small]

powerups = [gold_apple, poisoned_apple]
powerups_small = [gold_apple_small, poisoned_apple_small]

piece_list = ['knight', 'apple']
powerups_list = ['golden apple', 'poisoned apple']

# check variables / flashing the counter

def add_apple_values():
    """
    Assigns random values from 1 to 9 to each red and green apple.
    """
    global red_apple_values, green_apple_values
    red_apple_values = {loc: random.randint(1, 9) for loc in red_apples_locations}
    green_apple_values = {loc: random.randint(1, 9) for loc in green_apples_locations}


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
        status_text = ['Red: Select a Piece to Move!', 'Red: Select a Destination',
                       'Green: Select a Piece to Move!', 'Green: Select a Destination']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 820))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)


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

    red_score = sum(captured_pieces_red)        
    green_score = sum(captured_pieces_green)
    
    score_text = f"Scores:\nred = {red_score}\ngreen = {green_score}"
    
    lines = score_text.split('\n')
    y_offset = 20
    for line in lines:
        screen.blit(font.render(line, True, 'black'), (820, y_offset))
        y_offset += 60


##########################################################################
# MAIN LOOP
##########################################################################
add_apple_values()  # Call this function to initialize apple values

green_options = check_options(green_pieces, green_locations, 'green')
red_options = check_options(red_pieces, red_locations, 'red')

run = True
while run:
    timer.tick(fps)
    screen.fill('light gray')
    draw_board()
    draw_pieces()
    draw_captured_values()

    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

            
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            
            if turn_step <= 1: # red to move              
                if click_coords in red_locations:
                    selection = red_locations.index(click_coords)
                    print(f'red_pieces[selection]: {red_pieces[selection]}')
                    if red_pieces[selection] == 'knight':  # Only allow selection if it's a knight
                        if turn_step == 0:
                            turn_step = 1
                            
                if click_coords in valid_moves and selection != 100:
                    red_locations[selection] = click_coords
                    print(f'red_locations[selection]: {red_locations[selection]}')
                    
                    if len(extra_red_apple) != 0:
                        index = list(extra_red_apple.keys())[0]
                        red_pieces.insert(index, 'apple')
                        red_locations.insert(index, extra_red_apple[index])
                        extra_red_apple = {}
                        
                    if click_coords in green_locations:
                        green_piece = green_locations.index(click_coords)
                        captured_pieces_red.append(green_apple_values[click_coords])
                        print(f"green pieces[green piece]: {green_pieces[green_piece]}")
                        green_pieces.pop(green_piece)
                        print(f"green locations[green piece]: {green_locations[green_piece]}")
                        green_locations.pop(green_piece)

                    elif click_coords in red_locations:
                        red_piece = red_locations.index(click_coords)
                        extra_red_apple = {red_piece: click_coords}
                        red_pieces.pop(red_piece)
                        red_locations.pop(red_piece)
                    
                    red_locations[0] = click_coords
                    red_pieces[0] = 'knight'
                    
                    green_options = check_options(green_pieces, green_locations, 'green')
                    red_options = check_options(red_pieces, red_locations, 'red')
                    turn_step = 2
                    selection = 100
                    isSecondIter = True
                    valid_moves = []
                    
                    
            if turn_step > 1: # green to move

                if click_coords in green_locations:
                    selection = green_locations.index(click_coords)
                    if green_pieces[selection] == 'knight':  # Only allow selection if it's a knight
                        if turn_step == 2:
                            turn_step = 3
                                                        
                if click_coords in valid_moves and selection != 100:
                    green_locations[selection] = click_coords
        
                    if len(extra_green_apple) != 0:
                        index = list(extra_green_apple.keys())[0]
                        green_pieces.insert(index, 'apple')
                        green_locations.insert(index, extra_green_apple[index])
                        extra_green_apple = {}
                    
                    if click_coords in red_locations:
                        red_piece = red_locations.index(click_coords)
                        captured_pieces_green.append(red_apple_values[click_coords])
                        red_pieces.pop(red_piece)
                        red_locations.pop(red_piece)                      
                        
                    elif click_coords in green_locations:
                        green_piece = green_locations.index(click_coords)
                        extra_green_apple = {green_piece: click_coords}
                        green_pieces.pop(green_piece)
                        green_locations.pop(green_piece)
                    
                    green_locations[-1] = click_coords
                    green_pieces[-1] = 'knight'
                    
                    green_options = check_options(green_pieces, green_locations, 'green')
                    red_options = check_options(red_pieces, red_locations, 'red')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
                
                
    pygame.display.flip()
pygame.quit()
