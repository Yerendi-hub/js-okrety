import pygame
import Data
import Drawing
import Logic


def quitGame():
    """This function allows safe program exit."""
    pygame.quit()  # close pygame module
    quit(0)  # close program with code 0 - no error


def main():
    """Program initialization and update loop"""
    pygame.init()  # initialize pygame module
    window = pygame.display.set_mode((Data.width, Data.height))  # setup window
    pygame.display.set_caption(Data.name)  # set window name
    clock = pygame.time.Clock()  # set clock - it manages constant frame rate during the game
    run = True
    drawing = Drawing.Drawing(window)  # initialize drawing
    logic = Logic.Logic()  # initialize logic

    """
         it could be while True: with quitGame in event.type == pygame.QUIT, 
     but it is good practice letting program to finish processing events from last frame
     even if user request quit
    """
    while run:
        clock.tick(Data.fps)  # clock logic - handled by pygame.time module
        events = pygame.event.get()  # gather events.
        """
        Events in pygame are all things that occur while player interaction with game like pressing buttons,
        pressing mouse but also moving window, resizing it or quitting by pressing X on window
        """

        for event in events:
            if event.type == pygame.QUIT:
                run = False
            else:
                # while QUIT logic is executed from main loop, other events are handled by logic module
                logic.handleEvent(event)

        drawing.drawGame()
        logic.AI()

    quitGame()


# prevent to run program while using as module
if __name__ == '__main__':
    main()
