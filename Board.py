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


    def draw_board(self, turn_step, count_red_shield, count_green_shield):
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
            pygame.draw.rect(screen, 'dark gray', (x * 100 + 1, y * 100 + 1, 98, 98))
        
        # Loop through green golden clue positions and draw blue highlight
        for pos in green_golden_clue_pos:
            x, y = pos
            pygame.draw.rect(screen, 'dark gray', (x * 100 + 1, y * 100 + 1, 98, 98))
            
    def draw_pieces(self):
        self.draw_color_pieces('red', self.red_locations)
        self.draw_color_pieces('green', self.green_locations)

    def draw_color_pieces(self, color, locations):
        for location in locations:
            rect = pygame.Rect(100 * location[0], 100 * location[1], 100, 100)
            pygame.draw.rect(self.screen, 'black', rect, 3)
            pygame.draw.rect(self.screen, 'gold', rect, 5)

            x_offset = 25 if color == 'red' else 0
            y_offset = 10
            pieces = self.red_pieces if color == 'red' else self.green_pieces
            piece = pieces[locations.index(location)]
            image = self.get_piece_image(color, piece)
            self.screen.blit(image, (100 * location[0] + x_offset, 100 * location[1] + y_offset))

    def get_piece_image(self, color, piece):
        if color == 'red':
            if piece == 'knight':
                return self.red_images[0]
            elif piece == 'apple':
                return self.red_images[1]
            elif piece == 'poison':
                return self.red_images[2]
            elif piece == 'golden':
                return self.red_images[3]
        else:
            if piece == 'knight':
                return self.green_images[0]
            elif piece == 'apple':
                return self.green_images[1]
            elif piece == 'poison':
                return self.green_images[2]
            elif piece == 'golden':
                return self.green_images[3]

    def draw_captured_values(self):
        pass

    def draw_poisoned_apples(self):
        pass



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
