
import pygame
import random
import sys

CELL_SIZE = 40
TOP_HEIGHT = 42
BOTTOM_HEIGHT = 28

BACKGROUND = (76, 88, 68)
WHITE = (255, 255, 255)
YELLOW = (196, 181, 80)
CELL_COLOR = (61, 72, 55)
OPEN_COLOR = (105, 112, 88)
BORDER = (130, 139, 112)

pygame.init()

cell_font = pygame.font.Font(None, 30)
info_font = pygame.font.Font(None, 25)
small_font = pygame.font.Font(None, 21)


# Создание игрового поля и размещение мин
def create_board(rows, cols, mines):
    board = []

    for row in range(rows):
        line = []

        for col in range(cols):
            line.append(0)

        board.append(line)

    placed_mines = 0

    while placed_mines < mines:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)

        if board[row][col] != -1:
            board[row][col] = -1
            placed_mines += 1

    return board


# Подсчёт мин вокруг каждой клетки
def calculate_numbers(board, rows, cols):
    for row in range(rows):
        for col in range(cols):

            if board[row][col] == -1:
                continue

            count = 0

            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):

                    if r >= 0 and r < rows and c >= 0 and c < cols:
                        if board[r][c] == -1:
                            count += 1

            board[row][col] = count

    return board


# Создание таблицы открытых клеток и флажков
def create_marks(rows, cols):
    marks = []

    for row in range(rows):
        line = []

        for col in range(cols):
            line.append(False)

        marks.append(line)

    return marks


# Открытие клетки и соседних пустых клеток
def open_cell(board, opened, flags, row, col, rows, cols):
    if row < 0 or row >= rows or col < 0 or col >= cols:
        return

    if opened[row][col] or flags[row][col]:
        return

    opened[row][col] = True

    if board[row][col] == 0:
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):

                if r != row or c != col:
                    open_cell(
                        board, opened, flags,
                        r, c, rows, cols
                    )


# Основная функция запуска игры
def start_game(rows=10, cols=10, mines=15,
               show_timer=True, show_counter=True):

    width = cols * CELL_SIZE
    height = TOP_HEIGHT + rows * CELL_SIZE + BOTTOM_HEIGHT

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Сапёр")

    board = create_board(rows, cols, mines)
    board = calculate_numbers(board, rows, cols)

    opened = create_marks(rows, cols)
    flags = create_marks(rows, cols)

    first_click = True
    game_over = False
    win = False

    start_ticks = None
    end_ticks = None

    running = True

    while running:
        # Обработка нажатий клавиш и мыши
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                # Перезапуск игры
                if event.key == pygame.K_r and game_over:
                    board = create_board(rows, cols, mines)
                    board = calculate_numbers(board, rows, cols)

                    opened = create_marks(rows, cols)
                    flags = create_marks(rows, cols)

                    first_click = True
                    game_over = False
                    win = False

                    start_ticks = None
                    end_ticks = None

            # Открытие клеток и установка флажков
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

                mouse_x, mouse_y = event.pos

                col = mouse_x // CELL_SIZE
                row = (mouse_y - TOP_HEIGHT) // CELL_SIZE

                if 0 <= row < rows and 0 <= col < cols:

                    if event.button == 1:

                        if not flags[row][col] and not opened[row][col]:

                            # При первом нажатии мины не будет
                            if first_click:
                                while board[row][col] == -1:
                                    board = create_board(rows, cols, mines)
                                    board = calculate_numbers(board, rows, cols)

                                first_click = False
                                start_ticks = pygame.time.get_ticks()

                            if board[row][col] == -1:
                                game_over = True
                                win = False
                                end_ticks = pygame.time.get_ticks()

                            else:
                                open_cell(
                                    board, opened, flags,
                                    row, col, rows, cols
                                )

                    if event.button == 3:

                        if not opened[row][col]:
                            flags[row][col] = not flags[row][col]

        # Подсчёт открытых клеток и установленных флажков
        opened_count = 0
        flag_count = 0

        for row in range(rows):
            for col in range(cols):

                if opened[row][col]:
                    opened_count += 1

                if flags[row][col]:
                    flag_count += 1

        # Проверка победы
        if opened_count == rows * cols - mines and not game_over:
            game_over = True
            win = True
            end_ticks = pygame.time.get_ticks()

        # Расчёт времени игры
        if start_ticks is None:
            elapsed = 0

        elif end_ticks is None:
            elapsed = (pygame.time.get_ticks() - start_ticks) // 1000

        else:
            elapsed = (end_ticks - start_ticks) // 1000

        minutes = elapsed // 60
        seconds = elapsed % 60

        screen.fill(BACKGROUND)

        # Отображение счётчика мин и таймера
        if game_over:
            if win:
                message = "ПОБЕДА!"
            else:
                message = "ПОРАЖЕНИЕ"
        else:
            message = "САПЁР"

        if not show_counter and not show_timer:
            title = info_font.render(message, True, YELLOW)
            title_rect = title.get_rect(
                center=(width // 2, TOP_HEIGHT // 2)
            )
            screen.blit(title, title_rect)

        if show_counter:
            counter = info_font.render(
                "МИНЫ: " + str(mines - flag_count),
                True,
                WHITE
            )

            screen.blit(counter, (8, 11))

        if show_timer:
            timer = info_font.render(
                "ВРЕМЯ: {:02d}:{:02d}".format(minutes, seconds),
                True,
                WHITE
            )

            timer_rect = timer.get_rect(
                right=width - 8,
                centery=TOP_HEIGHT // 2
            )

            screen.blit(timer, timer_rect)

        # Отрисовка игрового поля
        for row in range(rows):
            for col in range(cols):

                x = col * CELL_SIZE
                y = TOP_HEIGHT + row * CELL_SIZE

                if opened[row][col]:
                    color = OPEN_COLOR
                else:
                    color = CELL_COLOR

                pygame.draw.rect(
                    screen,
                    color,
                    (x, y, CELL_SIZE - 1, CELL_SIZE - 1)
                )

                pygame.draw.rect(
                    screen,
                    BORDER,
                    (x, y, CELL_SIZE - 1, CELL_SIZE - 1),
                    1
                )

                if opened[row][col]:

                    if board[row][col] == -1:
                        pygame.draw.circle(
                            screen,
                            YELLOW,
                            (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                            9
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

                # Показ всех мин после окончания игры
                if game_over and board[row][col] == -1:
                    pygame.draw.circle(
                        screen,
                        YELLOW,
                        (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        9
                    )

        # Подсказка управления
        if game_over:
            hint_text = "R - заново    ESC - меню"
        else:
            hint_text = "ЛКМ - открыть    ПКМ - флаг    ESC - меню"

        hint = small_font.render(hint_text, True, WHITE)

        hint_rect = hint.get_rect(
            center=(width // 2, height - BOTTOM_HEIGHT // 2)
        )

        screen.blit(hint, hint_rect)

        pygame.display.update()

    return
