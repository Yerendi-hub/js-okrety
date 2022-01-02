import pygame

import RectUtils
import Data
from Utils import GameState, Colors, TextUtility, BoardMarkersUtils, BoardMarkers, Tour, Drawer


class Drawing:

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
        Drawer.drawButton(self.__window, "start", Data.startButton,
                          color=Colors.red if Data.anyShipLeftToPlace(Data.playerShips) else Colors.blue)
        Drawer.drawButton(self.__window, "reset", Data.resetButton)
        countShips = (Data.countUnplacedShips(1), Data.countUnplacedShips(2),
                      Data.countUnplacedShips(3), Data.countUnplacedShips(4))

        drawPlaceShipButton = lambda s, data, count: Drawer.drawButton(self.__window, s, data, textSize=35,
                                                                       color=Colors.green if count > 0 else Colors.red)

        drawPlaceShipButton(f"one mast ({countShips[0]})", Data.oneMastButton, countShips[0])
        drawPlaceShipButton(f"two mast ({countShips[1]})", Data.twoMastButton, countShips[1])
        drawPlaceShipButton(f"three mast ({countShips[2]})", Data.threeMastButton, countShips[2])
        drawPlaceShipButton(f"four mast ({countShips[3]})", Data.fourMastButton, countShips[3])

        mouse_pos = pygame.mouse.get_pos()
        coord = RectUtils.getPlayerBoardCoordinate(mouse_pos)
        Data.currentShip.setCoords(coord, Data.shipOrientation)

        for row in range(0, Data.gridSize):
            for col in range(0, Data.gridSize):
                c = BoardMarkersUtils.getColorBaseOnBoardMarker(Data.playerShipsGrid[row][col])

                if Data.playerShipsGrid[row][col] == BoardMarkers.shipNeighborhood:
                    c = Colors.gray

                if Data.currentShip.numberOfMasts > 0 and (row, col) in Data.currentShip.gridFields:
                    c = BoardMarkersUtils.getColorBaseOnBoardMarker(BoardMarkers.placeShip)

                pygame.draw.rect(self.__window, c, Data.playerButtonsGrid[row][col])

    def __drawGame(self):
        Drawer.drawButton(self.__window, "reset", Data.resetButton)

        for row in range(0, Data.gridSize):
            for col in range(0, Data.gridSize):
                c = BoardMarkersUtils.getColorBaseOnBoardMarker(Data.playerShipsGrid[row][col])
                pygame.draw.rect(self.__window, c, Data.playerButtonsGrid[row][col])

                c = BoardMarkersUtils.getColorBaseOnBoardMarker(Data.enemyShipsGrid[row][col])
                if Data.enemyShipsGrid[row][col] == BoardMarkers.ship:
                    c = BoardMarkersUtils.getColorBaseOnBoardMarker(BoardMarkers.water)
                pygame.draw.rect(self.__window, c, Data.enemyButtonsGrid[row][col])

        if Data.tour == Tour.gameEnd:
            winner = "Wygrana!" if Data.winner == Tour.player else "Przegrana!"
            Drawer.textToScreen(self.__window, winner, Data.winnerText[0], Data.winnerText[1], size=30)
        else:
            Drawer.textToScreen(self.__window,
                                       f"1-maszt przeciwnika: {Data.countAliveShips(1, Data.enemyShips, Data.enemyShipsGrid)}",
                                       Data.oneMastButton[0], Data.oneMastButton[1], size=30)
            Drawer.textToScreen(self.__window,
                                       f"2-maszt przeciwnika: {Data.countAliveShips(2, Data.enemyShips, Data.enemyShipsGrid)}",
                                       Data.twoMastButton[0], Data.twoMastButton[1], size=30)
            Drawer.textToScreen(self.__window,
                                       f"3-maszt przeciwnika: {Data.countAliveShips(3, Data.enemyShips, Data.enemyShipsGrid)}",
                                       Data.threeMastButton[0], Data.threeMastButton[1], size=30)
            Drawer.textToScreen(self.__window,
                                       f"4-maszt przeciwnika: {Data.countAliveShips(4, Data.enemyShips, Data.enemyShipsGrid)}",
                                       Data.fourMastButton[0], Data.fourMastButton[1], size=30)
