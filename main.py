import pygame

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
red_pieces = ['knight'] + ['apple'] * 31
red_locations = [(0,0), (1,0), (2,0), (3,0),
                 (0,1), (1,1), (2,1), (3,1),
                 (0,2), (1,2), (2,2), (3,2),
                 (0,3), (1,3), (2,3), (3,3),
                 (0,4), (1,4), (2,4), (3,4),
                 (0,5), (1,5), (2,5), (3,5),
                 (0,6), (1,6), (2,6), (3,6),
                 (0,7), (1,7), (2,7), (3,7)]
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

captured_pieces_red = []
captured_pieces_green = []

# 0 - red turn no selection; 1 - red turn piece selected; 2 - green turn no selection; 3 - green turn no selection
turn_step = 0
selection = 100
valid_moves = []    

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




# draw main game board
def draw_board():
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
    for i in range(len(red_pieces)):
        index = piece_list.index(red_pieces[i])
        x, y = red_locations[i]
        if red_pieces[i] == 'knight':
            screen.blit(red_images[index], (x * 100 + 10, y * 100 + 10))
        else:
            screen.blit(red_images[index], (x * 100 + 22, y * 100 + 30))
        if turn_step < 2 and selection == i:
            pygame.draw.rect(screen, 'red', [x * 100 + 1, y * 100 + 1, 100, 100], 2)

    for i in range(len(green_pieces)):
        index = piece_list.index(green_pieces[i])
        x, y = green_locations[i]
        if green_pieces[i] == 'knight':
            screen.blit(green_images[index], (x * 100 + 10, y * 100 + 10))
        else:
            screen.blit(green_images[index], (x * 100 + 22, y * 100 + 30))
        if turn_step >= 2 and selection == i:
            pygame.draw.rect(screen, 'blue', [x * 100 + 1, y * 100 + 1, 100, 100], 2)



        
        
##########################################################################
# MAIN LOOP
##########################################################################
run = True
while run:
    timer.tick(fps)
    screen.fill('light gray')
    draw_board()
    draw_pieces()
    
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    pygame.display.flip()
pygame.quit()
        
        