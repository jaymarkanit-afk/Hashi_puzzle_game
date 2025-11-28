import pygame
from collections import deque
pygame.init()

WINDOW_WIDTH = 880
WINDOW_HEIGHT = 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

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
    
class HashiGame:
    """Main game class handling the puzzle logic"""
    def __init__(self, matrix):
        self.matrix = matrix
        self.islands = []
        self.island_grid = {}  
        self.selected_island = None
        self.ai_mode = False
        self.show_hints = False
        self.solution_steps = []    
        self.step_index = 0
        self.message = "Click islands to connect with bridges!"
        self.message_color = WHITE
        
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] > 0:
                    island = Island(row, col, matrix[row][col])
                    self.islands.append(island)
                    self.island_grid[(row, col)] = island
    
    def get_island_at_pos(self, x, y):
        """Get island at screen position"""
        col = x // tile_size
        row = y // tile_size
        return self.island_grid.get((row, col))
    
    def find_path_islands(self, island1, island2):
        """Returns all islands along the path between two islands, or None if invalid"""
        if island1.row == island2.row:  
            row = island1.row
            col_start = min(island1.col, island2.col)
            col_end = max(island1.col, island2.col)
            path = []
            for col in range(col_start + 1, col_end):
                if (row, col) in self.island_grid:
                    return None  
            return (island1, island2, 'h')
        elif island1.col == island2.col:  
            col = island1.col
            row_start = min(island1.row, island2.row)
            row_end = max(island1.row, island2.row)
            for row in range(row_start + 1, row_end):
                if (row, col) in self.island_grid:
                    return None  
            return (island1, island2, 'v')
        return None
    
    def check_bridge_crossing(self, island1, island2):
        """Check if adding bridge would cross existing bridges"""
        for island_a in self.islands:
            for island_b, count in island_a.neighbors.items():
                if count == 0:
                    continue
        
                if self.bridges_intersect(island1, island2, island_a, island_b):
                    return True
        return False
    
    def bridges_intersect(self, i1, i2, i3, i4):
        """Check if two bridges intersect"""
        
        if i1.row == i2.row and i3.col == i4.col:
            h_row = i1.row
            h_col_min, h_col_max = min(i1.col, i2.col), max(i1.col, i2.col)
            v_col = i3.col
            v_row_min, v_row_max = min(i3.row, i4.row), max(i3.row, i4.row)
            
            if h_col_min < v_col < h_col_max and v_row_min < h_row < v_row_max:
                return True
        
        if i1.col == i2.col and i3.row == i4.row:
            v_col = i1.col
            v_row_min, v_row_max = min(i1.row, i2.row), max(i1.row, i2.row)
            h_row = i3.row
            h_col_min, h_col_max = min(i3.col, i4.col), max(i3.col, i4.col)
            
            if h_col_min < v_col < h_col_max and v_row_min < h_row < v_row_max:
                return True
        
        return False

    def toggle_bridge(self, island1, island2):
        """Add or cycle bridges between two islands"""
        path_info = self.find_path_islands(island1, island2)
        if not path_info:
            self.message = "Invalid bridge: must be horizontal/vertical with no islands between"
            self.message_color = RED
            return False
        
        current_bridges = island1.neighbors.get(island2, 0)
        
        if current_bridges == 0:
            
            if self.check_bridge_crossing(island1, island2):
                self.message = "Bridges cannot cross!"
                self.message_color = RED
                return False
            if island1.can_add_bridge(island2, current_bridges):
                island1.add_bridge(island2)
                self.message = "Bridge added (1)"
                self.message_color = GREEN
                return True
            else:
                self.message = "Cannot add bridge: degree constraint violated"
                self.message_color = RED
                return False
        elif current_bridges == 1:
            
            if island1.can_add_bridge(island2, current_bridges):
                island1.add_bridge(island2)
                self.message = "Double bridge (2)"
                self.message_color = GREEN
                return True
            else:
                
                island1.remove_bridge(island2)
                self.message = "Bridge removed (0)"
                self.message_color = YELLOW
                return True
        else:  
            
            island1.remove_bridge(island2)
            island1.remove_bridge(island2)
            self.message = "All bridges removed (0)"
            self.message_color = YELLOW
            return True

    def is_connected(self):
        """Check if all islands form a connected graph (BFS)"""
        if not self.islands:
            return True
        
        visited = set()
        queue = deque([self.islands[0]])
        visited.add(self.islands[0])
        
        while queue:
            island = queue.popleft()
            for neighbor in island.neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return len(visited) == len(self.islands)

    def check_win(self):
        """Check if puzzle is solved"""
        
        for island in self.islands:
            if island.get_current_degree() != island.required_degree:
                return False
        
       
        if not self.is_connected():
            return False
        
        return True

    def get_possible_neighbors(self, island):
        """Get all islands that could potentially connect to this island"""
        neighbors = []
        
        for other in self.islands:
            if other != island and other.row == island.row:
                
                col_min = min(island.col, other.col)
                col_max = max(island.col, other.col)
                blocked = False
                for col in range(col_min + 1, col_max):
                    if (island.row, col) in self.island_grid:
                        blocked = True
                        break
                if not blocked:
                    neighbors.append(other)
        
        for other in self.islands:
            if other != island and other.col == island.col:
                
                row_min = min(island.row, other.row)
                row_max = max(island.row, other.row)
                blocked = False
                for row in range(row_min + 1, row_max):
                    if (row, island.col) in self.island_grid:
                        blocked = True
                        break
                if not blocked:
                    neighbors.append(other)
        
        return neighbors

    def solve_puzzle(self):
        """AI Solver using optimized constraint propagation + backtracking"""
        self.solution_steps = []
        
        for island in self.islands:
            island.neighbors.clear()
        
        # Try to solve with optimized algorithm
        max_iterations = 10000 
        iteration = 0
        
        changed = True
        while changed and iteration < max_iterations:
            changed = False
            iteration += 1
            
            for island in self.islands:
                if island.get_current_degree() >= island.required_degree:
                    continue
                
                needed = island.required_degree - island.get_current_degree()
                neighbors = self.get_possible_neighbors(island)
                
                # Filter to valid neighbors
                valid_neighbors = []
                for neighbor in neighbors:
                    current_bridges = island.neighbors.get(neighbor, 0)
                    if current_bridges < 2:
                        if not self.check_bridge_crossing(island, neighbor):
                            if island.can_add_bridge(neighbor, current_bridges):
                                valid_neighbors.append(neighbor)
                
                # Forced move: only one possible neighbor
                if len(valid_neighbors) == 1 and needed > 0:
                    neighbor = valid_neighbors[0]
                    bridges_to_add = min(2 - island.neighbors.get(neighbor, 0), needed)
                    for _ in range(bridges_to_add):
                        if island.can_add_bridge(neighbor, 0):
                            island.add_bridge(neighbor)
                            changed = True
                else:
                    # Stronger CSP rule: if the total possible capacity across
                    # all valid neighbors equals the needed amount, then all
                    # those capacities must be used (forward-checking).
                    if needed > 0 and valid_neighbors:
                        cap_list = []
                        total_cap = 0
                        for nb in valid_neighbors:
                            cur = island.neighbors.get(nb, 0)
                            cap_nb = 2 - cur
                            # limit by neighbor remaining need
                            nb_remain = nb.required_degree - nb.get_current_degree()
                            if nb_remain <= 0:
                                continue
                            cap = min(cap_nb, nb_remain)
                            if cap > 0:
                                cap_list.append((nb, cap))
                                total_cap += cap

                        if total_cap > 0 and total_cap == needed:
                            # enforce these capacities now
                            for nb, cap in cap_list:
                                add = min(cap, 2 - island.neighbors.get(nb, 0))
                                for _ in range(add):
                                    if island.can_add_bridge(nb, 0) and not self.check_bridge_crossing(island, nb):
                                        island.add_bridge(nb)
                                        changed = True
        
        # Check if solved
        if self.check_win():
            self.message = "Puzzle solved by AI!"
            self.message_color = GREEN
            return True
        
        # If not fully solved, try lightweight backtracking
        if self._smart_backtrack(0, 0):
            self.message = "Puzzle solved by AI!"
            self.message_color = GREEN
            return True
        else:
            self.message = "Partial solution - try solving manually!"
            self.message_color = YELLOW
            return False

    def _smart_backtrack(self, island_idx, depth):
        """Optimized recursive backtracking with depth limit"""
        # Depth limit to prevent freezing
        if depth > 100:
            return False
            
        # Base case: all islands processed
        if island_idx >= len(self.islands):
            return self.check_win()
        
        current_island = self.islands[island_idx]
        
        # Skip if already satisfied
        if current_island.get_current_degree() == current_island.required_degree:
            return self._smart_backtrack(island_idx + 1, depth)
        
        # Early termination: if impossible to satisfy
        needed = current_island.required_degree - current_island.get_current_degree()
        if needed <= 0:
            return self._smart_backtrack(island_idx + 1, depth)
        
        # Get valid neighbors
        possible_neighbors = self.get_possible_neighbors(current_island)
        valid_neighbors = []
        
        for neighbor in possible_neighbors:
            current_bridges = current_island.neighbors.get(neighbor, 0)
            if current_bridges < 2:
                if not self.check_bridge_crossing(current_island, neighbor):
                    if current_island.can_add_bridge(neighbor, current_bridges):
                        valid_neighbors.append(neighbor)
        
        # If no valid neighbors but still needs bridges, fail
        if not valid_neighbors and needed > 0:
            return False
        
        # Try adding bridges to each valid neighbor
        for neighbor in valid_neighbors:
            for num_bridges in [1, 2]:
                current_bridges = current_island.neighbors.get(neighbor, 0)
                
                if current_bridges + num_bridges > 2:
                    continue
                
                if current_bridges + num_bridges > needed:
                    continue
                
                # Add bridges
                added = []
                success = True
                for _ in range(num_bridges):
                    if current_island.can_add_bridge(neighbor, 0):
                        if not self.check_bridge_crossing(current_island, neighbor):
                            current_island.add_bridge(neighbor)
                            added.append(neighbor)
                        else:
                            success = False
                            break
                    else:
                        success = False
                        break
                
                if success and added:
                    # Try to continue
                    if self._smart_backtrack(island_idx, depth + 1):
                        return True
                    
                    # Backtrack
                    for _ in added:
                        current_island.remove_bridge(neighbor)
        
        # Try skipping this island
        return self._smart_backtrack(island_idx + 1, depth + 1)

    def get_hint(self):
        """Provide a hint for the next move"""
        # Simple hint: find island with only one valid way to satisfy its degree
        for island in self.islands:
            current_degree = island.get_current_degree()
            needed = island.required_degree - current_degree
            
            if needed <= 0:
                continue
            
            neighbors = self.get_possible_neighbors(island)
            valid_neighbors = []
            
            for neighbor in neighbors:
                current_bridges = island.neighbors.get(neighbor, 0)
                if current_bridges < 2:
                    if not self.check_bridge_crossing(island, neighbor):
                        if island.can_add_bridge(neighbor, current_bridges):
                            valid_neighbors.append(neighbor)
            
            if len(valid_neighbors) == 1 and needed > 0:
                return (island, valid_neighbors[0])
        
        return None

    def reset(self):
        """Reset all bridges"""
        for island in self.islands:
            island.neighbors.clear()
        self.selected_island = None
        self.message = "Puzzle reset!"
        self.message_color = YELLOW

