import pygame
import random

class Board:
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.big_font = pygame.font.Font('freesansbold.ttf', 50)
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.is_putting_poison_done = False
        self.turn_step_putting_poison = 0

        apple_scale = (50, 50)
        knight_scale = (80, 80)
        # Load and scale all game pieces
        self.red_apple = self.load_image('assets/red_apple.png', apple_scale)
        self.red_knight = self.load_image('assets/red_knight.png', knight_scale)
        self.green_knight = self.load_image('assets/green_knight.png', knight_scale)
        self.green_apple = self.load_image('assets/green_apple.png', apple_scale)
        self.red_poisoned_apple = self.load_image('assets/red_poisoned_apple.png', apple_scale)
        self.green_poisoned_apple = self.load_image('assets/green_poisoned_apple.png', apple_scale)
        self.gold_apple = self.load_image('assets/gold_apple.png', apple_scale)

        # Organize images into lists
        self.red_images = [self.red_knight, self.red_apple, self.red_poisoned_apple, self.gold_apple]
        self.green_images = [self.green_knight, self.green_apple, self.green_poisoned_apple, self.gold_apple]
        self.piece_list = ['knight', 'apple', 'poison', 'golden']
    
    def load_image(self, path, scale):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, scale)

    def draw_golden_apples(self, locations, pieces):
        """
        Randomly selects two locations for golden apples from red and green locations, excluding the knights' initial positions, 
        and updates the respective pieces lists to include golden apples.

        Parameters:
        None

        Returns:
        None
        """
        golden_locations = random.sample([loc for loc in locations], 2)
        
        for i in range(2):
            golden_index = locations.index(golden_locations[i])
            pieces[golden_index] = 'golden'
        
        return golden_locations, pieces
        
    
    def add_apple_values(board):
        board.add_apple_values()

    def draw_dialogue_box(screen, font, WIDTH, HEIGHT):
        box_width = 400
        box_height = 200
        box_x = (WIDTH - box_width) // 2
        box_y = (HEIGHT - box_height) // 2

        congrats_text = font.render(f"You have eaten a golden apple!", True, 'black')
        choose_text = font.render(f"Choose an option:", True, 'black')
        shield_text = font.render("1. Shield", True, 'black')
        clues_text = font.render("2. Clues about poison", True, 'black')

        shield_rect = pygame.Rect(box_x + 50, box_y + 100, shield_text.get_width(), shield_text.get_height())
        clues_rect = pygame.Rect(box_x + 50, box_y + 140, clues_text.get_width(), clues_text.get_height())

        pygame.draw.rect(screen, 'white', [box_x, box_y, box_width, box_height])
        pygame.draw.rect(screen, 'black', [box_x, box_y, box_width, box_height], 3)
        screen.blit(congrats_text, (box_x + 50, box_y + 20))
        screen.blit(choose_text, (box_x + 50, box_y + 60))
        screen.blit(shield_text, (box_x + 50, box_y + 100))
        screen.blit(clues_text, (box_x + 50, box_y + 140))

        pygame.display.flip()
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

    def choose_color(screen, font, WIDTH, HEIGHT):
        colors = ['dark red', 'dark green']
        random.shuffle(colors)

        while True:
            screen.fill('white')
            text = font.render("Choose your color:", True, 'black')
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            screen.blit(text, text_rect)

            card_width, card_height = 200, 100
            card_margin = 50
            card1_button = pygame.Rect(WIDTH // 4 - card_width // 2, HEIGHT // 2, card_width, card_height)
            pygame.draw.rect(screen, 'gray', card1_button)
            pygame.draw.rect(screen, 'black', card1_button, 5)

            card2_button = pygame.Rect(3 * WIDTH // 4 - card_width // 2, HEIGHT // 2, card_width, card_height)
            pygame.draw.rect(screen, 'gray', card2_button)
            pygame.draw.rect(screen, 'black', card2_button, 5)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if card1_button.collidepoint(mouse_pos):
                        pygame.draw.rect(screen, colors[0], card1_button)
                        pygame.display.flip()
                        pygame.time.wait(1000)
                        return colors[0]
                    elif card2_button.collidepoint(mouse_pos):
                        pygame.draw.rect(screen, colors[1], card2_button)
                        pygame.display.flip()
                        pygame.time.wait(1000)
                        return colors[1]


    def draw_board(self, turn_step, count_red_shield, count_green_shield, red_golden_clue_pos, green_golden_clue_pos):
        """
        Draws the main game board, including grid lines, status text, and board borders.

        Parameters:
        None

        Returns:
        None
        """
        for i in range(32):
            pygame.draw.rect(self.screen, 'gray', [0, 800, self.WIDTH, 100])
            pygame.draw.rect(self.screen, 'gold', [0, 800, self.WIDTH, 100], 5)
            pygame.draw.rect(self.screen, 'gold', [800, 0, 200, self.HEIGHT], 5)
            
            if self.is_putting_poison_done:
                status_text = ['Red: Select a Piece to Move!', 'Red: Select a Destination',
                            'Green: Select a Piece to Move!', 'Green: Select a Destination']
                self.screen.blit(self.font.render(status_text[turn_step], True, 'black'), (20, 820))
            else:
                status_text = ['Red: Choose where to put the poison apple', 'Green: Choose where to put the poison apple']
                self.screen.blit(self.font.render(status_text[self.turn_step_putting_poison], True, 'black'), (20, 820))
            
            # if players have shield
            golden_text = None
            if count_red_shield > 0 and turn_step == 1:
                golden_text = f"Red: You have {count_red_shield} shield!"
            elif count_green_shield > 0 and turn_step == 3:
                golden_text = f"Green: You have {count_green_shield} shield!"
                
            self.screen.blit(self.font.render(golden_text, True, 'black'), (20, 860))
                
            for i in range(9):
                pygame.draw.line(self.screen, 'black', (0, 100 * i), (800, 100 * i), 2)
                pygame.draw.line(self.screen, 'black', (100 * i, 0), (100 * i, 800), 2)
                
        # Loop through red golden clue positions and draw blue highlight
        for pos in red_golden_clue_pos:
            x, y = pos
            pygame.draw.rect(self.screen, 'dark gray', (x * 100 + 1, y * 100 + 1, 98, 98))
        
        # Loop through green golden clue positions and draw blue highlight
        for pos in green_golden_clue_pos:
            x, y = pos
            pygame.draw.rect(self.screen, 'dark gray', (x * 100 + 1, y * 100 + 1, 98, 98))
            
    def draw_pieces(self, player, locations, pieces, apple_values, turn_step, selection):
        piece_list = ['knight', 'apple', 'poison', 'golden']
        if player == 'red':
            for i in range(len(pieces)):
                index = piece_list.index(pieces[i])
                x, y = locations[i]
                if pieces[i] == 'knight':
                    self.screen.blit(self.red_images[index], (x * 100 + 10, y * 100 + 10))
                else:
                    self.screen.blit(self.red_images[index], (x * 100 + 22, y * 100 + 30))
                    value = apple_values.get((x, y), 0)
                    self.screen.blit(self.font.render(str(value), True, 'white'), (x * 100 + 40, y * 100 + 40))
                if turn_step < 2 and selection == i and pieces[i] == 'knight':
                    pygame.draw.rect(self.screen, 'yellow', [locations[i][0] * 100 + 1, locations[i][1] * 100 + 1, 
                                    100, 100], 2)
        else:
            for i in range(len(pieces)):
                index = piece_list.index(pieces[i])
                x, y = locations[i]
                if pieces[i] == 'knight':
                    self.screen.blit(self.green_images[index], (x * 100 + 10, y * 100 + 10))
                else:
                    self.screen.blit(self.green_images[index], (x * 100 + 22, y * 100 + 30))
                    value = apple_values.get((x, y), 0)
                    self.screen.blit(self.font.render(str(value), True, 'white'), (x * 100 + 40, y * 100 + 40))
                if turn_step >= 2 and selection == i and pieces[i] == 'knight':
                    pygame.draw.rect(self.screen, 'green', [locations[i][0] * 100 + 1, locations[i][1] * 100 + 1, 
                                    100, 100], 5)

    def draw_captured_values(self, red_captured_values, green_captured_values, round_counter):
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
            self.screen.blit(self.font.render(line, True, 'black'), (820, y_offset))
            y_offset += 60
            pass

    def draw_poisoned_apples(self, locations, poison_location):
        """
        Allows players to place poisoned apples on the board during the initial setup phase.

        Parameters:
        None

        Returns:
        None
        """
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x_coord = event.pos[0] // 100
                y_coord = event.pos[1] // 100
                click_coords = (x_coord, y_coord)
            
                # red to put poison
                if turn_step_putting_poison == 0 and click_coords in locations and click_coords != (0, 0) and click_coords not in red_golden_locations and click_coords not in red_poison_locations:
                    red_poison_locations.append(click_coords)
                    red_piece_index = locations.index(click_coords)
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


    def draw_golden_clues(self):
        pass

    def update_options(self):
        pass

    def check_valid_moves(self):
        return []

    def draw_valid(self, valid_moves):
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)

    def add_apple_values(self):
        pass

    def update_shield(self):
        pass

    def check_game_over(self):
        pass
