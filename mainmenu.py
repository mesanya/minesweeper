import pygame
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Сапёр")

font = pygame.font.Font(None, 50)
title_font = pygame.font.Font(None, 90)

WHITE = (255, 255, 255)
DARK = (30, 35, 45)
BUTTON = (55, 65, 80)
BUTTON_HOVER = (75, 90, 110)

buttons = [
    pygame.Rect(250, 250, 300, 65),
    pygame.Rect(250, 340, 300, 65),
    pygame.Rect(250, 430, 300, 65)
]

names = ["Начать игру", "Настройки", "Выход"]

running = True

while running:
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if buttons[0].collidepoint(mouse):
                    print("Начать игру")

                elif buttons[1].collidepoint(mouse):
                    print("Настройки")

                elif buttons[2].collidepoint(mouse):
                    running = False

    screen.fill(DARK)

    title = title_font.render("САПЁР", True, WHITE)
    screen.blit(title, (300, 120))

    for i in range(3):
        if buttons[i].collidepoint(mouse):
            color = BUTTON_HOVER
        else:
            color = BUTTON

        pygame.draw.rect(screen, color, buttons[i], border_radius=10)

        text = font.render(names[i], True, WHITE)
        text_rect = text.get_rect(center=buttons[i].center)

        screen.blit(text, text_rect)

    pygame.display.update()

pygame.quit()
sys.exit()
