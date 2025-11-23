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
