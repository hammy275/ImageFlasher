import os
import pygame
import sys
import tkinter.filedialog

# Settings
PICTURE_CHANGES_PER_SECOND: int = 20
START_STOP_KEYS: list[int] = [pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER]

# Data from settings
pictures = []

# Game state
class GameState:
    picture_index: int = 0
    freeze_image: bool = False

game_state: GameState = GameState()

def do_quit():
    pygame.quit()
    sys.exit(0)

def main_loop(screen: pygame.Surface, clock: pygame.time.Clock):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            do_quit()

        if event.type == pygame.KEYDOWN:
            if event.key in START_STOP_KEYS:
                game_state.freeze_image = not game_state.freeze_image
            elif event.key == pygame.K_ESCAPE:
                do_quit()

    # Reset fill
    screen.fill("white")

    # Actual game loop
    if not game_state.freeze_image:
        game_state.picture_index += 1
        if game_state.picture_index == len(pictures):
            game_state.picture_index = 0

    pic = pygame.transform.scale(pictures[game_state.picture_index], screen.get_size())
    screen.blit(pic, pic.get_rect())

    pygame.display.flip()

    clock.tick(PICTURE_CHANGES_PER_SECOND)

def ask_and_load_photos() -> bool:
    main_window = tkinter.Tk()
    main_window.withdraw()
    picture_path = tkinter.filedialog.askdirectory(parent=main_window)
    main_window.destroy()
    pictures.clear()
    if picture_path == "":  # User didn't select a path
        sys.exit(0)
    for f in os.listdir(picture_path):
        try:
            pictures.append(pygame.image.load(os.path.join(picture_path, f)))
        except (FileNotFoundError, pygame.error):
            pass
    return len(pictures) > 1

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), flags=pygame.RESIZABLE)
    clock = pygame.time.Clock()

    while not ask_and_load_photos():
        pass

    while True:
        main_loop(screen, clock)

if __name__ == "__main__":
    main()
