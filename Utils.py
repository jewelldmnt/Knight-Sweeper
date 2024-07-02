import pygame
import random

def load_image(path, scale):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, scale)

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
