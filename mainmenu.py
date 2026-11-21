from pathlib import Path
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

# папка SFX должна находиться рядом с mainmenu.py
SFX_DIR = Path(__file__).resolve().parent / "SFX"

# если аудиоустройство недоступно, меню продолжит работать без звука
audio_available = False
try:
    if pygame.mixer.get_init() is None:
        pygame.mixer.init()
    audio_available = True
except pygame.error as error:
    print(f"Не удалось инициализировать аудио: {error}")


def load_sound(filename, volume=0.7):
    """загружает звуковой эффект из папки SFX."""
    sound_path = SFX_DIR / filename
    if not sound_path.is_file():
        print(f"Не найден аудиофайл: {sound_path}")
        return None

    try:
        sound = pygame.mixer.Sound(str(sound_path))
        sound.set_volume(volume)
        return sound
    except pygame.error as error:
        print(f"Не удалось загрузить {sound_path}: {error}")
        return None


hover_sound = None
click_sound = None
music_loaded = False

if audio_available:
    hover_sound = load_sound("buttonrollover.wav")
    click_sound = load_sound("buttonclickrelease.wav")

    music_path = SFX_DIR / "mainmenu_Theme.mp3"
    if music_path.is_file():
        try:
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  # -1 - повторять музыку бесконечно
            music_loaded = True
        except pygame.error as error:
            print(f"Не удалось загрузить музыку {music_path}: {error}")
    else:
        print(f"Не найден аудиофайл: {music_path}")

running = True
hovered_button = None
exit_click_channel = None
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked_button = next(
                (i for i, button in enumerate(buttons) if button.collidepoint(event.pos)),
                None
            )

            if clicked_button is not None:
                click_channel = click_sound.play() if click_sound else None

                if clicked_button == 0:
                    # музыка главного меню не должна играть во время игры
                    if music_loaded:
                        pygame.mixer.music.stop()

                    import minesweeper
                    minesweeper.start_game()

                    # вернулись из игры в меню - снова запускаем тему меню
                    if running and music_loaded:
                        pygame.mixer.music.play(-1)

                elif clicked_button == 1:
                    print("Настройки")

                elif clicked_button == 2:
                    exit_click_channel = click_channel
                    running = False

    mouse = pygame.mouse.get_pos()
    current_hovered_button = next(
        (i for i, button in enumerate(buttons) if button.collidepoint(mouse)),
        None
    )

    # проигрываем rollover только при входе курсора на кнопку,
    # а не каждый кадр, пока курсор остаётся над ней
    if current_hovered_button is not None and current_hovered_button != hovered_button:
        if hover_sound:
            hover_sound.play()

    hovered_button = current_hovered_button

    screen.fill(BACKGROUND)

    title = title_font.render("MINESWEEPER", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, 145))
    screen.blit(title, title_rect)

    subtitle = small_font.render("CLASSIC GAME", True, YELLOW)
    subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 200))
    screen.blit(subtitle, subtitle_rect)

    pygame.draw.line(screen, YELLOW, (250, 225), (550, 225), 2)

    for i in range(3):
        if i == hovered_button:
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
    clock.tick(60)

# даём звуку кнопки «ВЫХОД» закончиться до закрытия аудиомикшера
if exit_click_channel is not None:
    while exit_click_channel.get_busy():
        clock.tick(60)

pygame.quit()
sys.exit()
