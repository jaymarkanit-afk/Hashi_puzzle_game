import pygame

pygame.init()

WINDOW_WIDTH = 880
WINDOW_HEIGHT = 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def easy_mode():
    pass

def medium_mode():
    pass

def hard_mode():
    pass

FPS = 60
clock = pygame.time.Clock()
running = True

# == Main Menu ==

def main_menu():
    """Display the main menu and handle user input.

    Press 1/2/3 to select difficulty. Close window or press ESC to quit.
    """
    font = pygame.font.SysFont(None, 55)
    small_font = pygame.font.SysFont(None, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_1:
                    easy_mode()
                elif event.key == pygame.K_2:
                    medium_mode()
                elif event.key == pygame.K_3:
                    hard_mode()

        screen.fill((0, 0, 0))
        title_text = font.render("Hashi Puzzle Game", True, (255, 255, 255))
        easy_text = font.render("1. Easy Mode", True, (255, 255, 255))
        medium_text = font.render("2. Medium Mode", True, (255, 255, 255))
        hard_text = font.render("3. Hard Mode", True, (255, 255, 255))
        instruct = small_font.render("Press 1/2/3 to choose, ESC to quit", True, (200, 200, 200))

        screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 100))
        screen.blit(easy_text, (WINDOW_WIDTH // 2 - easy_text.get_width() // 2, 250))
        screen.blit(medium_text, (WINDOW_WIDTH // 2 - medium_text.get_width() // 2, 350))
        screen.blit(hard_text, (WINDOW_WIDTH // 2 - hard_text.get_width() // 2, 450))
        screen.blit(instruct, (WINDOW_WIDTH // 2 - instruct.get_width() // 2, 540))

        pygame.display.flip()
        clock.tick(FPS)


def main():
    try:
        main_menu()
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()