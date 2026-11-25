import pygame
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

font = pygame.font.Font(None, 38)
title_font = pygame.font.Font(None, 80)
small_font = pygame.font.Font(None, 25)

BACKGROUND = (76, 88, 68)
WHITE = (255, 255, 255)
YELLOW = (196, 181, 80)
BUTTON = (61, 72, 55)
BORDER = (130, 139, 112)

DIFFICULTIES = [
    (8, 8, 10),
    (10, 10, 15),
    (16, 16, 40)
]

difficulty_names = ["ЛЁГКАЯ", "СРЕДНЯЯ", "СЛОЖНАЯ"]
selected_difficulty = 1
show_timer = True
show_counter = True
in_settings = False
running = True

menu_buttons = [
    pygame.Rect(250, 260, 300, 65),
    pygame.Rect(250, 345, 300, 65),
    pygame.Rect(250, 430, 300, 65)
]

settings_buttons = [
    pygame.Rect(170, 250, 145, 55),
    pygame.Rect(327, 250, 145, 55),
    pygame.Rect(484, 250, 145, 55)
]

timer_button = pygame.Rect(250, 345, 300, 50)
counter_button = pygame.Rect(250, 410, 300, 50)
back_button = pygame.Rect(300, 490, 200, 55)


def draw_button(rect, text, selected=False):
    mouse = pygame.mouse.get_pos()

    if selected or rect.collidepoint(mouse):
        text_color = YELLOW
        border_color = YELLOW
    else:
        text_color = WHITE
        border_color = BORDER

    pygame.draw.rect(screen, BUTTON, rect)
    pygame.draw.rect(screen, border_color, rect, 2)

    label = font.render(text, True, text_color)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)


while running:
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if in_settings:
                for i in range(3):
                    if settings_buttons[i].collidepoint(event.pos):
                        selected_difficulty = i

                if timer_button.collidepoint(event.pos):
                    show_timer = not show_timer

                if counter_button.collidepoint(event.pos):
                    show_counter = not show_counter

                if back_button.collidepoint(event.pos):
                    in_settings = False

            else:
                if menu_buttons[0].collidepoint(event.pos):
                    import minesweeper

                    rows, cols, mines = DIFFICULTIES[selected_difficulty]

                    minesweeper.start_game(
                        rows, cols, mines,
                        show_timer, show_counter
                    )

                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    pygame.display.set_caption("Minesweeper")

                elif menu_buttons[1].collidepoint(event.pos):
                    in_settings = True

                elif menu_buttons[2].collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    screen.fill(BACKGROUND)

    if in_settings:
        title = title_font.render("НАСТРОЙКИ", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, 135))
        screen.blit(title, title_rect)

        subtitle = small_font.render("ВЫБОР СЛОЖНОСТИ", True, YELLOW)
        subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 205))
        screen.blit(subtitle, subtitle_rect)

        for i in range(3):
            draw_button(
                settings_buttons[i],
                difficulty_names[i],
                i == selected_difficulty
            )

            rows, cols, mines = DIFFICULTIES[i]

            size_text = small_font.render(
                str(rows) + "x" + str(cols) + " / " + str(mines) + " мин",
                True,
                WHITE
            )

            size_rect = size_text.get_rect(
                center=(settings_buttons[i].centerx, 315)
            )

            screen.blit(size_text, size_rect)

        timer_text = "ТАЙМЕР: ВКЛ" if show_timer else "ТАЙМЕР: ВЫКЛ"
        counter_text = "СЧЁТЧИК МИН: ВКЛ" if show_counter else "СЧЁТЧИК МИН: ВЫКЛ"


        draw_button(timer_button, timer_text)
        draw_button(counter_button, counter_text)
        draw_button(back_button, "НАЗАД")

    else:
        title = title_font.render("MINESWEEPER", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, 145))
        screen.blit(title, title_rect)

        subtitle = small_font.render("CLASSIC GAME", True, YELLOW)
        subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 200))
        screen.blit(subtitle, subtitle_rect)

        pygame.draw.line(screen, YELLOW, (250, 225), (550, 225), 2)

        names = ["НАЧАТЬ ИГРУ", "НАСТРОЙКИ", "ВЫХОД"]

        for i in range(3):
            draw_button(menu_buttons[i], names[i])

        footer = small_font.render(
            "POWERED BY PYTHON & PYGAME",
            True,
            WHITE
        )

        footer_rect = footer.get_rect(center=(WIDTH // 2, 550))
        screen.blit(footer, footer_rect)

    pygame.display.update()

pygame.quit()
sys.exit()
