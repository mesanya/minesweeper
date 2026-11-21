
import pygame
import sys

def start_game():
    WIDTH = 800
    HEIGHT = 600

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Сапёр")

    font = pygame.font.Font(None, 40)

    WHITE = (255, 255, 255)
    DARK = (30, 35, 45)
    CELL = (65, 80, 100)

    rows = 10
    cols = 10
    cell_size = 45

    board = []

    for row in range(rows):
        line = []

        for col in range(cols):
            line.append(0)

        board.append(line)

    running = True

    while running:
        screen.fill(DARK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for row in range(rows):
            for col in range(cols):
                x = 175 + col * cell_size
                y = 70 + row * cell_size

                pygame.draw.rect(
                    screen, CELL,
                    (x, y, cell_size - 2, cell_size - 2)
                )

        title = font.render("ИГРА", True, WHITE)
        screen.blit(title, (365, 20))

        pygame.display.update()
