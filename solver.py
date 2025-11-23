import pygame

pygame.init()

WINDOW_WIDTH = 880
WINDOW_HEIGHT = 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hashi (Bridges) Puzzle Game - AI Solver Edition")

# Colors
WHITE = (255, 255, 255)
GREY = (60, 60, 60)
BG = (50, 50, 50)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
LIGHT_GREY = (150, 150, 150)

# Grid setup
# Grid setup
tile_size = 80
rows = WINDOW_HEIGHT // tile_size
cols = WINDOW_WIDTH // tile_size
FPS = 60
clock = pygame.time.Clock()

def show_mode_screen(mode_name):
    """Simple feedback screen shown when a mode is selected.

    Press ESC to return to the main menu.
    """
    font = pygame.font.SysFont(None, 90)
    small = pygame.font.SysFont(None, 28)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        screen.fill((16, 24, 32))
        text = font.render(f"{mode_name} Mode", True, (255, 255, 255))
        instr = small.render("Press ESC to return to the main menu", True, (200, 200, 200))
        screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - 60))
        screen.blit(instr, (WINDOW_WIDTH // 2 - instr.get_width() // 2, WINDOW_HEIGHT // 2 + 20))
        pygame.display.flip()
        clock.tick(FPS)
