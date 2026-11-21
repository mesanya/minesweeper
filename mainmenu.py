import pygame
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

font = pygame.font.Font(None, 42)
title_font = pygame.font.Font(None, 85)
small_font = pygame.font.Font(None, 25)

BACKGROUND = (76, 88, 68)
WHITE = (255, 255, 255)
YELLOW = (196, 181, 80)
BUTTON = (61, 72, 55)
BORDER = (130, 139, 112)

buttons = [
    pygame.Rect(250, 260, 300, 65),
    pygame.Rect(250, 345, 300, 65),
    pygame.Rect(250, 430, 300, 65)
]

names = ["НАЧАТЬ ИГРУ", "НАСТРОЙКИ", "ВЫХОД"]

running = True

while running:
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                if buttons[0].collidepoint(mouse):
                    import minesweeper
                    minesweeper.start_game()

                elif buttons[1].collidepoint(mouse):
                    print("Настройки")

                elif buttons[2].collidepoint(mouse):
                    running = False

    screen.fill(BACKGROUND)

    title = title_font.render("MINESWEEPER", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, 145))
    screen.blit(title, title_rect)

    subtitle = small_font.render("CLASSIC GAME", True, YELLOW)
    subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 200))
    screen.blit(subtitle, subtitle_rect)

    pygame.draw.line(screen, YELLOW, (250, 225), (550, 225), 2)

    for i in range(3):
        if buttons[i].collidepoint(mouse):
            text_color = YELLOW
            border_color = YELLOW
        else:
            text_color = WHITE
            border_color = BORDER

        pygame.draw.rect(screen, BUTTON, buttons[i])
        pygame.draw.rect(screen, border_color, buttons[i], 2)

        text = font.render(names[i], True, text_color)
        text_rect = text.get_rect(center=buttons[i].center)

        screen.blit(text, text_rect)

    footer = small_font.render("POWERED BY PYTHON & PYGAME", True, WHITE)
    footer_rect = footer.get_rect(center=(WIDTH // 2, 550))
    screen.blit(footer, footer_rect)

    pygame.display.update()

pygame.quit()
sys.exit()
