import pygame
import pygame_widgets
import Data
import Drawing
import Logic

pygame.init()
window = pygame.display.set_mode((Data.width, Data.height))
pygame.display.set_caption(Data.name)


def flushDisplay(events):
    pygame.display.flip()
    pygame.display.update()
    pygame_widgets.update(events)


def main():
    clock = pygame.time.Clock()
    run = True
    drawing = Drawing.Drawing()
    logic = Logic.Logic()

    while run:
        clock.tick(Data.fps)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    logic.handleLeftMouseDown()
                elif event.button == 3:
                    logic.handleRightMouseDown()
            if event.type == pygame.KEYDOWN:
                logic.handleKeyPress(event.key)

        drawing.drawGame(window)
        flushDisplay(events)
        logic.gameLogic()

    quitGame()


def quitGame():
    pygame.quit()
    quit(0)


if __name__ == '__main__':
    main()
