import pygame
import random

class Player():  # Player inherits from Board
    def __init__(self) -> None:
        self.WIDTH = 1000
        self.HEIGHT = 900
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.big_font = pygame.font.Font('freesansbold.ttf', 50)
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])

    def choose_color(self):
        """
        Function to let the player choose between Red and Green before starting the game.
        Returns:
            str: 'red' if the player chooses Red, 'green' if the player chooses Green.
        """
        colors = ['dark red', 'dark green']
        random.shuffle(colors)  # Shuffle the colors to randomize their positions
        
        while True: 
            self.screen.fill('white')
            text = self.font.render("Choose your color:", True, 'black')
            text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 50))
            self.screen.blit(text, text_rect)
            
            card_width, card_height = 200, 100
            card_margin = 50
            card1_button = pygame.Rect(self.WIDTH // 4 - card_width // 2, self.HEIGHT // 2, card_width, card_height)
            pygame.draw.rect(self.screen, 'gray', card1_button)  # Replace with initial hidden color
            pygame.draw.rect(self.screen, 'black', card1_button, 5)
            
            card2_button = pygame.Rect(3 * self.WIDTH // 4 - card_width // 2, self.HEIGHT // 2, card_width, card_height)
            pygame.draw.rect(self.screen, 'gray', card2_button)  # Replace with initial hidden color
            pygame.draw.rect(self.screen, 'black', card2_button, 5)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if card1_button.collidepoint(mouse_pos):
                        # Flip card 1 to reveal true color
                        pygame.draw.rect(self.screen, colors[0], card1_button)
                        pygame.display.flip()
                        pygame.time.wait(1000)  # Optional delay before returning color
                        return colors[0]
                    elif card2_button.collidepoint(mouse_pos):
                        # Flip card 2 to reveal true color
                        pygame.draw.rect(self.screen, colors[1], card2_button)
                        pygame.display.flip()
                        pygame.time.wait(1000)  # Optional delay before returning color
                        return colors[1]
                        
    def check_options(self, pieces, locations, turn):
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
                moves_list = self.check_knight(location, turn)
            all_moves_list.append(moves_list)
        return all_moves_list
    

    def check_knight(self, position, turn):
        """
        Checks for valid knight moves from a given position.

        Parameters:
        position (tuple): The current position of the knight.
        color (str): The color of the knight, either 'red' or 'green'.
        
        Returns:
        moves_list (list): A list of valid move positions for the knight.
        """
        moves_list = []
        if turn == 'red':
            enemies_list = [(x, y) for y in range(8) for x in range(4, 8)]
            friends_list = [(x, y) for y in range(8) for x in range(4)]
        else:
            enemies_list = [(x, y) for y in range(8) for x in range(4)]
            friends_list = [(x, y) for y in range(8) for x in range(4, 8)]
        
        
        # 8 squares to check for knight, they can go two squares in one direction and one in another
        targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
        for i in range(8):
            target = (position[0] + targets[i][0], position[1] + targets[i][1])
            if (target in friends_list or target in enemies_list) and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                moves_list.append(target)
        return moves_list