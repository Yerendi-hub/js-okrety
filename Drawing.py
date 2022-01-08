import pygame

import RectUtils
import Data
from Utils import GameState, Colors, BoardMarkersUtils, BoardMarkers, Tour, Drawer


class Drawing:
    """Class responsible for visual part of the game"""

    def __init__(self, window):
        self.__window = window

    def drawGame(self):
        """Method responsible for drawing game window"""

        self.__window.fill(Colors.white)  # draw background

        # depending on gameState we draw corresponding scenes
        match Data.gameState:
            case GameState.menu:
                self.__drawMenu()
            case GameState.placeShips:
                self.__drawPlaceShips()
            case GameState.game:
                self.__drawGame()

        # display.update does display magic, in this case double buffering surface swapping
        pygame.display.update()

    def __drawMenu(self):
        """Draw menu scene - start and quit buttons"""
        Drawer.drawButton(self.__window, "start", Data.startButton)
        Drawer.drawButton(self.__window, "quit", Data.quitButton)

    def __drawPlaceShips(self):
        """Draw placing ships scene - player board, start, restart and ships buttons"""
        Drawer.drawButton(self.__window, "start", Data.startButton,
                          color=Colors.red if Data.anyShipLeftToPlace(Data.playerShips) else Colors.blue)
        Drawer.drawButton(self.__window, "reset", Data.resetButton)

        # tuple of ships count
        countShips = (Data.countUnplacedShips(1), Data.countUnplacedShips(2),
                      Data.countUnplacedShips(3), Data.countUnplacedShips(4))

        # function to draw buttons for placing ships. It's lambda because we will use it only here
        drawPlaceShipButton = lambda s, data, count: Drawer.drawButton(self.__window, s, data, textSize=35,
                                                                       color=Colors.green if count > 0 else Colors.red)

        drawPlaceShipButton(f"one mast ({countShips[0]})", Data.oneMastButton, countShips[0])
        drawPlaceShipButton(f"two mast ({countShips[1]})", Data.twoMastButton, countShips[1])
        drawPlaceShipButton(f"three mast ({countShips[2]})", Data.threeMastButton, countShips[2])
        drawPlaceShipButton(f"four mast ({countShips[3]})", Data.fourMastButton, countShips[3])

        # we get position of the mouse, calculate coordinates from it and set it to fake ship - it allows us to
        # display "ghost" of the ship that we are currently placing
        mouse_pos = pygame.mouse.get_pos()
        coord = RectUtils.getPlayerBoardCoordinate(mouse_pos)
        Data.currentShip.setCoords(coord, Data.shipOrientation)

        # iterate over ships grid to draw players ships
        for row in range(0, Data.gridSize):
            for col in range(0, Data.gridSize):
                c = BoardMarkersUtils.getColorBaseOnBoardMarker(Data.playerShipsGrid[row][col])

                # while normally shipNeighborhood is treated as water, when we draw player board we want to show
                # adjacent fields to communicate to player that he can't place ships there
                if Data.playerShipsGrid[row][col] == BoardMarkers.shipNeighborhood:
                    c = Colors.gray

                # if we have field that is part of the ship then set ship color
                if Data.currentShip.numberOfMasts > 0 and (row, col) in Data.currentShip.gridFields:
                    if Data.playerShipsGrid[row][col] != BoardMarkers.water:
                        c = BoardMarkersUtils.getColorBaseOnBoardMarker(BoardMarkers.error)
                    else:
                        c = BoardMarkersUtils.getColorBaseOnBoardMarker(BoardMarkers.placeShip)

                # finally, we draw grid field with given color at given coordinates
                pygame.draw.rect(self.__window, c, Data.playerButtonsGrid[row][col])

    def __drawGame(self):
        """Draw main game scene - player and enemy board, restart button and remaining ships info"""
        Drawer.drawButton(self.__window, "reset", Data.resetButton)

        # iterate over ships grid to draw players and enemy ships
        for row in range(0, Data.gridSize):
            for col in range(0, Data.gridSize):

                # get color for player ship and draw it
                c = BoardMarkersUtils.getColorBaseOnBoardMarker(Data.playerShipsGrid[row][col])
                pygame.draw.rect(self.__window, c, Data.playerButtonsGrid[row][col])

                # get color for enemy ship and draw it. When we draw enemy ship then we don't want to draw parts
                # of the ship that has not been hit by player (BoardMarkers.ship). We draw them as water
                c = BoardMarkersUtils.getColorBaseOnBoardMarker(Data.enemyShipsGrid[row][col])
                if Data.enemyShipsGrid[row][col] == BoardMarkers.ship:
                    c = BoardMarkersUtils.getColorBaseOnBoardMarker(BoardMarkers.water)
                pygame.draw.rect(self.__window, c, Data.enemyButtonsGrid[row][col])

        # if one of players win the game then Data.tour is set to gameEnd, and we draw information about it
        if Data.tour == Tour.gameEnd:
            winner = "You won!" if Data.winner == Tour.player else "You loose!"
            Drawer.textToScreen(self.__window, winner, Data.winnerText[0], Data.winnerText[1], size=30)
        # otherwise, we draw information about remaining ships
        else:
            # function to draw ships info. It's lambda because we will use it only here
            drawText = lambda masts, rect: Drawer.textToScreen(self.__window,
                                                               f"{masts}-mast enemy: {Data.countAliveShips(masts, Data.enemyShips, Data.enemyShipsGrid)}",
                                                               rect[0], rect[1], size=30)
            drawText(1, Data.oneMastButton)
            drawText(2, Data.twoMastButton)
            drawText(3, Data.threeMastButton)
            drawText(4, Data.fourMastButton)
