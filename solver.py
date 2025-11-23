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
tile_size = 80
rows = WINDOW_HEIGHT // tile_size
cols = WINDOW_WIDTH // tile_size
FPS = 60
clock = pygame.time.Clock()


# Font for island numbers
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# ========== ISLAND AND GRAPH CLASSES ==========
class Island:
    """Represents an island node in the puzzle"""
    def __init__(self, row, col, required_degree):
        self.row = row
        self.col = col
        self.required_degree = required_degree
        self.neighbors = {}  
        self.x = col * tile_size + tile_size // 2
        self.y = row * tile_size + tile_size // 2
    
    def get_current_degree(self):
        """Returns sum of all bridges connected to this island"""
        return sum(self.neighbors.values())
    
    def can_add_bridge(self, other_island, bridges):
        """Check if we can add a bridge to another island"""
        current = self.neighbors.get(other_island, 0)
        if current >= 2: 
            return False
        if self.get_current_degree() >= self.required_degree:
            return False
        if other_island.get_current_degree() >= other_island.required_degree:
            return False
        return True
    
    def add_bridge(self, other_island):
        """Add a bridge connection"""
        self.neighbors[other_island] = self.neighbors.get(other_island, 0) + 1
        other_island.neighbors[self] = other_island.neighbors.get(self, 0) + 1
    
    def remove_bridge(self, other_island):
        """Remove a bridge connection"""
        if other_island in self.neighbors:
            self.neighbors[other_island] -= 1
            if self.neighbors[other_island] == 0:
                del self.neighbors[other_island]
        if self in other_island.neighbors:
            other_island.neighbors[self] -= 1
            if other_island.neighbors[self] == 0:
                del other_island.neighbors[self]
    
    def __repr__(self):
        return f"Island({self.row},{self.col},{self.required_degree})"

def draw_grid(tile_size):
    """Draw semi-transparent grid lines"""
    # Create a transparent surface for the grid
    grid_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    
    # Draw grid lines with transparency (RGBA - last value is alpha/transparency)
    grid_color = (100, 100, 100, 80)  
    
    for x in range(tile_size, WINDOW_WIDTH, tile_size):
        pygame.draw.line(grid_surface, grid_color, (x, 0), (x, WINDOW_HEIGHT), 1)
    for y in range(tile_size, WINDOW_HEIGHT, tile_size):
        pygame.draw.line(grid_surface, grid_color, (0, y), (WINDOW_WIDTH, y), 1)
    
    # Blit the transparent grid onto the screen
    screen.blit(grid_surface, (0, 0))

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
        # draw the grid overlay
        draw_grid(tile_size)
        text = font.render(f"{mode_name} Mode", True, (255, 255, 255))
        instr = small.render("Press ESC to return to the main menu", True, (200, 200, 200))
        screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - 60))
        screen.blit(instr, (WINDOW_WIDTH // 2 - instr.get_width() // 2, WINDOW_HEIGHT // 2 + 20))
        pygame.display.flip()
        clock.tick(FPS)
