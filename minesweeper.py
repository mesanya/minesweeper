
import pygame
import random


ROWS = 10
COLS = 10
MINES = 15

CELL_SIZE = 45

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE + 80

BACKGROUND = (76, 88, 68)
WHITE = (255, 255, 255)
YELLOW = (196, 181, 80)
CELL_COLOR = (61, 72, 55)


def create_board():
    board = []

    for row in range(ROWS):
        line = []

        for col in range(COLS):
            line.append(0)

        board.append(line)

    mines = 0

    while mines < MINES:
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)

        if board[row][col] != -1:
            board[row][col] = -1
            mines += 1

    return board


def calculate_numbers(board):
    for row in range(ROWS):
        for col in range(COLS):

            if board[row][col] == -1:
                continue

            count = 0

            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):

                    if r >= 0 and r < ROWS and c >= 0 and c < COLS:
                        if board[r][c] == -1:
                            count += 1

            board[row][col] = count

    return board


def start_game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Сапёр")

    board = create_board()
    board = calculate_numbers(board)

    running = True

    while running:
        screen.fill(BACKGROUND)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for row in range(ROWS):
            for col in range(COLS):

                x = col * CELL_SIZE
                y = row * CELL_SIZE + 80

                pygame.draw.rect(
                    screen,
                    CELL_COLOR,
                    (x, y, CELL_SIZE - 2, CELL_SIZE - 2)
                )

        pygame.display.update()

    return
