import pygame
import random
import sys

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
OPEN_COLOR = (105, 112, 88)
BORDER = (130, 139, 112)

pygame.init()

cell_font = pygame.font.Font(None, 32)
info_font = pygame.font.Font(None, 30)
small_font = pygame.font.Font(None, 23)


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


def open_cell(board, opened, flags, row, col):
    if row < 0 or row >= ROWS or col < 0 or col >= COLS:
        return

    if opened[row][col] or flags[row][col]:
        return

    opened[row][col] = True

    if board[row][col] == 0:
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if r != row or c != col:
                    open_cell(board, opened, flags, r, c)


def start_game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Сапёр")

    board = create_board()
    board = calculate_numbers(board)

    opened = []
    flags = []

    for row in range(ROWS):
        opened_line = []
        flags_line = []

        for col in range(COLS):
            opened_line.append(False)
            flags_line.append(False)

        opened.append(opened_line)
        flags.append(flags_line)

    game_over = False
    win = False
    first_click = True
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_r and game_over:
                    board = create_board()
                    board = calculate_numbers(board)

                    opened = []
                    flags = []

                    for row in range(ROWS):
                        opened_line = []
                        flags_line = []

                        for col in range(COLS):
                            opened_line.append(False)
                            flags_line.append(False)

                        opened.append(opened_line)
                        flags.append(flags_line)

                    game_over = False
                    win = False
                    first_click = True

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x, mouse_y = event.pos

                col = mouse_x // CELL_SIZE
                row = (mouse_y - 80) // CELL_SIZE

                if row >= 0 and row < ROWS and col >= 0 and col < COLS:

                    if event.button == 1:
                        if not flags[row][col] and not opened[row][col]:

                            if first_click:
                                while board[row][col] == -1:
                                    board = create_board()
                                    board = calculate_numbers(board)

                                first_click = False

                            if board[row][col] == -1:
                                game_over = True
                                win = False
                            else:
                                open_cell(board, opened, flags, row, col)

                    if event.button == 3:
                        if not opened[row][col]:
                            flags[row][col] = not flags[row][col]

        opened_count = 0

        for row in range(ROWS):
            for col in range(COLS):
                if opened[row][col]:
                    opened_count += 1

        if opened_count == ROWS * COLS - MINES and not game_over:
            game_over = True
            win = True

        screen.fill(BACKGROUND)

        if game_over:
            if win:
                message = "ПОБЕДА!"
            else:
                message = "МИНА! ВЫ ПРОИГРАЛИ"
        else:
            message = "ЛКМ - открыть    ПКМ - флаг"

        info = info_font.render(message, True, YELLOW)
        info_rect = info.get_rect(center=(WIDTH // 2, 25))
        screen.blit(info, info_rect)

        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE + 80

                if opened[row][col]:
                    color = OPEN_COLOR
                else:
                    color = CELL_COLOR

                pygame.draw.rect(
                    screen,
                    color,
                    (x, y, CELL_SIZE - 2, CELL_SIZE - 2)
                )

                pygame.draw.rect(
                    screen,
                    BORDER,
                    (x, y, CELL_SIZE - 2, CELL_SIZE - 2),
                    1
                )

                if opened[row][col]:
                    if board[row][col] == -1:
                        pygame.draw.circle(
                            screen,
                            YELLOW,
                            (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                            10
                        )

                    elif board[row][col] > 0:
                        number = cell_font.render(
                            str(board[row][col]),
                            True,
                            WHITE
                        )
                        number_rect = number.get_rect(
                            center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2)
                        )
                        screen.blit(number, number_rect)

                elif flags[row][col]:
                    flag = cell_font.render("F", True, YELLOW)
                    flag_rect = flag.get_rect(
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2)
                    )
                    screen.blit(flag, flag_rect)

                if game_over and board[row][col] == -1:
                    pygame.draw.circle(
                        screen,
                        YELLOW,
                        (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        10
                    )

        if game_over:
            hint = small_font.render(
                "R - заново    ESC - главное меню",
                True,
                WHITE
            )
        else:
            hint = small_font.render(
                "ESC - главное меню",
                True,
                WHITE
            )

        hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT - 12))
        screen.blit(hint, hint_rect)

        pygame.display.update()

    return