# ========== DRAWING FUNCTIONS ==========
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

def draw_bridges(game):
    """Draw all bridges between islands"""
    drawn_pairs = set()
    
    for island in game.islands:
        for neighbor, num_bridges in island.neighbors.items():
            # Avoid drawing the same bridge twice
            pair = tuple(sorted([id(island), id(neighbor)]))
            if pair in drawn_pairs:
                continue
            drawn_pairs.add(pair)
            
            if num_bridges > 0:
                x1, y1 = island.x, island.y
                x2, y2 = neighbor.x, neighbor.y
                
                if num_bridges == 1:
                    # Single bridge
                    pygame.draw.line(screen, BLUE, (x1, y1), (x2, y2), 4)
                else:
                    # Double bridge - draw parallel lines
                    if island.row == neighbor.row:  # Horizontal
                        offset = 5
                        pygame.draw.line(screen, BLUE, (x1, y1 - offset), (x2, y2 - offset), 4)
                        pygame.draw.line(screen, BLUE, (x1, y1 + offset), (x2, y2 + offset), 4)
                    else:  # Vertical
                        offset = 5
                        pygame.draw.line(screen, BLUE, (x1 - offset, y1), (x2 - offset, y2), 4)
                        pygame.draw.line(screen, BLUE, (x1 + offset, y1), (x2 + offset, y2), 4)

