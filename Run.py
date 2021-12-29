import pygame
import GameLogic
import pygame_widgets
from Utils import GeneralData, Colors

pygame.init()
window = pygame.display.set_mode((GeneralData.width, GeneralData.height))
pygame.display.set_caption(GeneralData.name)


def draw_window(events):
#    window.fill(Colors.white)
#    pygame.draw.rect(window, Colors.red, pygame.Rect(10, 10, 100, 100))
    pygame.display.flip()
    pygame.display.update()
    pygame_widgets.update(events)


def main():
    clock = pygame.time.Clock()
    run = True
    gl = GameLogic.GameLogic(window)

    while run:
        clock.tick(GeneralData.fps)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        draw_window(events)

    pygame.quit()
    quit(0)


if __name__ == '__main__':
    main()
