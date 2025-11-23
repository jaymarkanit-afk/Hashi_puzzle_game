import pygame
from solver import show_mode_screen

pygame.init()

WINDOW_WIDTH = 880
WINDOW_HEIGHT = 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hashi Puzzle Game")


# Prefer jpg then png.
BG = None
try:
    BG = pygame.image.load("background.jpg").convert()
except Exception:
    try:
        BG = pygame.image.load("background.png").convert()
    except Exception:
        BG = None

if BG:
    try:
        BG = pygame.transform.scale(BG, (WINDOW_WIDTH, WINDOW_HEIGHT))
    except Exception:
        pass

def easy_mode():
    pygame.display.set_caption("Easy Mode - Hashi Puzzle Game")
    show_mode_screen("Easy")


def medium_mode():
    pygame.display.set_caption("Medium Mode - Hashi Puzzle Game")
    show_mode_screen("Medium")


def hard_mode():
    pygame.display.set_caption("Hard Mode - Hashi Puzzle Game")
    show_mode_screen("Hard")


FPS = 60
clock = pygame.time.Clock()
running = True

# == Main Menu ==

def main_menu():
    """Display the main menu and handle mouse-clickable buttons.

    Buttons highlight on hover and respond to left-click.
    """
    font = pygame.font.SysFont(None, 55)
    small_font = pygame.font.SysFont(None, 28)
    title_font = pygame.font.SysFont(None, 86, bold=True)


    # Button layout
    btn_width = 320
    btn_height = 60
    btn_x = WINDOW_WIDTH // 2 - btn_width // 2
    btn_y_start = 290
    btn_gap = 20

    easy_rect = pygame.Rect(btn_x, btn_y_start, btn_width, btn_height)
    medium_rect = pygame.Rect(btn_x, btn_y_start + (btn_height + btn_gap), btn_width, btn_height)
    hard_rect = pygame.Rect(btn_x, btn_y_start + 2 * (btn_height + btn_gap), btn_width, btn_height)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if easy_rect.collidepoint(event.pos):
                    easy_mode()
                elif medium_rect.collidepoint(event.pos):
                    medium_mode()
                elif hard_rect.collidepoint(event.pos):
                    hard_mode()

        # Draw image background if available otherwise solid fill
        if BG:
            screen.blit(BG, (0, 0))
        else:
            screen.fill((0, 0, 0))

        title_line1 = title_font.render("Hashi", True, (255, 255, 255))
        title_line2 = title_font.render("puzzle", True, (255, 255, 255))
        y_start = 80
        screen.blit(title_line1, (WINDOW_WIDTH // 2 - title_line1.get_width() // 2, y_start))
        screen.blit(title_line2, (WINDOW_WIDTH // 2 - title_line2.get_width() // 2, y_start + title_line1.get_height() + 8))

        # Draw buttons with hover effect
        for rect, text_str in ((easy_rect, "Easy Mode"), (medium_rect, "Medium Mode"), (hard_rect, "Hard Mode")):
            is_hover = rect.collidepoint(mouse_pos)
            color = (70, 130, 180) if is_hover else (40, 40, 40)
            border = (200, 200, 200) if is_hover else (120, 120, 120)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, border, rect, 2)
            label = font.render(text_str, True, (255, 255, 255))
            screen.blit(label, (rect.x + rect.width // 2 - label.get_width() // 2, rect.y + rect.height // 2 - label.get_height() // 2))

        instruct = small_font.render("Click a button to start a mode, or press ESC to quit", True, (200, 200, 200))
        screen.blit(instruct, (WINDOW_WIDTH // 2 - instruct.get_width() // 2, WINDOW_HEIGHT - 60))

        pygame.display.flip()
        clock.tick(FPS)


def main():
    try:
        main_menu()
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()