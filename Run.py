import pygame
import GameLogic
import pygame_widgets
from Utils import GeneralData, Colors

pygame.init()
window = pygame.display.set_mode((GeneralData.width, GeneralData.height))
pygame.display.set_caption(GeneralData.name)


def draw_window():
    window.fill(Colors.white)
    gl.drawGame(window)


def flushDisplay(events):
    pygame.display.flip()
    pygame.display.update()
    pygame_widgets.update(events)


def main():
    clock = pygame.time.Clock()
    run = True
    global gl
    gl = GameLogic.GameLogic()

    while run:
        clock.tick(GeneralData.fps)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                gl.handleMouseDown()

        draw_window()
        flushDisplay(events)

    pygame.quit()
    quit(0)


if __name__ == '__main__':
    main()