def draw_islands(game):
    """Draw all islands with their numbers"""
    for island in game.islands:
        # Determine island color based on status
        current_degree = island.get_current_degree()
        if current_degree == island.required_degree:
            color = GREEN
        elif current_degree > island.required_degree:
            color = RED
        else:
            color = WHITE
        
        # Highlight selected island
        if island == game.selected_island:
            pygame.draw.circle(screen, YELLOW, (island.x, island.y), tile_size // 3 + 5)
        
        # Draw the island circle
        pygame.draw.circle(screen, color, (island.x, island.y), tile_size // 3)
        pygame.draw.circle(screen, BLACK, (island.x, island.y), tile_size // 3, 2)
        
        # Draw the required degree number
        text = font.render(str(island.required_degree), True, BLACK)
        text_rect = text.get_rect(center=(island.x, island.y))
        screen.blit(text, text_rect)

def draw_ui(game):
    """Draw UI elements: instructions, status, buttons"""
    # Message bar at top
    msg_surface = small_font.render(game.message, True, game.message_color)
    screen.blit(msg_surface, (10, 10))
    
    # Instructions at bottom
    instructions = [
        "Click two islands to connect | R: Reset | S: AI Solve | H: Hint | ESC: Quit"
    ]
    y_offset = WINDOW_HEIGHT - 30
    for instruction in instructions:
        text = small_font.render(instruction, True, LIGHT_GREY)
        screen.blit(text, (10, y_offset))
        y_offset += 20
    
    # Win check display
    if game.check_win():
        win_text = font.render("PUZZLE SOLVED! Congratulations!", True, GREEN)
        win_rect = win_text.get_rect(center=(WINDOW_WIDTH // 2, 30))
        pygame.draw.rect(screen, BLACK, win_rect.inflate(20, 10))
        screen.blit(win_text, win_rect)

def draw_hint(game, hint):
    """Draw hint arrow"""
    if hint:
        island1, island2 = hint
        # Draw animated arrow or highlight
        pygame.draw.line(screen, YELLOW, (island1.x, island1.y), (island2.x, island2.y), 3)
        # Draw circles around the islands
        pygame.draw.circle(screen, YELLOW, (island1.x, island1.y), tile_size // 3 + 8, 3)
        pygame.draw.circle(screen, YELLOW, (island2.x, island2.y), tile_size // 3 + 8, 3)

def show_mode_screen(mode_name, matrix):
    """Simple feedback screen shown when a mode is selected.

    Press ESC to return to the main menu.
    """
    # create a fresh game instance for this mode so each difficulty starts clean
    game = HashiGame(matrix)
    font = pygame.font.SysFont(None, 90)
    small = pygame.font.SysFont(None, 28)
    hint = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    x, y = event.pos
                    clicked_island = game.get_island_at_pos(x, y)
                    
                    if clicked_island:
                        if game.selected_island is None:
                            # First island selected
                            game.selected_island = clicked_island
                            game.message = f"Island selected at ({clicked_island.row}, {clicked_island.col})"
                            game.message_color = WHITE
                            hint = None
                        else:
                            # Second island selected - try to toggle bridge
                            if clicked_island == game.selected_island:
                                # Deselect
                                game.selected_island = None
                                game.message = "Selection cancelled"
                                game.message_color = WHITE
                            else:
                                # Toggle bridge
                                game.toggle_bridge(game.selected_island, clicked_island)
                                game.selected_island = None
                                hint = None
                    else:
                        # Clicked empty space - deselect
                        game.selected_island = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_r:
                    # Reset puzzle
                    game.reset()
                    hint = None
                elif event.key == pygame.K_s:
                        # AI Solve
                    game.message = "AI Solver running..."
                    game.message_color = YELLOW
                    draw_grid(tile_size)
                    draw_islands(game)
                    draw_ui(game)
                    pygame.display.update()
                    game.solve_puzzle()
                    hint = None
                elif event.key == pygame.K_h:
                    # Show hint
                    hint = game.get_hint()
                    if hint:
                        game.message = "Hint: Try connecting these islands!"
                        game.message_color = YELLOW
                    else:
                        game.message = "No obvious hints available"
                        game.message_color = WHITE

        screen.fill((16, 24, 32))

        # draw the grid overlay
        draw_grid(tile_size)
        draw_bridges(game)
        draw_islands(game)
        if hint:
            draw_hint(game, hint)
        draw_ui(game)

        text = font.render(f"{mode_name} Mode", True, (255, 255, 255))
        instr = small.render("Press ESC to return to the main menu", True, (200, 200, 200))
        screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - 60))
        screen.blit(instr, (WINDOW_WIDTH // 2 - instr.get_width() // 2, WINDOW_HEIGHT // 2 + 20))
        pygame.display.flip()
        clock.tick(FPS)
