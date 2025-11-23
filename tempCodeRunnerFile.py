
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

def show_mode_screen(mode_name):
    """Simple feedback screen shown when a mode is selected.

    Press ESC to return to the main menu.
    """
    font = pygame.font.SysFont(None, 72)
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


def easy_mode():
    show_mode_screen("Easy")


def medium_mode():
    show_mode_screen("Medium")